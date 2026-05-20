"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, lib

lib.folio_tsa_client_new.argtypes = [ct.c_char_p]
lib.folio_tsa_client_new.restype = ct.c_uint64

lib.folio_tsa_client_free.argtypes = [ct.c_uint64]
lib.folio_tsa_client_free.restype = None


class TSAClient(AbstractFolioObject):
    """
    A Time Stamp Authority (TSA) client for adding trusted timestamps
    to digital signatures. Required for PAdES B-T and above.
    """

    _requires_close = True

    def __init__(self, url: str):
        """
        Creates a TSA client pointing to the given URL.

        Args:
            url: the TSA service URL

        Returns:
            a new `TSAClient`
        """
        self.__handle = lib.folio_tsa_client_new(ct.c_char_p(url.encode()))

    def close(self):
        lib.folio_tsa_client_free(self._handle)

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)
