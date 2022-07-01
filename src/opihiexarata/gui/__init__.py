"""Parts of the Exarata GUI.
"""

# The relevant GUIs which are to be used when interfacing with the outside
# world.
# Automatic mode related GUIs.
import opihiexarata.gui.automatic as automatic

# Manual mode related GUIs.
import opihiexarata.gui.manual as manual
import opihiexarata.gui.selector as selector
import opihiexarata.gui.name as name

# Helpful functions.
import opihiexarata.gui.functions as functions

# The GUI frameworks. This is only used for very advanced GUIs. Other GUIs
# may not use this and are simple enough to be built manually.
import opihiexarata.gui.qtui as qtui
