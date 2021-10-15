"""Controls the inputting of configuration files. This also serves to bring all 
of the configuration parameters into a more accessable space which other parts 
of Exarata can use.

Note these configuration constant parameters are all accessed using capital 
letters regardless of the configuration file's labels.
"""

import os
import yaml

import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.typehints as hint



def load_configuration_file(filename: str) -> dict:
    """Loads a configuration file and outputs a dictionary of parameters.

    Note configuration files should be flat, there should be no nested
    configuration parameters.

    Parameters
    ----------
    filename : string
        The filename of the configuration file, with the extension. Will raise
        if the filename is not the correct extension, just as a quick check.

    Returns
    -------
    configuration_dict : dictionary
        The dictionary which contains all of the configuration parameters
        within it.
    """
    # Checking the extension is valid, just as a quick sanity check that the
    # configuration file is proper.
    config_extension = "yaml"
    filename_ext = library.path.get_file_extension(pathname=filename)
    if config_extension != filename_ext:
        raise error.FileError(
            "Configuration file does not have the proper extension it should be a yaml"
            " file."
        )
    # Loading the configuration file.
    with open(filename, "r") as config_file:
        configuration_dict = dict(yaml.load(config_file, Loader=yaml.SafeLoader))
    # Double check that the configuration is flat as per the documentation
    # and expectation.
    for __, valuedex in configuration_dict.items():
        if isinstance(valuedex, dict):
            # A dictionary implies a nested configuration which is not allowed.
            raise error.ConfigurationError(
                "The configuration file should not have any embedded configurations, it"
                " should be a flat file. Please use the configuration file templates."
            )
    # The configuration dictionary should be good.
    return configuration_dict


def load_then_apply_configuration(filename: str) -> None:
    """Loads a configuration file, then applies it to the entire Exarata system.

    Loads a configuration file and overwrites any overlapping
    configurations. It writes the configuration to the configuration module
    for usage throughout the entire program.

    Note configuration files should be flat, there should be no nested
    configuration parameters.

    Parameters
    ----------
    filename : string
        The filename of the configuration file, with the extension. Will raise
        if the filename is not the correct extension, just as a quick check.

    Returns
    -------
    None
    """

    # Load the configuration dictionary.
    configuration = load_configuration_file(filename=filename)
    # Applying the configurations to this module's global namespace is the
    # preferred method of applying the configuration. As these configurations
    # will not change, they are constant like and thus can be accessed in a
    # more Pythonic manner.

    # Constants typically are all capitalized in their variable naming.
    configuration = {
        keydex.upper(): valuedex for keydex, valuedex in configuration.items()
    }
    # Applying it to the global space of this module only.
    globals().update(configuration)
    return None

