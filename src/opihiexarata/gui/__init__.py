"""Parts of the Exarata GUI."""

# The relevant GUIs which are to be used when interfacing with the outside
# world.
# Automatic mode related GUIs.
from opihiexarata.gui import automatic

# Helpful functions.
from opihiexarata.gui import functions

# Manual mode related GUIs.
from opihiexarata.gui import manual
from opihiexarata.gui import name

# The GUI frameworks. This is only used for very advanced GUIs. Other GUIs
# may not use this and are simple enough to be built manually.
from opihiexarata.gui import qtui
from opihiexarata.gui import selector
