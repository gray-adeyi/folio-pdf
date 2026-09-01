"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, lib

lib.folio_ocsp_client_new.argtypes = []
lib.folio_ocsp_client_new.restype = ct.c_uint64

lib.folio_ocsp_client_free.argtypes = [ct.c_uint64]
lib.folio_ocsp_client_free.restype = None


class OCSPClient(AbstractFolioObject):
    """
    An OCSP (Online Certificate Status Protocol) client for checking
    certificate revocation during signing. Required for PAdES B-LT and above.
    """

    _requires_close = True
    _binding_resource_free_fn = lib.folio_ocsp_client_free

    def __init__(self):
        self._is_closed = False
        self.__handle = lib.folio_ocsp_client_new()

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)
