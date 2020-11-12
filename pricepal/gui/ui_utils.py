# Imports =============================================================

# Standard Libraries
import os

# Third-party Libraries
from PyQt5 import uic

# =====================================================================

def find_form(form_name: str) -> str:
    """This function serves as a directory search for ui files within
    the gui module of AutoGraph. It will search the co-located ui
    files and return the absolute path for loading or other
    manipulation. It has been off-loaded from the main form to allow
    for extensibility in its use. No exceptions are raised within
    as these are already handled gracefully when opening the file.

    Arguments:
        form_name {str} -- The name of the ui file including '.ui' suffix

    Returns:
        str -- The complete, rooted path to the ui file
    """
    ui_path = os.path.dirname(os.path.abspath(__file__))
    ui_path += "/" + form_name
    return ui_path
