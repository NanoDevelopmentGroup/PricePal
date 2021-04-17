# Unit Test ==========================================================
#
# Testing for the scraping functionality. These tests will
# exercise functionality of the scrape_engine module.
# Contains helper functions to perform requests, scrape and parse data.
# This will handle instances/actions associated with price tracking
# data collection and cleaning, but will not perform any of the higher
# level scheduling and configuring.
#
# Imports =============================================================

import json

# Local Application Libraries
import pricepal.common.scrape_engine as scraper
from pricepal.common.status_logger import init_test_logging
from pricepal.pricepal_utils import root_relative_path

# Constants ===========================================================

SCRAPE_TEST_CASES = "test_scrape_engine_cases.json"
# This file is a json, including key:value pairs of:
# test_case_N : <str> -- the website url to request during test
# response_case_N : <str, html> -- optional html payload to compare test response against

# =====================================================================

# Initialize standard logging for recording of unit test operation/results
init_test_logging()

# Load address used to receive test emails from a local file
file_location = root_relative_path(SCRAPE_TEST_CASES)

with open(file_location) as scrape_test_cases_file:
    scrape_test_cases = json.load(scrape_test_cases_file)

scraper.request_and_parse(scrape_test_cases["test_case_1"])
