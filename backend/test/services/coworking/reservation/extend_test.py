"""ReservationService#extend_reservation method tests"""
import pytest
from unittest.mock import create_autospec

from requests import session
from backend.models.coworking.reservation import Reservation

from backend.models.coworking.seat import SeatIdentity
from backend.models.coworking.time_range import TimeRange
from backend.models.user import UserIdentity
from backend.services.coworking.reservation import (
    ReservationException,
    ReservationService,
)
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


def test_non_existent_reservation(
    reservation_svc: ReservationService,
):
    """Extend a non-existing reservation."""
    with pytest.raises(ResourceNotFoundException):
        NONEXISTENT_ID = 423
        res: Reservation = reservation_svc.extend_reservation(NONEXISTENT_ID, 60)


def test_negative_duration(
    reservation_svc: ReservationService, time: dict[str, datetime]
):
    """Extend an existing reservation by a non-positive amount."""
    reservation = reservation_svc.draft_reservation(
        user_data.root,
        reservation_data.test_request(
            {
                "users": [UserIdentity(**user_data.root.model_dump())],
                "seats": [seat_data.monitor_seat_10],
                "start": operating_hours_data.future.start,
                "end": operating_hours_data.future.start + ONE_HOUR,
            }
        ),
    )
    with pytest.raises(ReservationException):
        res: Reservation = reservation_svc.extend_reservation(
            reservation_data.reservation_4.id, 0
        )
    with pytest.raises(ReservationException):
        res: Reservation = reservation_svc.extend_reservation(
            reservation_data.reservation_4.id, -25
        )


def test_overlapping_reservation(
    reservation_svc: ReservationService, time: dict[str, datetime]
):
    """Extend an existing reservation that cannot be extendable due to overlapping reservation."""
    reservation = reservation_svc.draft_reservation(
        user_data.root,
        reservation_data.test_request(
            {
                "users": [UserIdentity(**user_data.root.model_dump())],
                "seats": [seat_data.monitor_seat_10],
                "start": operating_hours_data.future.start,
                "end": operating_hours_data.future.start + ONE_HOUR,
            }
        ),
    )
    reservation2 = reservation_svc.draft_reservation(
        user_data.user,
        reservation_data.test_request(
            {
                "users": [UserIdentity(**user_data.user.model_dump())],
                "seats": [seat_data.monitor_seat_10],
                "start": operating_hours_data.future.start + ONE_HOUR,
                "end": operating_hours_data.future.start + ONE_HOUR * 2,
            }
        ),
    )
    with pytest.raises(ReservationException):
        res: Reservation = reservation_svc.extend_reservation(reservation.id, 60)


def test_xl_closing(reservation_svc: ReservationService, time: dict[str, datetime]):
    """Extend an existing reservation by a time that would exceed operating hours."""
    with pytest.raises(ReservationException):
        res: Reservation = reservation_svc.extend_reservation(
            reservation_data.reservation_4.id,
            40,  # reservation_4 ends 30 minutes before XL closes
        )


def test_extending1(reservation_svc: ReservationService, time: dict[str, datetime]):
    """Extend an existing reservation."""
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
    res: Reservation = reservation_svc.extend_reservation(reservation.id, 85)
    assert res.end == reservation.end + timedelta(minutes=85)


def test_extending2(reservation_svc: ReservationService, time: dict[str, datetime]):
    """Extend an existing reservation."""
    reservation = reservation_svc.draft_reservation(
        user_data.secondUser,
        reservation_data.test_request(
            {
                "users": [UserIdentity(**user_data.secondUser.model_dump())],
                "seats": [seat_data.monitor_seat_01],
                "start": operating_hours_data.today.start + ONE_HOUR,
                "end": operating_hours_data.today.start + ONE_HOUR * 2,
            }
        ),
    )
    res: Reservation = reservation_svc.extend_reservation(reservation.id, 45)
    assert res.end == reservation.end + timedelta(minutes=45)
