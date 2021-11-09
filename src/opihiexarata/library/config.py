"""Controls the inputting of configuration files. This also serves to bring all 
of the configuration parameters into a more accessable space which other parts 
of Exarata can use.

Note these configuration constant parameters are all accessed using capital 
letters regardless of the configuration file's labels. Moreover, there are 
constant parameters which are stored here which are not otherwise changeable
by the configuration file.
"""

import os
import yaml
import shutil

import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint


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
    config_extension = ("yaml", "yml")
    filename_ext = library.path.get_file_extension(pathname=filename)
    if filename_ext not in config_extension:
        raise error.FileError(
            "Configuration file does not have the proper extension it should be a yaml"
            " file."
        )
    # Loading the configuration file.
    try:
        with open(filename, "r") as config_file:
            configuration_dict = dict(yaml.load(config_file, Loader=yaml.SafeLoader))
    except FileNotFoundError:
        # This is an error that is specific to OpihiExarata.
        raise error.FileError(
            "The following configuration filename does not exist: \n {fname}".format(
                fname=filename
            )
        )
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


def generate_configuration_file_copy(filename: str, overwrite=False) -> None:
    """This generates a copy of the default configuration file to the given
    location.

    Parameters
    ----------
    filename : string
        The pathname or filename where the configuration file should be put
        to. If it does not have the proper yaml extension, it will be added.
    overwrite : bool, default = False
        If the file already exists, overwrite it. If False, it would raise
        an error instead.

    Returns
    -------
    None
    """
    # Check if the filename is already taken by something.
    if os.path.isfile(filename) and (not overwrite):
        raise error.FileError(
            "Filename already exists, overwrite is False: \n {fname}".format(
                fname=filename
            )
        )
    # If the user did not provide a filename with the proper extension, add it.
    user_ext = library.path.get_file_extension(pathname=filename)
    yaml_extensions = ("yaml", "yml")
    preferred_yaml_extension = yaml_extensions[0]
    if user_ext not in yaml_extensions:
        file_destination = library.path.merge_pathname(
            filename=filename, extension=preferred_yaml_extension
        )
    else:
        # Nothing needs to be done. The filename is fine.
        file_destination = filename

    # Copy the file over from the default location within this install.
    default_config_path = library.path.merge_pathname(
        directory=library.config.MODULE_INSTALLATION_PATH,
        filename="configuration",
        extension="yaml",
    )
    shutil.copyfile(default_config_path, file_destination)
    return None


def generate_secrets_file_copy(filename: str, overwrite=False) -> None:
    """This generates a copy of the secrets configuration file to the given
    location.

    Parameters
    ----------
    filename : string
        The pathname or filename where the configuration file should be put
        to. If it does not have the proper yaml extension, it will be added.
    overwrite : bool, default = False
        If the file already exists, overwrite it. If False, it would raise
        an error instead.

    Returns
    -------
    None
    """
    # Check if the filename is already taken by something.
    if os.path.isfile(filename) and (not overwrite):
        raise error.FileError(
            "Filename already exists, overwrite is False: \n {fname}".format(
                fname=filename
            )
        )
    # If the user did not provide a filename with the proper extension, add it.
    user_ext = library.path.get_file_extension(pathname=filename)
    yaml_extensions = ("yaml", "yml")
    preferred_yaml_extension = yaml_extensions[0]
    if user_ext not in yaml_extensions:
        file_destination = library.path.merge_pathname(
            filename=filename, extension=preferred_yaml_extension
        )
    else:
        # Nothing needs to be done. The filename is fine.
        file_destination = filename

    # Copy the file over from the default location within this install.
    default_config_path = library.path.merge_pathname(
        directory=library.config.MODULE_INSTALLATION_PATH,
        filename="secrets",
        extension="yaml",
    )
    shutil.copyfile(default_config_path, file_destination)
    return None


# Configuration/constant parameters which are otherwise not usually provided
# or must be provided at runtime with code.
###################

# The default path which this module is installed in. It is one higher than
# this file which is within the library module of the OpihiExarata install.
MODULE_INSTALLATION_PATH = os.path.dirname(
    os.path.realpath(os.path.join(os.path.realpath(__file__), ".."))
)
