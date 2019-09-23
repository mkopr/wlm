import os

from website_measure import LOG_DIR_PATH, logger
from website_measure.constants import RESULT_OUTPUT_FILENAME


class WriteFile:
    """
    Write text file in the indicated direction.
    """
    def __init__(self, file_name: str = RESULT_OUTPUT_FILENAME):
        """
        self.file_name - file name of text file wit result data from
        constants.py file.
        self.file_path - path of self.file_name from __init__ file.

        :param file_name: str
        """
        self.file_name = file_name
        self.file_path = os.path.join(LOG_DIR_PATH, self.file_name)
        self.file = None

    def __enter__(self):
        """
        Context manager method.
        Remove old result file from self.file_path directory.

        :return: self
        """
        try:
            os.remove(self.file_path)
        except FileNotFoundError:
            pass
        return self

    def __exit__(self, *args, **kwargs):
        """
        Context manager method.
        Close file.
        """
        self.file.close()

    def append(self, text: str):
        """
        Create and append text file with text data.

        :param text: str
        :return: None
        """
        with open(self.file_path, 'a') as self.file:
            self.file.write(text)
            logger.info(
                f'\n[INFO][WriteFile][append]'
                f'\nAppend file {self.file_name}\nText: {text}'
            )
