"""Test HTTP interaction functions."""

import os

import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint


def test_download_file_from_url() -> None:
    """Test the ability download a file from a url.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    # Using Wikipedia, mostly because it is likely that they will be online,
    # and they have nice public domain images. Sparrow likes this logo.
    image_url = "https://upload.wikimedia.org/wikipedia/commons/6/6d/Seal_of_Cybersecurity_and_Infrastructure_Security_Agency.svg"
    save_path = "./cisa_seal.svg"
    # Try to download the image.
    try:
        library.http.download_file_from_url(url=image_url, filename=save_path)
    except:
        assert_message = "Could not download the file from the test link."
        assert False, assert_message
    finally:
        # Delete the file, this is just a test after all.
        try:
            os.remove(save_path)
        except OSError:
            pass
    return None
