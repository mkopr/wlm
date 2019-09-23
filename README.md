# wlm - Website Load Measure
*Benchmark loading time of the website in comparison to the other
websites (check how fast is the website's loading time in comparison to
other competitors).*

[toc]

# setup
```
$ git clone git@github.com:mkopr/wlm.git
$ cd wlm
$ pip install -e .
$ touch .env
Add enviroment variables - check bellow
$ wlm 
```
```
usage: wlm [-h] -u URL -l LIST [LIST ...] [-m MAIL] [-p PHONE_NUMBER]
        the following arguments are required: -u/--url, -l/--list
```
Require python>=3.7  
Service logs in file `logs/wlm_RRRR_MM_DD.log`  
Result data in file `logs/log.txt`

# environment variables
set environment variables in `.env` file.  

Example:
```
SMPT_SERVER=smtp.outlook.com
SMPT_PORT=587
EMAIL=mail@outlook.com
PASSWORD=password
DEFAULT_RECIPIENT_MAIL_ADDRESS=mail@gmail.com

TWILIO_ACCOUNT_ID=123123123
TWILIO_TOKEN=123123123
TWILIO_SENDER_NUMBER=123123123
DEFAULT_RECIPIENT_PHONE_NUMBER=123123123
```

# example of use
command: 
``` 
$ wlm -u https://stackoverflow.com/questions/ -l
https://facebook.com https://wp.pl https://onet.pl -p 123123123 -m
marcinkoprek@gmail.com
```  
output
``` 
############## Dummy sms ##############

To: 123123123

Your page is 4 of 4 tested pages.
The benchmarked website is loaded twice as slow as at least one of the 
competitors.

#######################################
|1. 	| time: 0.061 	| url: https://facebook.com
|2. 	| time: 0.09 	| url: https://onet.pl
|3. 	| time: 0.212 	| url: https://wp.pl
|4. 	| time: 0.513 	| url: https://stackoverflow.com/questions/
comparison_result:		Your page is 4 of 4 tested pages
comparison_date:		2019-09-23 21:33:04.060560
```

# chosen third-party libraries
python-dotenv - to handle environment variables from .env file;  
twlilio - sms provider

# tests
```
$ python -m unittest discover
```

# logging
change logging direction, filename in `website_measure/__init__.py`

# constants
change message template, regex strings, result file name in
`website_measure/constants.py`
