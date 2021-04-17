# Unit Test ==========================================================
#
# Testing for the notification functionality. These tests will
# exercise functionality of the notification module.
# This module will accept all required information for the body or
# content of a notification, and will perform actions related to the
# configuration and delivery of that content.
#
# Imports =============================================================

# Standard Libraries
import json

# Third-party Libraries
import pandas as pd

# Local Application Libraries
import pricepal.notification.notification as notif
from pricepal.common.status_logger import init_test_logging
from pricepal.pricepal_utils import root_relative_path

# Constants ===========================================================

RECEIVER_EMAIL_INFO = "receiver_email.json"
# This file is a barebones json, including one key:value pair being:
# email : <str> -- email address(es) which will receive the test email(s)

# =====================================================================

# Initialize standard logging for recording of unit test operation/results
init_test_logging()

# Load address used to receive test emails from a local file
file_location = root_relative_path(RECEIVER_EMAIL_INFO)

with open(file_location) as receiver_email_file:
    receiver_email = json.load(receiver_email_file)


notif.send_unformatted_email("This is a test subject.", "This is a test message.",
                             receiver_email["email"])

sample_df = pd.DataFrame({'location' : ['ottawa', 'cambridge', 'waterloo'],
                          'stock' : ['1', '5+', '-']})

notif.send_formatted_table_email("This is a test table subject.", "This is the header to a table message.",
                                 receiver_email["email"], sample_df)
