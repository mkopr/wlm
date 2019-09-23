import re

from website_measure import logger
from website_measure.constants import REGEX_VALIDATION


class Validate:
    """
    Validate input data with regex.
    """
    def __init__(self, data_type: str):
        """
        self.regex_string - regex string from REGEX_VALIDATION dictionary
        self.error_message - error message from REGEX_VALIDATION dictionary

        Update REGEX_VALIDATION dict in constants.py to use different regex
        strings, error messages of validate different types of data.

        :param data_type: str
        """
        try:
            self.regex_string = REGEX_VALIDATION[data_type]['regex']
            self.error_message = REGEX_VALIDATION[data_type]['error_message']
        except KeyError:
            logger.error(
                '\n[ERROR][__init__]'
                '\nNo data in REGEX_VALIDATION dict'
            )
            raise KeyError

    def is_valid(self, data: str, ) -> bool:
        """
        Use provided with type regex string to check data.
        Raise ValueError if not.

        :param data: str
        :return: bool
        """
        regex = re.compile(self.regex_string, re.IGNORECASE)
        if not regex.search(data):
            logger.error(self.error_message.format(data=data))
            raise ValueError
        return True
