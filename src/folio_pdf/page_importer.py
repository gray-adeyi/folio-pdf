"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, lib


class PageImporter(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self.__handle = -1

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)

    def close(self):
        lib.folio_page_import_free(self._handle)

    @property
    def width(self):
        return lib.folio_page_import_width(self._handle)

    @property
    def height(self):
        return lib.folio_page_import_height(self._handle)
