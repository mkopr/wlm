import unittest
from unittest.mock import patch

from website_measure.constants import MAIL_SUBJECT, MAIL_TEMPLATE
from website_measure.mail import MailSender


class TestMailSender(unittest.TestCase):
    def setUp(self):
        self.mail_sender = MailSender()
        self.main_website_place = 1
        self.all_websites = 3
        self.recipient_mail = 'example@example.com'

    def test_prepare_message(self):
        message = self.mail_sender.prepare_message(
            self.main_website_place, self.all_websites, self.recipient_mail
        )
        self.assertTrue(MAIL_SUBJECT in message)
        self.assertTrue(MAIL_TEMPLATE.format(
            main_website_place=self.main_website_place,
            all_websites=self.all_websites
        ) in message)

    @patch.object(MailSender, 'send_message', create=True)
    def test_send_email(self, mock):
        self.mail_sender.send_message(
            self.main_website_place, self.all_websites, self.recipient_mail
        )
        self.assertTrue(mock.called)
