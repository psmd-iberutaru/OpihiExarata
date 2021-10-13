"""The installing script for this software. This is if you want to install it
and run it from your PATH."""

import datetime
from types import GetSetDescriptorType
import setuptools

NAME = "OpihiExarata"
AUTHOR = "Sparrow"
AUTHOR_EMAIL = "psmd.iberutaru@gmail.com"
SHORT_DESCRIPTION = "Analysis software for the IRTF Opihi telescope."

KEYWORDS = []
URL = "https://github.com/psmd-iberutaru/OpihiExarata"
BUG_URL = "https://github.com/psmd-iberutaru/OpihiExarata/issues"
DOCUMENTATION_URL = "https://github.com/psmd-iberutaru/OpihiExarata"
SOURCE_URL = "https://github.com/psmd-iberutaru/OpihiExarata"




###############################################################################
###############################################################################


def get_date_version() -> str:
    """The version of the project.
    
    Returns the project's version using date notation, rather than version
    numbering. There is not expectation for anything but the most recent 
    version to be used anyways.
    
    Parameters
    ----------
    None

    Returns
    -------
    date_version : string
        The version of this project, as a date.
    """
    current_datatime = datetime.datetime.now()
    version_string = "{year}.{month}.{day}".format(
        year=current_datatime.year, 
        month=current_datatime.month, 
        day=current_datatime.day)
    return version_string
DATE_VERSION = get_date_version()

def get_dependencies() -> list:
    """Obtains the requirements for this project.
    
    This reads the local requirements.txt file and extracts the dependencies 
    from it to be used to the setuptools pipeline.

    Parameters
    ----------
    None

    Returns
    -------
    dependencies : list
        The list of package dependencies for this project.
    """
    with open("requirements.txt", "r", encoding="utf-8") as file:
        requirements_file = file.read()
        dependencies = requirements_file.split("\n")
    return dependencies
DEPENDENCIES = get_dependencies()

with open("README.md", "r", encoding="utf-8") as file:
    README_FILE = file.read()

setuptools.setup(
    name=NAME,
    version=DATE_VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=SHORT_DESCRIPTION,
    long_description=README_FILE,
    long_description_content_type="text/markdown",
    url=URL,
    project_urls={
        "Bug Tracker":BUG_URL,
        "Documentation":DOCUMENTATION_URL,
        "Source Code":SOURCE_URL,
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires = DEPENDENCIES,
    python_requires=">=3.6",
)


