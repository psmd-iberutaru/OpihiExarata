"""All of the subparts of the OpihiExarata software."""

# The library must be imported first as all other parts depend on it.
# Otherwise, a circular loop may occur in the imports.
# The main parts of the package themselves.
from opihiexarata import astrometry
from opihiexarata import ephemeris

# The section for the user interface.
from opihiexarata import gui
from opihiexarata import library

# The primary collective solutions for OpihiExarata.
from opihiexarata import opihi
from opihiexarata import orbit
from opihiexarata import photometry
from opihiexarata import propagate
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
    ),
)
library.config.load_then_apply_configuration(
    filename=library.path.merge_pathname(
        directory=library.config.MODULE_INSTALLATION_PATH,
        filename="secrets",
        extension="yaml",
    ),
)

# Lastly, the main file. We only do this so that Sphinx correctly builds the
# documentation. (Though this too could be a misunderstanding.) Functionality
# of __main__ should be done via the command line interface.
import __main__ as __
