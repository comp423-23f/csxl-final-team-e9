"""ReservationService#is_colab_open tests."""

import pytest
from unittest.mock import create_autospec

from backend.models.coworking.seat import SeatIdentity
from backend.models.coworking.time_range import TimeRange
from backend.models.user import UserIdentity
from backend.services.coworking.reservation import ReservationService
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
from .. import seat_data
from . import reservation_data
from backend.test.services.coworking import operating_hours_data


def test_is_colabl_open_true1(
    reservation_svc: ReservationService, time: dict[str, datetime]
):
    """Time range from operating hours start to end. is_colab_open should return True"""
    assert reservation_svc.is_colab_open(
        TimeRange(
            start=operating_hours_data.today.start, end=operating_hours_data.today.end
        )
    )


def test_is_colabl_open_one_sided2(
    reservation_svc: ReservationService, time: dict[str, datetime]
):
    """Time range from operating hours start to end + 1 hour. is_colab_open should return False"""
    assert not reservation_svc.is_colab_open(
        TimeRange(
            start=operating_hours_data.today.start,
            end=operating_hours_data.today.end + ONE_HOUR,
        )
    )
    """Time range from operating hours start - 30 minutes to end. is_colab_open should return False"""
    assert not reservation_svc.is_colab_open(
        TimeRange(
            start=operating_hours_data.today.start - THIRTY_MINUTES,
            end=operating_hours_data.today.end,
        )
    )


def test_is_colabl_open_outside_hours3(
    reservation_svc: ReservationService, time: dict[str, datetime]
):
    """Time range starting and ending before operating hours. is_colab_open should return False"""
    range = TimeRange(
        start=operating_hours_data.today.start - THIRTY_MINUTES,
        end=operating_hours_data.today.start - FIVE_MINUTES,
    )
    assert not reservation_svc.is_colab_open(range)


def test_is_colabl_open_two_operating_hours4(
    reservation_svc: ReservationService, time: dict[str, datetime]
):
    """Time range with large gap up of unavailability between start and end. is_colab_open should return False"""
    range = TimeRange(
        start=operating_hours_data.today.end - THIRTY_MINUTES,
        end=operating_hours_data.tomorrow.start + FIVE_MINUTES,
    )
    assert not reservation_svc.is_colab_open(range)
