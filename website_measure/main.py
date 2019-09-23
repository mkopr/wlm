import argparse
import datetime
import sys
import urllib.request
from time import time
from typing import List

from dotenv import load_dotenv
from website_measure import logger
from website_measure.constants import RESULT_TEMPLATE
from website_measure.mail import MailSender
from website_measure.sms import DummySMSSender
from website_measure.validate import Validate
from website_measure.website import WebsiteMeasurement
from website_measure.write import WriteFile

load_dotenv()


class WebsiteMeasure:
    """
    Main class of website load measure app.
    Ends with context manager = sys.exit().
    """
    def __init__(self):
        """
        self.mail - mail from parsed data
        self.sms - phone number from parsed data
        self.main_website - website url from parsed data
        self.websites_list - website urls from parsed data
        self.result_data - comparision result
        """
        self.mail = None
        self.sms = None
        self.main_website = None
        self.websites_list = None
        self.result_data = None

    def __exit__(self, **kwargs):
        """
        Context manager method.
        End of running.
        """
        sys.exit()

    def run(self) -> None:
        """
        Main method in WebsiteMeasure class.
        Logging to logger start info.
        Gets arguments by get_arguments method and validate
        mail/phone_number if passed.
        Compare loading time of collected websites.
        Send notifications and save results of measurement.

        :return: None
        """
        logger.info(f'\nApplication started!\n{str(sys.argv[1:])}')
        parsed = self.get_arguments(sys.argv[1:])

        if parsed.mail:
            Validate('mail').is_valid(parsed.mail)
            self.mail = parsed.mail

        if parsed.phone_number:
            Validate('phone_number').is_valid(parsed.phone_number)
            self.sms = parsed.phone_number

        self.compare_websites(
            parsed.url, parsed.list
        )
        self.send_notifications()
        self.print_result()
        self.write_result_to_file()

    def get_arguments(self, args: list) -> argparse.Namespace:
        """
        Uses argparse to get data from terminal.
        Defined parser arguments for main website, other websites and
        additional mail address and phone number.
        Default mail address and phone number for notification in .env file.

        usage: wlm [-h] -u URL -l LIST [LIST ...] [-m MAIL] [-p PHONE_NUMBER]
        the following arguments are required: -u/--url, -l/--list

        :param args: list()
        :return: argparse.Namespace
        """
        parser = argparse.ArgumentParser(
            description='App to measure and compare time of loading web pages.'
        )
        parser.add_argument(
            '-u',
            '--url',
            help='URL of main website',
            required=True,
            type=str
        )
        parser.add_argument(
            '-l',
            '--list',
            nargs='+',
            help='URLs of websites to compare',
            required=True
        )
        parser.add_argument(
            '-m',
            '--mail',
            help='mail address for notification',
            required=False,
            type=str,
            default=None
        )
        parser.add_argument(
            '-p',
            '--phone_number',
            help='phone number for notification',
            required=False,
            type=str,
            default=None
        )
        return parser.parse_args(args)

    def compare_websites(
            self, page_one_url: str, pages_urls: List[str]
    ) -> None:
        """
        Measure load time for passed websites and save to object
        attributes.
        Prepare load measure data.

        :param page_one_url: str
        :param pages_urls: str
        :return: None
        """
        self.main_website = self.measure_load_time(page_one_url)
        self.websites_list = [
            self.measure_load_time(page) for page in pages_urls
        ]
        self.prepare_additional_data()

    def measure_load_time(self, url: str) -> WebsiteMeasurement:
        """
        Validate passed url address then try to load website html
        and measure time from start to end.
        Return WebsiteMeasurement with collected data.

        :param url: str
        :return: WebsiteMeasurement
        """
        Validate('url').is_valid(url)
        client = urllib.request.urlopen(url)
        start_time = time()
        client.read()
        end_time = time()
        client.close()
        website = self.save_to_object(url, start_time, end_time)
        return website

    def save_to_object(
            self,
            url: str,
            start_time: time,
            end_time: time
    ) -> WebsiteMeasurement:
        """
        Save measurement data to WebsiteMeasurement dataclass.

        :param url: str
        :param start_time: time
        :param end_time: time
        :return: WebsiteMeasurement
        """
        return WebsiteMeasurement(url, start_time, end_time)

    def prepare_additional_data(self):
        """
        Create result_data dictionary with data about measurements result
        based on sorted and ranked list of WebsiteMeasurement objects.

        :return: None
        """
        self.websites_list.append(self.main_website)
        self.websites_list = WebsiteMeasurement.get_sorted_ranking(
            self.websites_list
        )
        result_data = dict()
        result_data['comparison_result'] = self.get_comparison_result()
        result_data['comparison_date'] = str(datetime.datetime.now())

        self.result_data = result_data

    def get_comparison_result(self) -> str:
        """
        Fill RESULT_TEMPLATE with comparision data.

        :return: str
        """
        return RESULT_TEMPLATE.format(
            ranking_place=self.main_website.ranking_place,
            websites_number=len(self.websites_list)
        )

    def send_notifications(self):
        """
        Send notification via mail and sms if the conditions are met:
            - if the benchmarked website is loaded slower than at least one of
            the competitors - send email message to specified email address.
            - if the benchmarked website is loaded twice as slow as at least
            one of the competitors send SMS message alongside the email message

        SMS notifications mocked with DummySMSSender.

        :return: None
        """
        if self.main_website.ranking_place != 1:
            with MailSender() as mail:
                mail.send_message(
                    self.main_website.ranking_place,
                    len(self.websites_list),
                    self.mail
                )

            for page in self.websites_list:
                if self.main_website.time * 2 >= page.time:
                    # from website_measure.sms import TwilioSMSSender
                    # sms = TwilioSMSSender()
                    sms = DummySMSSender()
                    sms.send_message(
                        self.main_website.ranking_place,
                        len(self.websites_list),
                        self.sms
                    )
                    break

    def write_result_to_file(self):
        """
        Save comparision result with result_data and compared pages to file.

        :return: None
        """
        with WriteFile() as write_file:
            for page in self.websites_list:
                write_file.append(f'{str(page)}\n')
            for k, v in self.result_data.items():
                write_file.append(f'{k}:\t\t{v}\n')

    def print_result(self):
        """
        Print comparision result with result_data and compared pages to
        terminal.
        To change WebsiteMeasurement print format check str method in
        website.py/WebsiteMeasurement.

        :return: None
        """
        for page in self.websites_list:
            print(str(page))
        for k, v in self.result_data.items():
            print(f'{k}:\t\t{v}')
