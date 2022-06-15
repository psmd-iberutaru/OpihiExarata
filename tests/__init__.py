import os
import sys
import inspect

# We must use the local version rather than some installed version.
opihiexarata_local_path = "../../src/"
file_absolute_path = os.path.abspath(inspect.getsourcefile(lambda: 0))
opihiexarata_abs_path = os.path.abspath(
    os.path.join(file_absolute_path, opihiexarata_local_path)
)
print(opihiexarata_abs_path)
sys.path.append(opihiexarata_abs_path)
import opihiexarata
