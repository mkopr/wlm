import unittest
from unittest.mock import patch

from website_measure.write import WriteFile


class TestWriteFile(unittest.TestCase):
    def setUp(self):
        self.write = WriteFile()

    @patch('builtins.open', create=True)
    def test_append(self, mock):
        self.write.append('example')
        self.assertTrue(mock.called)
