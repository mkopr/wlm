import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
from website_measure import logger
from website_measure.constants import MAIL_SUBJECT, MAIL_TEMPLATE

load_dotenv()


class MailSender:
    """
    Connect to server,  prepare and send mail via smtp sever.
    """
    def __init__(
            self,
            smtp_server: str = os.environ.get('SMPT_SERVER'),
            port: int = os.environ.get('SMPT_PORT')
    ):
        """
        self.mail - message sender's mail address from .env file
        self.password - message sender's mail password from .env file
        self.smtp_server - mail server address, example: smtp.outlook.com
        self.port - mail server port, example: 587

        :param smtp_server: str
        :param port: int
        """
        self.mail = os.environ.get('EMAIL')
        self.password = os.environ.get('PASSWORD')
        self.smtp_server = smtp_server
        self.port = port

    def __enter__(self):
        """
        Context manager method.
        Create connection with server and login to it with provided
        credentials after init.

        :return: self
        """
        self.server = smtplib.SMTP(self.smtp_server, self.port)
        self.server.ehlo()
        self.server.starttls()

        try:
            self.server.login(self.mail, self.password)
            logger.info(
                f'\n[INFO][MailSender][__enter__]'
                f'\nLogged with mail {self.mail}'
            )
        except Exception as e:
            logger.error(
                f'\n[ERROR][MailSender][__enter__]'
                f'\nError with mail {self.mail}\n{e}'
            )

        return self

    def __exit__(self, *args, **kwargs):
        """
        Context manager method.
        Close connection with server.
        """
        self.server.quit()

    def prepare_message(
            self,
            main_website_place: int,
            all_websites: int,
            recipient_mail: str
    ) -> str:
        """
        Prepare email message to send with provided data.
        Fill MAIL_TEMPLATE with provided data.

        :param main_website_place: int
        :param all_websites: int
        :param recipient_mail: str
        :return: str
        """
        text = MAIL_TEMPLATE.format(
            main_website_place=main_website_place, all_websites=all_websites
        )
        message = MIMEMultipart()
        message['From'] = self.mail
        message['To'] = recipient_mail
        message['Subject'] = MAIL_SUBJECT
        message.attach(MIMEText(text, 'plain'))
        return message.as_string()

    def send_message(
            self,
            main_website_place: int,
            all_websites: int,
            recipient_mail: str
    ) -> None:
        """
        Send prepared message to recipient_mail email address or address
        from .env file.

        :param main_website_place: int
        :param all_websites: int
        :param recipient_mail: str
        :return: None
        """
        if not recipient_mail:
            recipient_mail = os.environ.get('DEFAULT_RECIPIENT_MAIL_ADDRESS')

        message = self.prepare_message(
            main_website_place, all_websites, recipient_mail
        )
        try:
            self.server.sendmail(self.mail, recipient_mail, message)
            logger.info(
                f'\n[INFO][MailSender][send_message]'
                f'\nEmail to {recipient_mail}\nMessage: {message}'
            )
        except Exception as e:
            logger.info(
                f'\n[ERROR][MailSender][send_message]'
                f'\nEmail to {recipient_mail}\nMessage: {message}\n{e}'
            )
