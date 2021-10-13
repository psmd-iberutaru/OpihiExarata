"""Tests pathname manipulations."""
import sys

import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.typehints as hint

# The operating system that is running, if it is Windows, the tests for
# pathnames are different.
IS_OPERATING_SYSTEM_WINDOWS = sys.platform.startswith("win")


def test_get_directory() -> None:
    """Test the ability to get the directory from a pathname.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    if IS_OPERATING_SYSTEM_WINDOWS:
        # Example of a Windows OS pathname with spaces and other intresting
        # characters.
        example_windows_pathname = (
            R"A:\Kalos\Music\Pokémon\Official Tracks\Mystery Dungeon\PMD"
            R" Explorers\Dialga's Fight to the Finish!.flac"
        )
        # Getting the directory.
        directory = library.path.get_directory(pathname=example_windows_pathname)
        expected_dir = (
            R"A:\Kalos\Music\Pokémon\Official Tracks\Mystery Dungeon\PMD Explorers"
        )
        # Asserting.
        assert_message = "Windows based pathnames fail."
        assert directory == expected_dir, assert_message
    else:
        # Example of a Linux OS pathname with spaces and other intresting
        # characters.
        example_linux_pathname = (
            R"/home/sparrow/Kirby/星のカービィ (Hoshi no Kaabii) (2001) -  Episode 1 - Kirby"
            R" - Right Back at Ya! Japanese [a9vrQ3Ns0gg].mkv"
        )
        # Getting the directory.
        directory = library.path.get_directory(pathname=example_linux_pathname)
        expected_dir = R"/home/sparrow/Kirby"
        # Asserting.
        assert_message = "Linux based pathnames fail."
        assert directory == expected_dir, assert_message

    return None


def test_get_filename_without_extension() -> None:
    """Test the ability to get the filename without extension from a pathname.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    if IS_OPERATING_SYSTEM_WINDOWS:
        # Example of a Windows OS pathname with spaces and other intresting
        # characters.
        example_windows_pathname = (
            R"A:\Kalos\Music\Pokémon\Official Tracks\Mystery Dungeon\PMD"
            R" Explorers\Dialga's Fight to the Finish!.flac"
        )
        # Getting the directory.
        filename = library.path.get_filename_without_extension(
            pathname=example_windows_pathname
        )
        expected_filename = R"Dialga's Fight to the Finish!"
        # Asserting.
        assert_message = "Windows based pathnames fail."
        assert filename == expected_filename, assert_message
    else:
        # Example of a Linux OS pathname with spaces and other intresting
        # characters.
        example_linux_pathname = (
            R"/home/sparrow/Kirby/星のカービィ (Hoshi no Kaabii) (2001) -  Episode 1 - Kirby"
            R" - Right Back at Ya! Japanese [a9vrQ3Ns0gg].mkv"
        )
        # Getting the directory.
        filename = library.path.get_filename_without_extension(
            pathname=example_linux_pathname
        )
        expected_filename = (
            R"星のカービィ (Hoshi no Kaabii) (2001) - Episode 1 - Kirby -   Right Back at Ya!"
            R" Japanese [a9vrQ3Ns0gg]"
        )
        # Asserting.
        assert_message = "Linux based pathnames fail."
        assert filename == expected_filename, assert_message
    return None


