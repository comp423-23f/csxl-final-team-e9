"""ReservationService#max_extension_amount tests."""

import pytest
from unittest.mock import create_autospec

from requests import session
from backend.models.coworking.reservation import Reservation

from backend.models.coworking.seat import SeatIdentity
from backend.models.coworking.time_range import TimeRange
from backend.models.user import UserIdentity
from backend.services.coworking.reservation import ReservationService
from backend.services.exceptions import ResourceNotFoundException
from ..fixtures import (
    reservation_svc,
    permission_svc,
    seat_svc,
    policy_svc,
    operating_hours_svc,
)
from ..time import *
from ...core_data import setup_insert_data_fixture as insert_order_0
from ..operating_hours_data import fake_data_fixture as insert_order_1
from ..room_data import fake_data_fixture as insert_order_2
from ..seat_data import fake_data_fixture as insert_order_3
from .reservation_data import delete_future_data, fake_data_fixture as insert_order_4

from ...core_data import user_data
from .. import seat_data
from . import reservation_data
from backend.test.services.coworking import operating_hours_data


# TESTS FOR CHECK_EXTENSION_CLOSE
def test_near_operating_hours1(
    reservation_svc: ReservationService, time: dict[str, datetime]
):
    """When operating hours end in 31 minutes, check_extension_close should return 30."""
    reservation = reservation_svc.draft_reservation(
        user_data.user,
        reservation_data.test_request(
            {
                "users": [UserIdentity(**user_data.user.model_dump())],
                "seats": [
                    SeatIdentity(**seat.model_dump())
                    for seat in seat_data.reservable_seats
                ],
                "start": operating_hours_data.future.end - timedelta(hours=2),
                "end": operating_hours_data.future.end - timedelta(minutes=31),
            }
        ),
    )
    assert reservation_svc.check_extension_close(reservation.id) == 30


def test_near_operating_hours2(
    reservation_svc: ReservationService, time: dict[str, datetime]
):
    """When operating hours end in 5 minutes, check_extension_close should return 0."""
    reservation = reservation_svc.draft_reservation(
        user_data.user,
        reservation_data.test_request(
            {
                "users": [UserIdentity(**user_data.user.model_dump())],
                "seats": [
                    SeatIdentity(**seat.model_dump())
                    for seat in seat_data.reservable_seats
                ],
                "start": operating_hours_data.future.end - timedelta(hours=2),
                "end": operating_hours_data.future.end - timedelta(minutes=5),
            }
        ),
    )
    assert reservation_svc.check_extension_close(reservation.id) == 0


def test_near_operating_hours3(
    reservation_svc: ReservationService, time: dict[str, datetime]
):
    """When operating hours end in 2 hours, check_extension_close should return 60."""
    reservation = reservation_svc.draft_reservation(
        user_data.user,
        reservation_data.test_request(
            {
                "users": [UserIdentity(**user_data.user.model_dump())],
                "seats": [
                    SeatIdentity(**seat.model_dump())
                    for seat in seat_data.reservable_seats
                ],
                "start": operating_hours_data.future.start,
                "end": operating_hours_data.future.end - timedelta(hours=2),
            }
        ),
    )
    assert reservation_svc.check_extension_close(reservation.id) == 60


def test_near_operating_hours4(
    reservation_svc: ReservationService, time: dict[str, datetime]
):
    """Operating hours end in 30 minutes, so check_extension_close should return 30."""
    assert (
        reservation_svc.check_extension_close(reservation_data.reservation_4.id) == 30
    )


# TESTS FOR CHECK_EXTENSION_OVERLAP
def test_overlapping_reservation1(
    reservation_svc: ReservationService, time: dict[str, datetime]
):
    """
    When there is a reservation starting 1 minute after yours,
    check_extension_overlap should return 0.
    When there is no reservation following the second reservation,
    check_extension_overlap should return 60.
    """
    reservation = reservation_svc.draft_reservation(
        user_data.user,
        reservation_data.test_request(
            {
                "users": [UserIdentity(**user_data.user.model_dump())],
                "seats": [seat_data.monitor_seat_00],
                "start": operating_hours_data.future.start,
                "end": operating_hours_data.future.start + ONE_HOUR,
            }
        ),
    )
    assert reservation_svc.check_extension_overlap(reservation.id) == 60
    reservation2 = reservation_svc.draft_reservation(
        user_data.root,
        reservation_data.test_request(
            {
                "users": [UserIdentity(**user_data.secondUser.model_dump())],
                "seats": [seat_data.monitor_seat_00],
                "start": operating_hours_data.future.start + ONE_HOUR + ONE_MINUTE,
                "end": operating_hours_data.future.start + ONE_HOUR + ONE_HOUR,
            }
        ),
    )
    assert reservation_svc.check_extension_overlap(reservation.id) == 0
    assert reservation_svc.check_extension_overlap(reservation2.id) == 60


