# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import datetime
import sphinx_rtd_theme

# For the Python code itself.
sys.path.insert(0, os.path.abspath(os.path.join("..", "..", "src")))


# -- Project information -----------------------------------------------------

project = "OpihiExarata"
copyright = "2022, Kenji Sparrow Emerson"
author = "Kenji Sparrow Emerson"

# The full version, including alpha/beta/rc tags
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


release = get_date_version()


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx_rtd_theme",
]
# Sphinx Napoleon autodoc config.
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True

# We do not include the Python inter-sphinx mapping because native Python
# types should already be known and because the footnote links in the LaTeX
# file, get super out of hand.
intersphinx_mapping = {
    # "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/", None),
    "matplotlib": ("https://matplotlib.org/stable/", None),
    "astropy": ("https://docs.astropy.org/en/stable/", None),
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# Allow for figure numbers.
numfig = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "collapse_navigation": False,
    "sticky_navigation": False,
    "navigation_depth": 5,
}
html_favicon = "./assets/pyukumuku_favicon.png"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


# -- Options for LaTeX output -------------------------------------------------
latex_engine = "lualatex"
latex_show_urls = "footnote"

latex_elements = {
    # Allow for nesting.
    "preamble": r"\usepackage{enumitem}",
    # A little bigger font to be more readable.
    "pointsize": "11pt",
    # Single column index.
    "makeindex": "\\usepackage[columns=1]{idxlayout}\\makeindex",
    # Strict figure placement so things do not get lost.
    "figure_align": "H",
}
