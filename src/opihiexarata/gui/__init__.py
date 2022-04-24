"""Parts of the Exarata GUI.
"""

# The relevant GUIs which are to be used when interfacing with the outside
# world.
import opihiexarata.gui.primary as primary
import opihiexarata.gui.selector as selector
import opihiexarata.gui.name as name

# The GUI frameworks. This is only used for very advanced GUIs. Other GUIs
# may not use this and are simple enough to be built manually.
import opihiexarata.gui.qtui as qtui