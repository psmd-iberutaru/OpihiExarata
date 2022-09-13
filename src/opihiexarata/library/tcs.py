"""This contains functions which allow for the calling of TCS commands for 
the IRTF telescope control software. It also formats the text according to 
the documentation specifications found in 
http://irtfweb.ifa.hawaii.edu/~tcs3/tcs3/users_manuals/1103_commands.pdf 

These functions call to the external shell and it formats and coverts the 
values from the conventions of OpihiExarata (as the expected input) to the 
expected input for the TCS.
"""

import os
import subprocess
import string


import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint

# Sometimes it is best to limit the user to only use latin characters (ascii)
# because of older software and other conventions.
LATIN_ASCII_CHARACTER_SET = set(
    string.ascii_uppercase + string.ascii_lowercase + string.digits + "-_" + " "
)


def t3io_tcs_next(
    ra: float,
    dec: float,
    ra_proper_motion: float = 0,
    dec_proper_motion: float = 0,
    epoch: int = 2000,
    equinox: int = 2000,
    coordinate_system: str = "fk5",
    target_name: str = None,
    magnitude: float = 0,
    ra_velocity: float = 0,
    dec_velocity: float = 0,
) -> hint.CompletedProcess:
    """This uses the t3io program to execute the TCS next command.
    As the command takes many values, if some "optional" values are not
    provided, they default to 0 when the command is sent if there are no
    otherwise reasonable parameters.

    For more information, see the
    `TCS Manual <http://irtfweb.ifa.hawaii.edu/~tcs3/tcs3/users_manuals/1103_commands.pdf>`_

    Parameters
    ----------
    ra : float
        The right ascension of the target, in degrees.
    dec : float
        The declination of the target, in degrees.
    ra_proper_motion : float, default = 0
        The RA proper motion of the target, in degrees per second.
    dec_proper_motion : float, default = 0
        The DEC proper motion of the target, in degrees per second.
    epoch : int, default = 2000
        The epoch year of the proper motion values to correct for current
        proper motion.
    equinox : int, default = 2000
        The equinox year of the coordinate system.
    coordinate_system : string, default = "fk5"
        The coordinate system which the RA and DEC is using. Must be either
        FK5, FK4, or APP, which is the topocentric apparent coordinate system.
    target_name : string, default = None
        The name of the target. If not provided, it defaults to the
        default name found in the configuration file for TCS requests.
    magnitude : float, default = 0
        The magnitude of the target.
    ra_velocity : float, default = 0
        The non-sidereal motion of the target in RA, in degrees per second.
    dec_velocity : float, default = 0
        The non-sidereal motion of the target in DEC, in degrees per second.

    Returns
    -------
    t3io_response : CompletedProcess
        The response of the t3io command as captured (and packaged) by
        the subprocess module.
    """
    # To use the TCS, we utilize the t3io program. Its location is determined
    # by the configuration file.
    BINARY_PATH = str(library.config.GUI_MANUAL_T3IO_PROGRAM_BINARY_PATH)
    # If the t3io program does not exist, then we cannot send a command to the
    # TCS.
    if not os.path.exists(BINARY_PATH):
        raise error.ConfigurationError(
            "The t3io program does not exist at the path provided in the configuration."
            " This software cannot properly execute TCS commands."
        )
    # The hostname to be used, this matters as sometimes the hostname to be
    # used is the testing TCS hostname.
    TCS_HOST = library.config.GUI_MANUAL_T3IO_TCS_HOSTNAME
    if TCS_HOST is None:
        # The TCS host specified is None, which means that the system should 
        # default to the actual TCS. By default, the TCS command already 
        # does this. A space allows this entry to be passed over when 
        # the command is parsed.
        tcs_host_string = ""
    else:
        tcs_host_string = "-h {h}".format(h=TCS_HOST)

    # The t3io program takes the RA and DECs as sexagesimal.
    ra_sex, deg_sex = library.conversion.degrees_to_sexagesimal_ra_dec(
        ra_deg=ra, dec_deg=dec
    )

    # The proper motion is not currently implemented.
    if ra_proper_motion != 0 or dec_proper_motion != 0:
        raise error.DevelopmentError(
            "Proper motion is not yet implemented for this function."
        )

    # We assume the epoch and equinox passed by the user is correct.
    epoch = int(epoch)
    equinox = int(equinox)

    # There is only three coordinate systems allowed for the TCS, we check
    # that it is one of the three.
    coordinate_system = coordinate_system.casefold()
    if coordinate_system not in ("fk5", "fk4", "app"):
        raise error.InputError(
            "The TCS software only accepts the following coordinate systems: fk5, fk4,"
            " app. See the documentation for more information."
        )

    # We assume the object name is case sensitive. However, spaces must be
    # encoded using percent encoding. We will only accept latin characters
    # as well and encode the space as we go.
    target_name = (
        target_name
        if target_name is not None
        else library.config.GUI_MANUAL_T3IO_DEFAULT_TARGET_NAME
    )
    if set(target_name) <= LATIN_ASCII_CHARACTER_SET:
        # If there are any spaces, we need to re-encode them as %20 as the
        # space is the delimiter for different arguments in the t3io command.
        target_name = target_name.replace(" ", "%20")
    else:
        # There are invalid characters.
        raise error.InputError(
            "There are invalid characters in the target name provided: `{tn}`. The"
            " software only accepts ASCII letters, numbers, and the following symbols:"
            " -_ ".format(tn=target_name)
        )

    # The magnitude of the object.
    magnitude = float(magnitude)

    # The RA and DEC velocities (non-sidereal rates) for the t3io software
    # needs to be in arcseconds per second. By convention we use degrees
    # per second so we need to convert.
    ra_vel_as_s = library.conversion.degrees_per_second_to_arcsec_per_second(
        degree_per_second=ra_velocity
    )
    dec_vel_as_s = library.conversion.degrees_per_second_to_arcsec_per_second(
        degree_per_second=dec_velocity
    )

    # We compile the command to export to the shell for the t3io program.
    # This order is specific to the documentation of the TCS.
    t3io_command_arguments = [
        BINARY_PATH,
        tcs_host_string,
        "Next",
        ra_sex,
        deg_sex,
        ra_proper_motion,
        dec_proper_motion,
        epoch,
        equinox,
        coordinate_system,
        target_name,
        magnitude,
        ra_vel_as_s,
        dec_vel_as_s,
        "opihiexarata",
    ]
    t3io_response = subprocess.run(t3io_command_arguments)
    return t3io_response


