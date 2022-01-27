"""Photometric database access using PANSTARRS data. There are a few ways and 
they are implemented here."""


import astropy.io.ascii as ap_ascii
import astropy.table as ap_table
import numpy as np
import requests

import opihiexarata.library as library
import opihiexarata.library.error as error
import opihiexarata.library.hint as hint

PANSTARRS_AVAILABLE_COLUMNS = [
    "objName",
    "objAltName1",
    "objAltName2",
    "objAltName3",
    "objID",
    "uniquePspsOBid",
    "ippObjID",
    "surveyID",
    "htmID",
    "zoneID",
    "tessID",
    "projectionID",
    "skyCellID",
    "randomID",
    "batchID",
    "dvoRegionID",
    "processingVersion",
    "objInfoFlag",
    "qualityFlag",
    "raStack",
    "decStack",
    "raStackErr",
    "decStackErr",
    "raMean",
    "decMean",
    "raMeanErr",
    "decMeanErr",
    "epochMean",
    "posMeanChisq",
    "cx",
    "cy",
    "cz",
    "lambda",
    "beta",
    "l",
    "b",
    "nStackObjectRows",
    "nStackDetections",
    "nDetections",
    "ng",
    "nr",
    "ni",
    "nz",
    "ny",
    "gQfPerfect",
    "gMeanPSFMag",
    "gMeanPSFMagErr",
    "gMeanPSFMagStd",
    "gMeanPSFMagNpt",
    "gMeanPSFMagMin",
    "gMeanPSFMagMax",
    "gMeanKronMag",
    "gMeanKronMagErr",
    "gMeanKronMagStd",
    "gMeanKronMagNpt",
    "gMeanApMag",
    "gMeanApMagErr",
    "gMeanApMagStd",
    "gMeanApMagNpt",
    "gFlags",
    "rQfPerfect",
    "rMeanPSFMag",
    "rMeanPSFMagErr",
    "rMeanPSFMagStd",
    "rMeanPSFMagNpt",
    "rMeanPSFMagMin",
    "rMeanPSFMagMax",
    "rMeanKronMag",
    "rMeanKronMagErr",
    "rMeanKronMagStd",
    "rMeanKronMagNpt",
    "rMeanApMag",
    "rMeanApMagErr",
    "rMeanApMagStd",
    "rMeanApMagNpt",
    "rFlags",
    "iQfPerfect",
    "iMeanPSFMag",
    "iMeanPSFMagErr",
    "iMeanPSFMagStd",
    "iMeanPSFMagNpt",
    "iMeanPSFMagMin",
    "iMeanPSFMagMax",
    "iMeanKronMag",
    "iMeanKronMagErr",
    "iMeanKronMagStd",
    "iMeanKronMagNpt",
    "iMeanApMag",
    "iMeanApMagErr",
    "iMeanApMagStd",
    "iMeanApMagNpt",
    "iFlags",
    "zQfPerfect",
    "zMeanPSFMag",
    "zMeanPSFMagErr",
    "zMeanPSFMagStd",
    "zMeanPSFMagNpt",
    "zMeanPSFMagMin",
    "zMeanPSFMagMax",
    "zMeanKronMag",
    "zMeanKronMagErr",
    "zMeanKronMagStd",
    "zMeanKronMagNpt",
    "zMeanApMag",
    "zMeanApMagErr",
    "zMeanApMagStd",
    "zMeanApMagNpt",
    "zFlags",
    "yQfPerfect",
    "yMeanPSFMag",
    "yMeanPSFMagErr",
    "yMeanPSFMagStd",
    "yMeanPSFMagNpt",
    "yMeanPSFMagMin",
    "yMeanPSFMagMax",
    "yMeanKronMag",
    "yMeanKronMagErr",
    "yMeanKronMagStd",
    "yMeanKronMagNpt",
    "yMeanApMag",
    "yMeanApMagErr",
    "yMeanApMagStd",
    "yMeanApMagNpt",
    "yFlags",
    "distance",
]
# The column names are fine case insensitive for the MAST API call.
PANSTARRS_AVAILABLE_COLUMNS_LOWERCASE = [
    namedex.lower() for namedex in PANSTARRS_AVAILABLE_COLUMNS
]


