"""ReservationService#check_extention_eligibility tests."""

import pytest
from unittest.mock import create_autospec

from backend.models.coworking.seat import SeatIdentity
from backend.models.coworking.time_range import TimeRange
from backend.models.user import UserIdentity
from backend.services.coworking.reservation import ReservationService

# Imported fixtures provide dependencies injected for the tests as parameters.
# Dependent fixtures (seat_svc) are required to be imported in the testing module.
from ..fixtures import (
    reservation_svc,
    permission_svc,
    seat_svc,
    policy_svc,
    operating_hours_svc,
)
from ..time import *

# Import the setup_teardown fixture explicitly to load entities in database.
# The order in which these fixtures run is dependent on their imported alias.
# Since there are relationship dependencies between the entities, order matters.
from ...core_data import setup_insert_data_fixture as insert_order_0
from ..operating_hours_data import fake_data_fixture as insert_order_1
from ..room_data import fake_data_fixture as insert_order_2
from ..seat_data import fake_data_fixture as insert_order_3
from .reservation_data import fake_data_fixture as insert_order_4

# Import the fake model data in a namespace for test assertions
from ...core_data import user_data
from .. import seat_data
from . import reservation_data
from backend.test.services.coworking import operating_hours_data


# check overlap
# check operating hours
# case 30 minutes left, extending 1 hour is false
# case 30 minutes left, extending 1 hour is false


# case several hours aeay, extending 1 hour is true
# case 1 hour, extending 1 hour is true, extending over 1 hour is false


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
                "start": operating_hours_data.future.end - timedelta(minutes=150),
                "end": operating_hours_data.future.end - timedelta(hours=2),
            }
        ),
    )
    assert reservation_svc.check_extension_close(reservation.id) == 60
