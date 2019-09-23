import unittest

from website_measure.validate import Validate


class TestValidate(unittest.TestCase):
    def setUp(self):
        self.examples = {
            'mail': [
                ('example@example.pl', True),
                ('example@example', False),
                ('example', False),
                ('123', False)
            ],
            'url': [
                ('https://facebook.pl', True),
                ('facebook.pl', True),
                ('m.facebook.pl', True),
                ('127.0.0.1:8080', True),
                ('www', False),
                ('123123', False),
            ],
            'phone_number': [
                ('123123123', True),
                ('123-123-123', True),
                ('123 123 123', True),
                ('123.123.123', True),
                ('https://facebook.pl', False),
                ('abcd', False),
            ]
        }

    def test_validate(self):
        for data_type in self.examples:
            validate = Validate(data_type)
            for example in self.examples[data_type]:
                try:
                    self.assertEqual(validate.is_valid(example[0]), example[1])
                except ValueError:
                    self.assertFalse(example[1])
