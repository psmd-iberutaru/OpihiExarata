"""All of the subparts of the OpihiExarata software."""

# The library must be imported first as all other parts depend on it.
import opihiexarata.library as library

# The main parts of the package themselves.
import opihiexarata.astrometry as astrometry
import opihiexarata.ephemeris as ephemeris
import opihiexarata.orbit as orbit
import opihiexarata.photometry as photometry
import opihiexarata.propagate as propagate

# The section for the user interface.
import opihiexarata.gui as gui


# The primary collective solutions for OpihiExarata.
import opihiexarata.opihi as opihi
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
