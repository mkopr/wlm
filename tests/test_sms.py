import unittest
from unittest.mock import patch

from website_measure.sms import DummySMSSender


class TestDummySMSSender(unittest.TestCase):
    def setUp(self):
        self.sms_sender = DummySMSSender()
        self.main_website_place = 1
        self.all_websites = 3
        self.recipient_number = '123123123'

    @patch.object(DummySMSSender, 'send_message', create=True)
    def test_send_email(self, mock):
        self.sms_sender.send_message(
            self.main_website_place, self.all_websites, self.recipient_number
        )
        self.assertTrue(mock.called)
