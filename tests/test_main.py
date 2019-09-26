import io
import sys
import tempfile
import unittest
from time import time
from unittest.mock import patch

from website_measure.constants import RESULT_TEMPLATE
from website_measure.mail import MailSender
from website_measure.main import WebsiteMeasure
from website_measure.sms import DummySMSSender
from website_measure.website import WebsiteMeasurement


class TestWebsiteMeasure(unittest.TestCase):
    def setUp(self):
        self.main_website = 'https://stackoverflow.com'
        self.other_website_1 = 'https://facebook.com'
        self.other_website_2 = 'https://www.youtube.com/'
        self.phone_number = '+48123123123'
        self.mail = 'abcd@example.com'
        self.measure = WebsiteMeasure()
        self.test_directory = tempfile.TemporaryFile()

        self.measure.websites_list = [
            self.get_website_object(page) for page in [
                self.other_website_1, self.other_website_2
            ]
        ]
        self.measure.main_website = self.get_website_object(self.main_website)

    def tearDown(self):
        self.test_directory.close()

    def get_website_object(self, url, start_time=time(), end_time=time()):
        return WebsiteMeasurement(url, start_time, end_time)

    def parser_get_arguments(
            self, main_website, other_website, phone_number, mail
    ):
        parser = self.measure.get_arguments(
            [
                '-u', main_website,
                '-l', other_website,
                '-p', phone_number,
                '-m', mail
            ]
        )
        return parser

    def test_get_arguments(self):
        parser = self.parser_get_arguments(
            self.main_website, self.other_website_1, self.phone_number,
            self.mail
        )
        self.assertEqual(parser.url, self.main_website)
        self.assertEqual(parser.list, [self.other_website_1])
        self.assertEqual(parser.mail, self.mail)
        self.assertEqual(parser.phone_number, self.phone_number)

    def test_get_arguments_invalid_main_url(self):
        try:
            self.parser_get_arguments(
                123123, self.other_website_1, self.phone_number, self.mail
            )
        except TypeError:
            assert True
        else:
            assert False

    def test_get_arguments_invalid_other_url(self):
        try:
            self.parser_get_arguments(
                self.main_website, 123123, self.phone_number, self.mail
            )
        except TypeError:
            assert True
        else:
            assert False

    def test_get_arguments_without_phone_number_argument(self):
        parser = self.measure.get_arguments(
            [
                '-u', self.main_website,
                '-l', self.other_website_1,
                '-m', self.mail
            ]
        )
        self.assertEqual(parser.url, self.main_website)
        self.assertEqual(parser.list, [self.other_website_1])
        self.assertEqual(parser.mail, self.mail)
        self.assertEqual(parser.phone_number, None)

    def test_get_arguments_without_mail_argument(self):
        parser = self.measure.get_arguments(
            [
                '-u', self.main_website,
                '-l', self.other_website_1,
                '-p', self.phone_number
            ]
        )
        self.assertEqual(parser.url, self.main_website)
        self.assertEqual(parser.list, [self.other_website_1])
        self.assertEqual(parser.mail, None)
        self.assertEqual(parser.phone_number, self.phone_number)

    def test_compare_websites(self):
        self.assertEqual(self.measure.result_data, None)
        websites = [self.other_website_1, self.other_website_2]
        self.measure.compare_websites(self.main_website, websites)
        self.assertEqual(self.main_website, self.measure.main_website.url)
        websites.append(self.main_website)
        for page in self.measure.websites_list:
            self.assertTrue(page.url in websites)
        self.assertNotEqual(self.measure.result_data, None)

    def test_measure_website_load_time(self):
        measure = self.measure.measure_load_time(self.main_website)
        self.assertTrue(isinstance(measure, WebsiteMeasurement))
        self.assertEqual(measure.url, self.main_website)
        self.assertNotEqual(measure.start_time, None)
        self.assertNotEqual(measure.end_time, None)

    def test_measure_not_website_load_time(self):
        try:
            self.measure.measure_load_time('self.main_website')
        except ValueError:
            assert True
        else:
            assert False

    def test_save_to_object(self):
        measure = self.measure.save_to_object(
            self.main_website, time(), time()
        )
        self.assertTrue(isinstance(measure, WebsiteMeasurement))

    def test_prepare_additional_data(self):
        self.assertEqual(self.measure.result_data, None)
        self.measure.prepare_additional_data()
        self.assertNotEqual(self.measure.result_data, None)
        self.assertEqual(type(self.measure.result_data), dict)

    def test_get_comparison_result(self):
        self.measure.main_website.ranking_place = 1
        self.measure.websites_list = [
            self.get_website_object(page) for page in [
                self.other_website_1, self.other_website_2
            ]
        ]
        result = self.measure.get_comparison_result()
        self.assertEqual(
            RESULT_TEMPLATE.format(
                ranking_place=self.measure.main_website.ranking_place,
                websites_number=len(self.measure.websites_list)
            ),
            result
        )

    def test_print_result(self):
        self.measure.websites_list = WebsiteMeasurement.get_sorted_ranking(
            self.measure.websites_list
        )
        self.measure.result_data = {'info_1': 1, 'info_2': 2}
        new_output = io.StringIO()
        sys.stdout = new_output
        self.measure.print_result()
        self.assertTrue(self.other_website_1 in new_output.getvalue())
        self.assertTrue(self.other_website_2 in new_output.getvalue())

    @patch.object(MailSender, 'send_message', create=True)
    def test_not_send_notifications_mail(self, mock):
        self.measure.main_website.ranking_place = 1
        self.measure.send_notifications()
        self.assertFalse(mock.called)

    @patch.object(MailSender, 'send_message', create=True)
    @patch.object(DummySMSSender, 'send_message', create=True)
    def test_send_notifications(self, mock_mail, mock_sms):
        self.measure.main_website.ranking_place = 2
        self.measure.send_notifications()
        self.assertTrue(mock_mail.called)
        self.assertTrue(mock_sms.called)