class PanstarrsMastWebAPIEngine(library.engine.PhotometryEngine):
    """This is a photometric data extractor using PanSTARRS data obtained from
    their catalogs via the MAST API.

    See https://catalogs.mast.stsci.edu/docs/panstarrs.html for more
    information.
    """

    def __init__(self, verify_ssl: bool = True) -> None:
        """Create the instance of the API.

        Parameters
        ----------
        verify_ssl : boolean, default = True
            Connecting to the MAST API usually uses SSL verification via HTTPS,
            set to False to allow bypassing this.

        Returns
        -------
        None
        """
        self.verify_ssl = verify_ssl

        return None

    def _mask_table_data(self, data_table: hint.Table) -> hint.Table:
        """This masks the raw data derived from PanSTARRS, implementing the
        masking/null value specifics of the PanSTARRS system.

        The point of this is to make masked or invalid data more typical to
        the user by abstracting the idiosyncrasies of PanSTARRS.

        Parameters
        ----------
        data_table : Astropy Table
            The data table to be cleaned up.

        Return
        ------
        masked_data_table : Astropy Table
            The masked table.
        """
        # Enable masking capabilities, requires a new table.
        masked_data_table = ap_table.Table(data_table, masked=True)

        # Each column has different data types and the method which they are
        # flagged as masked are different.
        for colnamedex in data_table.colnames:
            column_data = np.array(data_table[colnamedex].value)

            # The method of masking is dependent on the kind of data contained.
            data_type = column_data.dtype.kind
            if data_type in ("U", "S"):
                # It is a string. The method for masking is not known.
                mask = np.zeros_like(column_data, dtype=bool)
            elif data_type in ("i", "f", "c"):
                # It is numerical data, unknown values are denoted by -999.
                mask = np.where(column_data <= -999, True, False)
            else:
                raise error.UndiscoveredError(
                    "The data type that PanSTARRS is sending is not one which has an"
                    " appropriate masking idiosyncrasy documented and implemented in"
                    " this API."
                )
            # Apply the mask to the column.
            masked_data_table[colnamedex].mask = mask
        return masked_data_table

    def cone_search(
        self,
        ra: float,
        dec: float,
        radius: float,
        detections: int = 3,
        color_detections: int = 1,
        columns: list[str] = None,
        max_rows: int = 1000,
        data_release: int = 2,
    ) -> hint.Table:
        """Search the PanSTARRS database for targets within a cone region
        specified.

        The table data returned from this function is not processed and is raw
        from the fetching of the results.

        Parameters
        ----------
        ra : float
            The right ascension of the center point of the cone search, in
            degrees.
        dec : float
            The declination of the center point of the cone search, in
            degrees.
        radius : float
            The radius from the center point of the cone search in which to
            search, in degrees.
        detections : int, default = 3
            The minimum number of detections each object needs to have to be
            included.
        color_detections : int, default = 1
            The minimum number of detections for the g, r, i, z filters of the
            Sloan filters of PanSTARRS. As this is a photometric engine for
            OpihiExarata, the filters should be the ones pertinent to the
            telescope.
        columns : list
            The columns that are desired to be pulled. The purpose of this is
            to lighten the data download load. If None, then it defaults to
            all columns.
        max_rows : int, default = 1000
            The maximum entries that will be pulled from the server.
        data_release : int, default = 2
            The PanSTARRS data release version from which to take the data from.

        Return
        ------
        catalog_results : Astropy Table
            The result of the cone search, pulled from the PanSTARRS catalog.
        """
        # Ensure that the RA and DEC are within degrees limits. The radius limit
        # also should have reasonable limits constrained upon it.
        if not 0 <= ra <= 360:
            raise error.InputError(
                "The right ascension for the cone search must be in degrees and within"
                " the reasonable limits thereof."
            )
        if not -90 <= dec <= 90:
            raise error.InputError(
                "The declination for the cone search must be in degrees and within the"
                " reasonable limits thereof."
            )
        if not 0 <= radius <= 180:
            raise error.InputError(
                "The right ascension for the cone search must be in degrees and within"
                " the reasonable limits thereof. The limit is the entire sky."
            )
        # Sanity checks for the other input parameters.
        try:
            detections = int(detections)
            if detections < 1:
                raise error.InputError(
                    "The number of required detections must be at least one."
                )
        except TypeError:
            error.InputError(
                "The number of detections inputted must be integer convertable."
            )
        try:
            max_rows = int(max_rows)
            if max_rows < 1:
                raise error.InputError(
                    "The number of required maximum rows queried must be at least one."
                )
        except TypeError:
            error.InputError(
                "The number of maximum rows queried inputted must be integer"
                " convertable."
            )

        # Check that the columns provided are valid columns.
        if columns is None:
            # The default is all columns.
            columns = PANSTARRS_AVAILABLE_COLUMNS_LOWERCASE
        elif isinstance(columns, str):
            # Encapsulate it into a list to retain it being a single value.
            columns = [columns]
        else:
            columns = list(columns)
        for columnlabeldex in columns:
            if columnlabeldex.lower() not in PANSTARRS_AVAILABLE_COLUMNS_LOWERCASE:
                raise error.InputError(
                    "The column label `{label}` is not a valid column which can be used"
                    " with the PanSTARRS query.".format(label=columnlabeldex)
                )
        # Specific formatting for the MAST API call.
        columns = [namedex.lower() for namedex in columns]
        colstring = "[" + ",".join(columns) + "]"

        # Check that the data release is suppored.
        data_release = str(data_release)
        VALID_PANSTARRS_DATA_RELEASES = ("1", "2")
        if data_release not in VALID_PANSTARRS_DATA_RELEASES:
            raise error.InputError(
                "The data release version provided is not supported."
            )

        # The MAST API service is a url request. Constructing the URL based on
        # the provided information.
        mast_api_url = (
            "https://catalogs.mast.stsci.edu/api/v0.1/panstarrs/dr{v}/mean?"
            "ra={a}&dec={d}&radius={r}&nDetections.gte={n}&columns={c}&pagesize={l}&"
            "ng.gte={p}&nr.gte={p}&ni.gte={p}&nz.gte={p}&"
            "format=csv"
        ).format(
            v=data_release,
            a=ra,
            d=dec,
            r=radius,
            n=detections,
            c=colstring,
            l=max_rows,
            p=color_detections,
        )
        # Pull the data into a table.
        query = requests.post(mast_api_url, verify=self.verify_ssl)
        catalog_results = ap_ascii.read(query.text, format="csv")
        return catalog_results

    def masked_cone_search(self, *args, **kwargs) -> hint.Table:
        """The same as cone_search, but it also masks the data based on the
        masking idiosyncrasies of PanSTARRS.

        Parameters
        ----------
        (see cone_search)

        Returns
        -------
        masked_catalog_results : Astropy Table
            The data from the cone search with the entries masked where
            appropriate.
        """
        # Get the data that will be post-processed using making.
        catalog_results = self.cone_search(*args, **kwargs)
        # Mask the table.
        masked_catalog_results = self._mask_table_data(data_table=catalog_results)
        return masked_catalog_results