def test_get_filename_with_extension() -> None:
    """Test the ability to get the filename with extension from a pathname.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    if IS_OPERATING_SYSTEM_WINDOWS:
        # Example of a Windows OS pathname with spaces and other intresting
        # characters.
        example_windows_pathname = (
            R"A:\Kalos\Music\Pokémon\Official Tracks\Mystery Dungeon\PMD"
            R" Explorers\Dialga's Fight to the Finish!.flac"
        )
        # Getting the directory.
        filename = library.path.get_filename_with_extension(
            pathname=example_windows_pathname
        )
        expected_filename = R"Dialga's Fight to the Finish!.flac"
        # Asserting.
        assert_message = "Windows based pathnames fail."
        assert filename == expected_filename, assert_message
    else:
        # Example of a Linux OS pathname with spaces and other intresting
        # characters.
        example_linux_pathname = (
            R"/home/sparrow/Kirby/星のカービィ (Hoshi no Kaabii) (2001) -  Episode 1 - Kirby"
            R" - Right Back at Ya! Japanese [a9vrQ3Ns0gg].mkv"
        )
        # Getting the directory.
        filename = library.path.get_filename_with_extension(
            pathname=example_linux_pathname
        )
        expected_filename = (
            R"星のカービィ (Hoshi no Kaabii) (2001) - Episode 1 - Kirby -   Right Back at Ya!"
            R" Japanese [a9vrQ3Ns0gg].mkv"
        )
        # Asserting.
        assert_message = "Linux based pathnames fail."
        assert filename == expected_filename, assert_message
    return None


def test_get_file_extension() -> None:
    """Test the ability to get the file extension from a pathname.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    if IS_OPERATING_SYSTEM_WINDOWS:
        # Example of a Windows OS pathname with spaces and other intresting
        # characters.
        example_windows_pathname = (
            R"A:\Kalos\Music\Pokémon\Official Tracks\Mystery Dungeon\PMD"
            R" Explorers\Dialga's Fight to the Finish!.flac"
        )
        # Getting the directory.
        extension = library.path.get_file_extension(pathname=example_windows_pathname)
        expected_extension = R"flac"
        # Asserting.
        assert_message = "Windows based pathnames fail."
        assert extension == expected_extension, assert_message
    else:
        # Example of a Linux OS pathname with spaces and other intresting
        # characters.
        example_linux_pathname = (
            R"/home/sparrow/Kirby/星のカービィ (Hoshi no Kaabii) (2001) -  Episode 1 - Kirby"
            R" - Right Back at Ya! Japanese [a9vrQ3Ns0gg].mkv"
        )
        # Getting the directory.
        extension = library.path.get_file_extension(pathname=example_linux_pathname)
        expected_extension = R"mkv"
        # Asserting.
        assert_message = "Linux based pathnames fail."
        assert extension == expected_extension, assert_message
    return None


def test_merge_pathname() -> None:
    """Test the ability to merge a pathname.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    if IS_OPERATING_SYSTEM_WINDOWS:
        # For Windows based pathnames.
        windows_directory = R"A:\Kalos\Pictures\Space Battleship Yamato"
        windows_filename = R"Space Battle Ship USS Arizona"
        windows_extension = R"jpg"
        # Merging.
        windows_pathname = library.path.merge_pathname(
            directory=windows_directory,
            filename=windows_filename,
            extension=windows_extension,
        )
        windows_expected_pathname = (
            R"A:\Kalos\Pictures\Space Battleship Yamato\Space Battle Ship USS"
            R" Arizona.jpg"
        )
        assert_message = "Windows pathname merging did not work."
        assert windows_pathname == windows_expected_pathname, assert_message
    else:
        # For Linux based pathnames.
        linux_directory = R"/home/sparrow/test/wiki"
        linux_filename = R"docker-compose"
        linux_extension = R"yml"
        # Merging.
        linux_pathname = library.path.merge_pathname(
            directory=linux_directory,
            filename=linux_filename,
            extension=linux_extension,
        )
        linux_expected_pathname = R"/home/sparrow/test/wiki/docker-compose.yml"
        assert_message = "Linux pathname merging did not work."
        assert linux_pathname == linux_expected_pathname, assert_message
    return None


def test_split_pathname() -> None:
    """Test the ability to split a pathname.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    if IS_OPERATING_SYSTEM_WINDOWS:
        # For Windows based pathnames.
        windows_pathname = (
            R"A:\Kalos\Pictures\Space Battleship Yamato\Space Battle Ship USS"
            R" Arizona.jpg"
        )
        # Splitting.
        (
            windows_directory,
            windows_filename,
            windows_extension,
        ) = library.path.split_pathname(pathname=windows_pathname)
        expected_windows_directory = R"A:\Kalos\Pictures\Space Battleship Yamato"
        expected_windows_filename = R"Space Battle Ship USS Arizona"
        expected_windows_extension = R"jpg"

        assert_message = "Windows pathname splitting did not work."
        assert (
            windows_directory == expected_windows_directory
            and windows_filename == expected_windows_filename
            and windows_extension == expected_windows_extension
        ), assert_message
    else:
        # For Linux based pathnames.
        linux_pathname = (
            R"/home/sparrow/test/wiki/docker-compose.yml"
        )
        # Splitting.
        (
            linux_directory,
            linux_filename,
            linux_extension,
        ) = library.path.split_pathname(pathname=linux_pathname)
        expected_linux_directory = R"/home/sparrow/test/wiki"
        expected_linux_filename = R"docker-compose"
        expected_linux_extension = R"yml"

        assert_message = "Linux pathname splitting did not work."
        assert (
            linux_directory == expected_linux_directory
            and linux_filename == expected_linux_filename
            and linux_extension == expected_linux_extension
        ), assert_message
    return None
