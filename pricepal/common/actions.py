# Definition ==========================================================
#
# Contains helper functions to perform actions of the UI widgets.
# This file's functions should also standalone if necessary, the UI
# only provides a means to call this set of functions.
#
# Imports =============================================================

# Standard Libraries
import logging
import time

# =====================================================================

def test_logging():
    """This function serves to test the various levels of logging and
    the ability of each handler to emit messages.
    This function will remain to assist in sanity testing of logging
    functionality.

    Intended result is four log messages at varied levels, ordered:
    DEBUG, INFO, WARNING, and ERROR. If all logs do not appear in
    your targeted handler, check the configured log level of that
    handler.
    """
    logging.debug('This is a DEBUG-level log.')
    logging.info('This is an INFO-level log.')
    logging.warning('This is a WARNING-level log.')
    logging.error('This is an ERROR-level log.')