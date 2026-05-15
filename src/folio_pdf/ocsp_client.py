"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, lib


class OCSPClient(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self.__handle = lib.folio_ocsp_client_new()

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)

    def close(self):
        lib.folio_ocsp_client_free(self._handle)
