"""Test"""

import os

import opihiexarata.library as library
import opihiexarata.asteroid as asteroid
import opihiexarata.astrometry as astrometry
import opihiexarata.gui as gui
import opihiexarata.photometry as photometry

# Load the default configuration parameters. The user's configurations should
# overwrite these when supplied.
_DEFAULT_CONFIG_PATH = os.path.dirname(os.path.realpath(__file__))
library.config.load_then_apply_configuration(
    filename=library.path.merge_pathname(
        directory=_DEFAULT_CONFIG_PATH, filename="configuration", extension="yaml"
    )
)
