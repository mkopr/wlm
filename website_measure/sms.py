import os

from twilio.rest import Client
from website_measure import logger
from website_measure.constants import SMS_TEMPLATE


class TwilioSMSSender:
    """
    Connect to provider, prepare and send sms via twilio.
    """
    def __init__(
            self,
            account_id: str = os.environ.get('TWILIO_ACCOUNT_ID'),
            token: str = os.environ.get('TWILION_TOKEN')
    ):
        """
        self.account_id - Twilio account ID from .env file
        self.token - Twilion account token from .env file

        :param account_id:  str
        :param token: str
        """
        self.account_id = account_id
        self.token = token

    def __enter__(self):
        """
        Context manager method.
        Create connection with server and login to it with provided
        credentials after init.

        :return: self
        """
        self.client = Client(self.account_id, self.token)
        return self

    def send_message(
            self,
            main_website_place: int,
            all_websites: int,
            recipient_number: str
    ) -> None:
        """
        Fill SMS_TEMPLATE with provided data.
        Send sms message to recipient_number phone number or phone number
        from .env file.

        :param main_website_place: int
        :param all_websites: int
        :param recipient_number: str
        :return: None
        """
        if not recipient_number:
            recipient_number = os.environ.get('DEFAULT_RECIPIENT_PHONE_NUMBER')

        text = SMS_TEMPLATE.format(
            main_website_place=main_website_place, all_websites=all_websites
        )
        try:
            message = self.client.messages.create(
                body=text,
                from_=os.environ.get('mail_template'),
                to=recipient_number
            )
            logger.info(
                f'\n[INFO][TwilioSMSSender][send_message]'
                f'\n{message.sid}')
        except Exception as e:
            logger.info(f'\n[ERROR][TwilioSMSSender][send_message]\n{e}')


class DummySMSSender:
    """
    Dummy implementation for sms sender without credentials.
    """
    def send_message(
            self,
            main_website_place: int,
            all_websites: int,
            recipient_number: str
    ) -> None:
        """
        Fill SMS_TEMPLATE with provided data.
        Print sms message with recipient_number phone number or phone number
        from .env file.

        :param main_website_place: int
        :param all_websites: int
        :param recipient_number: str
        :return: None
        """
        if not recipient_number:
            recipient_number = os.environ.get('DEFAULT_RECIPIENT_PHONE_NUMBER')

        text = SMS_TEMPLATE.format(
            main_website_place=main_website_place,
            all_websites=all_websites,
            recipient_number=recipient_number
        )
        print('############## Dummy sms ##############')
        print(text)
        print('#######################################')
        logger.info(
            f'\n[INFO][DummySMSSender][send_message]'
            f'\nSMS message: {text}'
        )
