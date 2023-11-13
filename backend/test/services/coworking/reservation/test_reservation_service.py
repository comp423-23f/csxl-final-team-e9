from datetime import datetime, timedelta
import pytest
from unittest.mock import MagicMock


class TestReservationService:
    @pytest.fixture
    def mock_operating_hours_service(self):
        return MagicMock()