def t3io_tcs_ns_rate(ra_velocity: float, dec_velocity: float) -> hint.CompletedProcess:
    """This uses the t3io program to execute the TCS ns.rate command.
    This command allows for the specification of the non-sidereal rates of the
    target.

    For more information, see the
    `TCS Manual <http://irtfweb.ifa.hawaii.edu/~tcs3/tcs3/users_manuals/1103_commands.pdf>`_

    Parameters
    ----------
    ra_velocity : float
        The non-sidereal motion of the target in RA, in degrees per second.
    dec_velocity : float
        The non-sidereal motion of the target in DEC, in degrees per second.

    Returns
    -------
    t3io_response : CompletedProcess
        The response of the t3io command as captured (and packaged) by
        the subprocess module.
    """
    # To use the TCS, we utilize the t3io program. Its location is determined
    # by the configuration file.
    BINARY_PATH = str(library.config.GUI_MANUAL_T3IO_PROGRAM_BINARY_PATH)
    # If the t3io program does not exist, then we cannot send a command to the
    # TCS.
    if not os.path.exists(BINARY_PATH):
        raise error.ConfigurationError(
            "The t3io program does not exist at the path provided in the configuration."
            " This software cannot properly execute TCS commands."
        )
    # The hostname to be used, this matters as sometimes the hostname to be
    # used is the testing TCS hostname.
    TCS_HOST = library.config.GUI_MANUAL_T3IO_TCS_HOSTNAME
    if TCS_HOST is None:
        # The TCS host specified is None, which means that the system should 
        # default to the actual TCS. By default, the TCS command already 
        # does this. A space allows this entry to be passed over when 
        # the command is parsed.
        tcs_host_string = " "
    else:
        tcs_host_string = "-h {h}".format(h=TCS_HOST)

    # The RA and DEC velocities (non-sidereal rates) for the t3io software
    # needs to be in arcseconds per second. By convention we use degrees
    # per second so we need to convert.
    ra_vel_as_s = library.conversion.degrees_per_second_to_arcsec_per_second(
        degree_per_second=ra_velocity
    )
    dec_vel_as_s = library.conversion.degrees_per_second_to_arcsec_per_second(
        degree_per_second=dec_velocity
    )

    # We compile the command to export to the shell for the t3io program.
    # This order is specific to the documentation of the TCS.
    t3io_command_arguments = [
        BINARY_PATH,
        tcs_host_string,
        "NS.rate",
        ra_vel_as_s,
        dec_vel_as_s,
    ]
    t3io_response = subprocess.run(t3io_command_arguments)
    return t3io_response
