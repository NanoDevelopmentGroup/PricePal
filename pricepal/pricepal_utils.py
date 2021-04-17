# Imports =============================================================

# Standard Libraries
import inspect
import os

# Constants ===========================================================

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
GUI_DIR = os.path.join(PROJECT_DIR, "gui")
UNIT_TEST_DIR = os.path.join(PROJECT_DIR, "tests")
DATA_DIR = os.path.normpath(os.path.join(PROJECT_DIR, "..", "data"))

# =====================================================================

def root_relative_path(file_name: str) -> str:
    """Generates the rooted, absolute path to the calling file
    then concatenates the supplied filename. This function should
    be used to open files with known locations relative to the
    calling file, for example, in the same directory.
    No exceptions are raised within this function as these are
    handled gracefully during the attempted opening of the file.

    Arguments:
        file_name {str} -- the filename or relative filepath to a file from the calling file

    Returns:
        {str} -- the complete, rooted path to the file, concatenating rooted path with file_name
    """

    rooted_path = os.path.dirname(inspect.stack()[1].filename)
    total_path = os.path.join(rooted_path, file_name)
    return total_path
