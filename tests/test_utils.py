import unittest
from unittest.mock import patch
import datetime

from src.utils import set_greeting


class TestSetGreeting(unittest.TestCase):
    class TestSetGreeting(unittest.TestCase):

        @patch('datetime.datetime')
        def test_greeting_night(self, mock_datetime):
            mock_datetime.now.return_value = datetime.datetime(2023, 1, 1, 2, 0, 0)
            expected_greeting = "Доброй ночи"
            self.assertEqual(set_greeting(), expected_greeting)

        @patch('datetime.datetime')
        def test_greeting_morning(self, mock_datetime):
            mock_datetime.now.return_value = datetime.datetime(2023, 1, 1, 8, 0, 0)
            expected_greeting = "Доброе утро"
            self.assertEqual(set_greeting(), expected_greeting)

        @patch('datetime.datetime')
        def test_greeting_afternoon(self, mock_datetime):
            mock_datetime.now.return_value = datetime.datetime(2023, 1, 1, 14, 0, 0)
            expected_greeting = "Добрый день"
            self.assertEqual(set_greeting(), expected_greeting)

        @patch('datetime.datetime')
        def test_greeting_evening(self, mock_datetime):
            mock_datetime.now.return_value = datetime.datetime(2023, 1, 1, 19, 0, 0)
            expected_greeting = "Добрый вечер"
            self.assertEqual(set_greeting(), expected_greeting)

    if __name__ == '__main__':
        unittest.main()