def test_overlapping_reservation2(
    reservation_svc: ReservationService, time: dict[str, datetime]
):
    reservation = reservation_svc.draft_reservation(
        user_data.user,
        reservation_data.test_request(
            {
                "users": [UserIdentity(**user_data.user.model_dump())],
                "seats": [seat_data.monitor_seat_00],
                "start": operating_hours_data.future.start,  # relative 12:00
                "end": operating_hours_data.future.start + ONE_HOUR,  # 1:00
            }
        ),
    )
    assert reservation_svc.check_extension_overlap(reservation.id) == 60
    reservation2 = reservation_svc.draft_reservation(
        user_data.root,
        reservation_data.test_request(
            {
                "users": [UserIdentity(**user_data.secondUser.model_dump())],
                "seats": [seat_data.monitor_seat_00],
                "start": operating_hours_data.future.start
                + ONE_HOUR
                + THIRTY_MINUTES,  # 1:30
                "end": operating_hours_data.future.start + ONE_HOUR * 2,  # 2:00
            }
        ),
    )
    assert reservation_svc.check_extension_overlap(reservation.id) == 30
    assert reservation_svc.check_extension_overlap(reservation2.id) == 60
    reservation3 = reservation_svc.draft_reservation(
        user_data.user,
        reservation_data.test_request(
            {
                "users": [UserIdentity(**user_data.user.model_dump())],
                "seats": [seat_data.monitor_seat_00],
                "start": operating_hours_data.future.start
                + timedelta(minutes=145),  # 2:25
                "end": operating_hours_data.future.end,
            }
        ),
    )
    assert reservation_svc.check_extension_overlap(reservation2.id) == 15
    assert reservation_svc.check_extension_overlap(reservation3.id) == 60


def test_overlapping_reservation3(
    reservation_svc: ReservationService, time: dict[str, datetime]
):
    reservation = reservation_svc.draft_reservation(
        user_data.root,
        reservation_data.test_request(
            {
                "users": [UserIdentity(**user_data.root.model_dump())],
                "seats": [seat_data.monitor_seat_10],
                "start": operating_hours_data.tomorrow.start,  # relative 12:00
                "end": operating_hours_data.tomorrow.start + ONE_HOUR,  # 1:00
            }
        ),
    )
    assert reservation_svc.check_extension_overlap(reservation.id) == 60
    reservation2 = reservation_svc.draft_reservation(
        user_data.secondUser,
        reservation_data.test_request(
            {
                "users": [UserIdentity(**user_data.secondUser.model_dump())],
                "seats": [seat_data.monitor_seat_10],
                "start": operating_hours_data.tomorrow.start
                + timedelta(minutes=135),  # 2:15
                "end": operating_hours_data.tomorrow.start
                + timedelta(minutes=150),  # 2:30
            }
        ),
    )
    assert reservation_svc.check_extension_overlap(reservation.id) == 60
    assert (
        reservation_svc.check_extension_overlap(reservation2.id) == 60
    )  # should be 60 before reservation3 is made
    reservation3 = reservation_svc.draft_reservation(
        user_data.root,
        reservation_data.test_request(
            {
                "users": [UserIdentity(**user_data.root.model_dump())],
                "seats": [seat_data.monitor_seat_10],
                "start": operating_hours_data.tomorrow.start
                + timedelta(minutes=150),  # 2:30
                "end": operating_hours_data.tomorrow.start
                + timedelta(minutes=180),  # 3:00
            }
        ),
    )
    assert reservation_svc.check_extension_overlap(reservation.id) == 60
    assert (
        reservation_svc.check_extension_overlap(reservation2.id) == 0
    )  # becomes 0 after reservation3 is made
    assert reservation_svc.check_extension_overlap(reservation3.id) == 60


def test_non_existent_reservation(
    reservation_svc: ReservationService,
):
    """Get extension eligibility for a non-existing reservation."""
    with pytest.raises(ResourceNotFoundException):
        NONEXISTENT_ID = 423
        amt: int = reservation_svc.max_extension_amount(NONEXISTENT_ID)
    with pytest.raises(ResourceNotFoundException):
        NONEXISTENT_ID = 123
        amt: int = reservation_svc.check_extension_close(NONEXISTENT_ID)
    with pytest.raises(ResourceNotFoundException):
        NONEXISTENT_ID = 000
        amt: int = reservation_svc.check_extension_overlap(NONEXISTENT_ID)
