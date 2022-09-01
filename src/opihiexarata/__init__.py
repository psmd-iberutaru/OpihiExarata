"""All of the subparts of the OpihiExarata software."""

# The library must be imported first as all other parts depend on it.
# Otherwise, a circular loop may occur in the imports.
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
from opihiexarata.opihi import OpihiZeroPointDatabaseSolution

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

# Lastly, the main file. We only do this so that Sphinx correctly builds the
# documentation. (Though this too could be a misunderstanding.) Functionality
# of __main__ should be done via the command line interface.
import __main__ as __
