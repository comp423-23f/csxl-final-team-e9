"""ReservationService#get_reservation_time_remaining method tests"""

import pytest
from unittest.mock import create_autospec

from backend.services.exceptions import ResourceNotFoundException
from .....services import PermissionService
from .....services.coworking import ReservationService
from .....services.coworking.reservation import ReservationException
from .....models.coworking import ReservationState
from .....models.user import UserIdentity
from .....models.coworking.seat import SeatIdentity
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
from .reservation_data import fake_data_fixture as insert_order_4
from ...core_data import user_data
from .. import operating_hours_data
from .. import seat_data
from . import reservation_data


def test_non_existent_reservation(
    reservation_svc: ReservationService,
):
    """Get extension eligibility for a non-existing reservation."""
    with pytest.raises(ResourceNotFoundException):
        NONEXISTENT_ID = 423
        amt: int = reservation_svc.get_reservation_time_remaining(NONEXISTENT_ID)


def test_time_remaining1(
    reservation_svc: ReservationService,
):
    reservation = reservation_svc.draft_reservation(
        user_data.root,
        reservation_data.test_request(
            {
                "users": [UserIdentity(**user_data.root.model_dump())],
                "seats": [seat_data.monitor_seat_00],
                "start": operating_hours_data.today.start,  # started an hour ago
                "end": operating_hours_data.today.end,  # end is 2 hours away
            }
        ),
    )
    assert (
        reservation_svc.get_reservation_time_remaining(reservation.id)
        == 2 * 60 * 60 - 1
    )


def test_time_remaining2(
    reservation_svc: ReservationService,
):
    reservation = reservation_svc.draft_reservation(
        user_data.root,
        reservation_data.test_request(
            {
                "users": [UserIdentity(**user_data.root.model_dump())],
                "seats": [seat_data.monitor_seat_10],
                "start": operating_hours_data.today.start,  # started an hour ago
                "end": operating_hours_data.today.start
                + 5 * THIRTY_MINUTES,  # should have 1.5 hours left
            }
        ),
    )
    assert reservation_svc.get_reservation_time_remaining(reservation.id) == 90 * 60 - 1


def test_time_remaining3(
    reservation_svc: ReservationService,
):
    reservation2 = reservation_svc.draft_reservation(
        user_data.root,
        reservation_data.test_request(
            {
                "users": [UserIdentity(**user_data.root.model_dump())],
                "seats": [seat_data.monitor_seat_10],
                "start": operating_hours_data.today.start,  # started an hour ago
                "end": operating_hours_data.today.start
                + ONE_HOUR
                + THIRTY_MINUTES
                + FIVE_MINUTES,  # should have 35 minutes left
            }
        ),
    )
    assert (
        reservation_svc.get_reservation_time_remaining(reservation2.id) == 35 * 60 - 1
    )
