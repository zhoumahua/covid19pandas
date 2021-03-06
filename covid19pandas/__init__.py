#   Copyright 2018 Samuel Payne sam_payne@byu.edu
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#       http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
Get COVID-19 data as pandas dataframes in just one function call. Built-in plotting functions. Tutorials in our docs.

To get help on functions for getting data tables, exit the current help dialog and run 'help(covid19pandas.getters)'.

To get help on functions for manipulating data tables, exit the current help dialog and run 'help(covid19pandas.selectors)'.

To get help on functions for plotting data, exit the current help dialog and run 'help(covid19pandas.plotters)'.

See also our tutorials at <https://github.com/PayneLab/covid19pandas/tree/master/docs>.
"""

import pandas as pd
import os
import sys
import warnings

from .getters import *
from .selectors import *
from .plotters import *
from .download import download_text as _download_text
from .exceptions import PackageError, NoInternetError, PackageWarning, OldPackageVersionWarning

def version():
    """Return version number of the package."""
    version = {}
    path_here = os.path.abspath(os.path.dirname(__file__))
    version_path = os.path.join(path_here, "version.py")
    with open(version_path) as fp:
        exec(fp.read(), version)
    return(version['__version__'])

# Helper functions for handling exceptions and warnings
def _exception_handler(exception_type, exception, traceback, default_hook=sys.excepthook): # Because Python binds default arguments when the function is defined, default_hook's default will always refer to the original sys.excepthook
    """Catch exceptions raised by our package, and make them prettier."""
    if issubclass(type(exception), PackageError):
        print(f"Error: {str(exception)} ({traceback.tb_frame.f_code.co_filename}, line {traceback.tb_lineno})", file=sys.stderr) # We still send to stderr
    else:
        default_hook(exception_type, exception, traceback) # This way, exceptions from other packages will still be treated the same way

def _warning_displayer(message, category, filename, lineno, file=None, line=None, default_displayer=warnings.showwarning): # Python binds default arguments when the function is defined, so default_displayer's default will always refer to the original warnings.showwarning
    """Catch warnings generated by our package and make them prettier."""
    if issubclass(category, PackageWarning):
        print(f"Warning: {str(message)} ({filename}, line {lineno})", file=sys.stderr) # We still send to stderr
    else:
        default_displayer(message, category, filename, lineno, file, line) # This way, warnings from other packages will still be displayed the same way

sys.excepthook = _exception_handler # Set our custom exception hook
warnings.showwarning = _warning_displayer # And our custom warning displayer

# Check whether the package is up-to-date
VERSION_URL = "https://byu.box.com/shared/static/kkkun3iz1quiwwz4dmedm8fhu8qjuuiu.txt"

try:
    REMOTE_VERSION = _download_text(VERSION_URL)
except NoInternetError:
    pass
else:
    LOCAL_VERSION = version()
    if REMOTE_VERSION != LOCAL_VERSION:
        warnings.warn(f"Your version of covid19pandas ({LOCAL_VERSION}) is out-of-date. Latest is {REMOTE_VERSION}. Please run 'pip install --upgrade covid19pandas' to update it.", OldPackageVersionWarning, stacklevel=2)

# Make sure the data storage directories have been created
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(PATH_HERE, "data")
JHU_DIR = os.path.join(DATA_DIR, "jhu")
NYT_DIR = os.path.join(DATA_DIR, "nyt")

if not os.path.isdir(DATA_DIR):
    os.mkdir(DATA_DIR)
if not os.path.isdir(JHU_DIR):
    os.mkdir(JHU_DIR)
if not os.path.isdir(NYT_DIR):
    os.mkdir(NYT_DIR)
