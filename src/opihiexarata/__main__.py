"""Just a small hook for the main execution. This section parses arguments 
which is then passed to execution to do exactly as expected by the commands.

The actual execution is done in the command.py file so that this file
does not get too large."""

import opihiexarata

import argparse

def main() -> None:
    """The main command for argument parsing and figuring out what to do based
    on command-line entries.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """

    # General description.
    parser = argparse.ArgumentParser(
        description=(
            "This is the command-line interface for OpihiExarata. Use"
            " `opihiexarata --help` for help on the available arguments."
            " This command-line interface really is only build to start"
            " the GUIs and other auxiliary functions."
        )
    )
    # Adding arguments.
    parser.add_argument("-m", "--manual", action="store_true", default=False,  required=False, help="Invoking this option opens up the manual/primary mode GUI.")
    parser.add_argument("-a","--auto", "--automatic", action="store_true", default=False, required=False, help="Invoking this option opens up the automatic mode GUI.")


    # Parsing the actual values.
    parser.parse_args()


if __name__ == "__main__":
    main()
