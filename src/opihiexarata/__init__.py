"""All of the subparts of the OpihiExarata software."""


import opihiexarata.astrometry as astrometry
import opihiexarata.ephemeris as ephemeris
import opihiexarata.opihi as opihi
import opihiexarata.orbit as orbit
import opihiexarata.photometry as photometry
import opihiexarata.propagate as propagate

import opihiexarata.library as library
import opihiexarata.gui as gui

# The primary solutions for OpihiExarata.
from opihiexarata.opihi import OpihiPreprocessSolution
from opihiexarata.opihi import OpihiSolution

# Load the default configuration parameters. The user's configurations should
# overwrite these when supplied.
library.config.load_then_apply_configuration(
    filename=library.path.merge_pathname(
        directory=library.config.MODULE_INSTALLATION_PATH,
        filename="configuration",
        extension="yaml",
    )
)
library.config.load_then_apply_configuration(
    filename=library.path.merge_pathname(
        directory=library.config.MODULE_INSTALLATION_PATH,
        filename="secrets",
        extension="yaml",
    )
)
