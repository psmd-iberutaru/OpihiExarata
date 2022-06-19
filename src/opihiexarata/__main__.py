"""Just a small hook for the main execution. This section parses arguments 
which is then passed to execution to do exactly as expected by the commands.

The actual execution is done in the command.py file so that this file
does not get too large."""

import os

import opihiexarata
import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint

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
    # Parse the arguments.
    parser, arguments = __main_parse_arguments()
    # And executing the arguments.
    __ = __main_execute_arguments(parser=parser, arguments=arguments)


def __main_parse_arguments() -> tuple[hint.ArgumentParser, hint.Namespace]:
    """The main section for argument parsing. We just have it here to better
    organize things.

    Parameters
    ----------
    None

    Returns
    -------
    parser : ArgumentParser
        The parser itself. This may not be needed for a lot of things, but
        it is still helpful for command processing.
    parsed_arguments : Namespace
        The arguments as parsed by the parser. Though technically it is a
        Namespace class, it is practically a dictionary.
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
    # Adding positional arguments.
    parser.add_argument(
        "action",
        nargs="?",
        default="help",
        help=(
            "The primary action to execute. Common actions: `manual` and `automatic`"
            " for the two windows. See documentation for more information."
        ),
    )

    # Adding optional arguments.
    parser.add_argument(
        "-m",
        "--manual",
        action="store_true",
        default=False,
        required=False,
        help=(
            "Invoking this option opens up the manual mode GUI along with the"
            " provided action."
        ),
    )
    parser.add_argument(
        "-a",
        "--auto",
        "--automatic",
        action="store_true",
        default=False,
        required=False,
        help=(
            "Invoking this option opens up the automatic mode GUI along with the"
            " provided action."
        ),
    )
    parser.add_argument(
        "-c",
        "--config",
        "--configuration",
        default=None,
        required=False,
        help=(
            "The OpihiExarata standard configuration file path. If the action is"
            " generate then this is the path where a new default/blank configuration"
            " file will be created."
        ),
    )
    parser.add_argument(
        "-s",
        "--secret",
        "--secrets",
        default=None,
        required=False,
        help=(
            "The OpihiExarata secrets configuration file path. If the action is"
            " generate then this is the path where a new default/blank secrets file"
            " will be created."
        ),
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        default=False,
        required=False,
        help=(
            "For any command line function where file conflicts are possible, then this"
            " flag specifies that files should be overwritten."
        ),
    )
    parser.add_argument(
        "--keep-temporary",
        action="store_true",
        default=False,
        required=False,
        help=(
            "If provided, the temporary directory created is not purged and is instead"
            " kept. This is really something that should only be done for debugging."
        ),
    )

    # Parsing the actual values.
    parsed_arguments = parser.parse_args()
    # All done.
    return parser, parsed_arguments


def __main_execute_arguments(
    parser: hint.ArgumentParser, arguments: hint.Namespace
) -> None:
    """We actually execute the software using the arguments provided in the
    # command line call. GUI's are started on separate threads

    Parameters
    ----------
    arguments : dict
        The parsed arguments from which the interpreted action will use. Note
        though that these arguments also has the interpreted actions.

    Returns
    -------
    None
    """
    # We do not always need the fanciness of the Namespace class. It can often
    # be more harmful than good.
    arguments_dict = vars(arguments)

    # The configurations to be applied, if they exist that is. We structure
    # them so that it is easier for the actions to use them later.
    standard_config_path = arguments_dict.get("config", None)
    secrets_config_path = arguments_dict.get("secret", None)
    if standard_config_path is not None:
        # A configuration file path has been supplied, attempting to load it
        # otherwise the action is likely generate.
        standard_config_path = os.path.abspath(standard_config_path)
        if os.path.isfile(standard_config_path):
            library.config.load_then_apply_configuration(filename=standard_config_path)
    if secrets_config_path is not None:
        # A secrets file path has been supplied, attempting to load it
        # otherwise the action is likely generate.
        secrets_config_path = os.path.abspath(secrets_config_path)
        if os.path.isfile(secrets_config_path):
            library.config.load_then_apply_configuration(filename=secrets_config_path)

    # A lot of the actions require the temporary directory for file handling
    # and other things. We create it here; it is later purged and destroyed
    # unless otherwise flagged.
    __ = library.temporary.create_temporary_directory()

    # The optional second thread actions. These happen independently of the
    # main action and are not freezed because of it.
    pass

    # The primary actions happen on the main thread and because the GUI's stall
    # it on the Python end, we execute these last.

    # We need to figure out what the action is to be for OpihiExarata.
    action = str(arguments_dict.get("action", None)).strip().casefold()

    # From the action, we determine what to do. We add a few shortcuts.
    if action in ("m", "manual"):
        # The manual GUI should be created. Because this it the primary
        # action, it happens on the main thread.
        # Load the window.
        __ = opihiexarata.gui.manual.start_manual_window()
    elif action in ("a", "auto", "automatic"):
        # The automatic GUI should be created. Because this it the primary
        # action, it happens on the main thread.
        # Load the window.
        __ = opihiexarata.gui.automatic.start_automatic_window()
    elif action in ("g", "generate"):
        # Files should be generated, this is normally for configuration and
        # secret file generation. We generate the files, if the paths provided
        # are properly defined.
        overwrite = arguments_dict.get("overwrite", False)
        if standard_config_path is not None:
            library.config.generate_configuration_file_copy(
                filename=standard_config_path, overwrite=overwrite
            )
        if secrets_config_path is not None:
            library.config.generate_secrets_file_copy(
                filename=secrets_config_path, overwrite=overwrite
            )
    elif action in ("h", "help"):
        # We just print the help screen, an action is required but none seems
        # have been provided.
        parser.print_help()
    else:
        raise error.CommandLineError(
            "The action `{act}` specified is not valid. Commonly accepted actions:"
            " manual, automatic, help. See documentation.".format(act=action)
        )

    # Cleaning up the temporary directory, unless the user wanted to keep it.
    keep_temporary = arguments_dict.get("keep_temporary", False)
    if keep_temporary:
        pass
    else:
        __ = library.temporary.purge_temporary_directory()
        __ = library.temporary.delete_temporary_directory()

    # All done.
    return None


if __name__ == "__main__":
    # Executing the actual functionality of this file.
    main()
