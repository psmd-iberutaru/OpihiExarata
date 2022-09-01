"""The installing script for this software. This is if you want to install it
and run it from your PATH."""

import datetime
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

DEPENDENCIES = [
    "astropy",
    "numpy",
    "pyyaml",
    "pillow",
    "PySide6",
    "requests",
    "scipy",
    "matplotlib",
    "plotly",
    "pandas",
]


###############################################################################
###############################################################################


def get_date_version() -> str:
    """The version of the project.

    Returns the project's version using date notation, rather than version
    numbering. There is no expectation for anything but the most recent
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
        day=current_datatime.day,
    )
    return version_string


DATE_VERSION = get_date_version()


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
        "Bug Tracker": BUG_URL,
        "Documentation": DOCUMENTATION_URL,
        "Source Code": SOURCE_URL,
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    package_data={"": ["*.yaml", "*.ui", "*.png"]},
    packages=setuptools.find_packages(where="src"),
    install_requires=DEPENDENCIES,
    python_requires=">=3.9",
    entry_points={"console_scripts": ["opihiexarata=opihiexarata:__main__.main"]},
)
