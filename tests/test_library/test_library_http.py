"""Test HTTP interaction functions."""

import os

import opihiexarata


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
    # For the Wikipedia link, they require a User agent.
    http_headers = {
        "User-Agent":"Mozilla/5.0 (X11; Linux i686; rv:148.0) Gecko/20100101 Firefox/148.0",
    }
    # Try to download the image.
    try:
        opihiexarata.library.http.download_file_from_url(
            url=image_url, filename=save_path, http_headers=http_headers
        )
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
