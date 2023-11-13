import unittest
from datetime import datetime, timedelta
from your_module.reservation import ReservationService, TimeRange


class TestReservationService(unittest.TestCase):
    def test_is_colab_open_colab_open(self):
        # Create an instance of the ReservationService with actual dependencies
        reservation_service = ReservationService()

        # Choose a time range when Colab is expected to be open
        time_range = TimeRange(
            start=datetime(2023, 1, 1, 10, 0), end=datetime(2023, 1, 1, 12, 0)
        )

        result = reservation_service.is_colab_open(time_range)
        self.assertTrue(result)

    def test_is_colab_open_colab_closed(self):
        # Create an instance of the ReservationService with actual dependencies
        reservation_service = ReservationService()

        # Choose a time range when Colab is expected to be closed
        time_range = TimeRange(
            start=datetime(2023, 1, 1, 18, 0), end=datetime(2023, 1, 1, 20, 0)
        )

        result = reservation_service.is_colab_open(time_range)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
