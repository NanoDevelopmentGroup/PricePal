"""
Summary:

This module contains helper functions to address and send notifications.
This module will accept all required information for the body or
content of a notification, and will perform actions related to the
configuration and delivery of that content.

Functions:
    send_unformatted_email() : send a simple email with addressee, subject, and body.
    send_formatted_table_email() : send an email both a body and html formatted DataFrame to contain data.

"""

# Imports =============================================================

# Standard Libraries
import logging
import smtplib
import ssl
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Third-party Libraries
import pandas as pd

# Local Application Libraries
import pricepal.common.scrape_engine as scraper
from pricepal.pricepal_utils import root_relative_path

# Constants ===========================================================

SEND_EMAIL_CREDENTIALS = "email_credentials.json"
# This file is a json, including key:value pairs of:
# email : <str> -- email address of the sending email
# pw : <str> -- password for the sending email account
# server : <str> -- the smtp server to be used by sending email account
# port : <int> -- the port number to be used by sending email account

# =====================================================================

#TODO: consider refactoring email functions such that there is a single with overloads.

def send_unformatted_email(subject: str, message: str, receiver_email: str):
    """Sends an email with subject and body to a single or list of addressees.

    This function is dependent on a local email credentials file which contains
    the login credentials and server information of the originating email.
    Consult the constant within notification.py for the conventional formatting
    of this credentials file.

    Arguments:
        subject {str} -- the subject bar of the email
        message {str} -- the body of the email, can contain formatting elements, as well as plaintext
        receiver_email {list, str} -- destination email address(es), can be single or list of strings
    """

    # Create a secure SSL context
    context = ssl.create_default_context()
    logging.debug("Created secure SSL context.")

    # Generate root of relative filepath
    file_location = root_relative_path(SEND_EMAIL_CREDENTIALS)

    # Open and parse sender credentials
    with open(file_location) as credentials_file:
        credentials = json.load(credentials_file)
    logging.debug("Loaded credentials file for outgoing email.")

    # Populate credentials for originating email account and server
    sender_email = credentials["email"]
    password = credentials["pw"]
    sender_email_server = credentials["server"]
    sender_email_port = credentials["port"]

    # Compose email
    email_content = MIMEMultipart()
    email_content["To"] = receiver_email
    email_content["From"] = sender_email
    email_content["Subject"] = subject
    email_content.attach(MIMEText(message, "plain"))

    # Split email to name and address for compatibility with logging, log the name of recipient
    logging.debug("Composed unformatted email to 'to:%s', 'subject:%s'.",
                  receiver_email, subject)

    # Send email
    with smtplib.SMTP_SSL(sender_email_server, sender_email_port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, email_content.as_string())

    logging.info("Sent unformatted email to 'to:%s', 'subject:%s'.",
                 receiver_email, subject)

def send_formatted_table_email(subject: str, message: str, receiver_email: str, data_table: pd.DataFrame):
    """Sends an email with subject, body and formatted data table to a single or list of addressees.
    This can be used to present a table of data (stock, price, otherwise) as well as preceeding paragraph.

    This function is dependent on a local email credentials file which contains
    the login credentials and server information of the originating email.
    Consult the constant within notification.py for the conventional formatting
    of this credentials file.

    Arguments:
        subject {str} -- the subject bar of the email
        message {str} -- the body of the email, can contain formatting elements, as well as plaintext
        receiver_email {list, str} -- destination email address(es), can be single or list of strings
        data_table {pandas.DataFrame} -- data table of data to present, will include row and column headers
    """

    # Create a secure SSL context
    context = ssl.create_default_context()
    logging.debug("Created secure SSL context.")

    # Generate root of relative filepath
    file_location = root_relative_path(SEND_EMAIL_CREDENTIALS)

    # Open and parse sender credentials
    with open(file_location) as credentials_file:
        credentials = json.load(credentials_file)
    logging.debug("Loaded credentials file for outgoing email.")

    # Populate credentials for originating email account and server
    sender_email = credentials["email"]
    password = credentials["pw"]
    sender_email_server = credentials["server"]
    sender_email_port = credentials["port"]

    # Compose email
    email_content = MIMEMultipart()
    email_content["To"] = receiver_email
    email_content["From"] = sender_email
    email_content["Subject"] = subject

    # Add email message at start of the body
    email_content.attach(MIMEText(message+"\n\n", "plain"))

    txt_data_table = scraper.tabulate_dataframe(data_table, "html")
    email_content.attach(MIMEText(txt_data_table, "html"))

    # Split email to name and address for compatibility with logging, log the name of recipient
    logging.debug("Composed formatted table email to 'to:%s', 'subject:%s'.",
                  receiver_email, subject)

    # Send email
    with smtplib.SMTP_SSL(sender_email_server, sender_email_port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, email_content.as_string())

    logging.info("Sent formatted table email to 'to:%s', 'subject:%s'.",
                 receiver_email, subject)
