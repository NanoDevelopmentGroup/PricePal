"""
Summary:

This module contains helper functions to perform requests, scrape and parse data.
This will handle instances/actions associated with price tracking
data collection and cleaning, but will not perform any of the higher
level scheduling and configuring.

Functions:
    request_and_parse() : requests a url of a webpage and returns the BeautifulSoup of the response.
    tabulate_dataframe() : formats a pandas dataframe for display with either text or html formatting.

"""

#TODO: Full error handling within the request_and_parse function.

# Imports =============================================================

# Standard Libraries
import logging

# Third-party Libraries
from tabulate import tabulate
import pandas as pd
from requests import get
from bs4 import BeautifulSoup


# Constants ===========================================================



# =====================================================================

def request_and_parse(url: str, parser: str = "html.parser", output_filename: str = ""):
    """Requests the url passed as an argument, then checks status code and either
    proceeds with parse if deemed to be successful.
    In successful cases, it will return the BeautifulSoup object resulting from
    the response to the request, in failed cases, it will return None.
    Also has the functionality to saved the 'prettify' result to an html file.
    This functionality can be leveraged by supplying an optional output_filename
    argument.

    Arguments:
        url {str} -- the complete url of the webpage to be requested
        parser {str} -- optional, the parser to be used by Beautiful soup, defaults to "html.parser"
        output_filename {str} -- optional, filename to save the resulting html, defaults to "" which will not save result

    Returns:
        {bs4.BeautifulSoup} -- the BeautifulSoup object resulting from the parse of the requested url

    Note: will return None if webpage does not respond with the correct status code.
    """

    # Get the page data from the url and extract its content
    page_response = get(url)

    # If response is 200, request was success and status ok, proceed with parse
    if page_response.status_code == 200:
        logging.debug("Completed request to 'url:%s' with 'response code:%s'. "
                      "Response code is OK. Proceeding with parse.", url, page_response.status_code)
        soup = BeautifulSoup(page_response.content, parser)

    # If response starts with 2, request was a success, but may not be ok
    # Log this unexpected response accordingly, but still proceed with parse
    elif str(page_response.status_code[0]) == "2":
        logging.debug("Completed request to 'url:%s' with 'response code:%s'. "
                      "Response code is unexpected but not critical. Proceeding with parse.", url, page_response.status_code)
        soup = BeautifulSoup(page_response.content, parser)

    # If response starts with 4, request resulted in an error
    # Log this response at warning level and do not proceed with parse
    elif str(page_response.status_code[0]) == "4":
        logging.warning("Completed request to 'url:%s' with 'response code:%s'. "
                        "Response code is critical. Cannot proceed with parse, entering error handling.", url, page_response.status_code)
        return None

    # If response is not caught by the above logic, request was not understood
    # This will be assumed as an error and logged, do not proceed with parse
    else:
        logging.warning("Completed request to 'url:%s' with 'response code:%s'. "
                        "Response code is unclassified, further assessment required. "
                        "Cannot proceed with parse, entering error handling.", url, page_response.status_code)
        return None

    if output_filename != "":
        with open(output_filename+".html", "w") as file:
            file.write(str(soup.prettify()))

    return soup

def tabulate_dataframe(df: pd.DataFrame, table_format: str = "pretty") -> str:
    """Accepts a pandas DataFrame and formats it for viewing as a table.
    The output format can be defined via input arguments, and is capable
    of a variety of html or text formats.

    Arguments:
        df {pandas.DataFrame} -- the DataFrame to format for viewing
        table_format {str} -- format to use for the output of the table, defaults to "pretty",
                              please see the "tabulate" package documentation for more info on
                              the available formatting options

    Returns:
        {str} -- string representation of the table in either html or text formatting

    Notes: using table_format="html" will leverage pandas DataFrame.to_html functionality.
    """

    if table_format == "html":
        table_data = df.to_html(index=False, justify="center")
    else:
        table_data = tabulate(df, headers='keys', tablefmt=table_format, showindex=False, colalign=("left",))
    return table_data
