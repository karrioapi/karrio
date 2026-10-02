import unittest

import karrio.lib as lib


class TestFlocaltime(unittest.TestCase):
    def test_afternoon_time_uses_twelve_hour_clock(self):
        self.assertEqual(lib.flocaltime("15:42:00"), "03:42 PM")

    def test_midnight_hour_uses_twelve_hour_clock(self):
        self.assertEqual(lib.flocaltime("00:15:00"), "12:15 AM")

    def test_morning_time(self):
        self.assertEqual(lib.flocaltime("09:05:00"), "09:05 AM")

    def test_noon(self):
        self.assertEqual(lib.flocaltime("12:00:00"), "12:00 PM")

    def test_explicit_output_format_is_respected(self):
        self.assertEqual(
            lib.flocaltime("15:42:00", output_format="%H:%M"),
            "15:42",
        )


if __name__ == "__main__":
    unittest.main()
