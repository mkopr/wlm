LOG_FORMAT = '[%(asctime)s]\t%(pathname)s\t%(message)s'

MAIL_SUBJECT = 'notification from Website Load Measure app'
MAIL_TEMPLATE = '''
Your page is {main_website_place} of {all_websites} tested pages.\n
The benchmarked website is loaded slower than at least one of the competitors.
'''

SMS_TEMPLATE = '''
To: {recipient_number}\n
Your page is {main_website_place} of {all_websites} tested pages.
The benchmarked website is loaded twice as slow as at least one of the 
competitors.
'''
RESULT_TEMPLATE = 'Your page is {ranking_place} of {websites_number} tested' \
                  ' pages'
RESULT_OUTPUT_FILENAME = 'log.txt'

REGEX_VALIDATION = {
    'url': {
        'regex': r"^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$",
        'error_message': '[ERROR] invalid URL: {data}'
    },
    'phone_number': {
        'regex': r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{3}|\(\d{3}\)\s*\d{3}["
                 r"-\.\s]??\d{3}|\d{3}[-\.\s]??\d{3})",
        'error_message': '[ERROR] invalid phone number: {data}'
    },
    'mail': {
        'regex': r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""",
        'error_message': '[ERROR] invalid mail address: {data}'
    }
}

ROUND_VALUE = 3  # 0.33333 -> 0.333
