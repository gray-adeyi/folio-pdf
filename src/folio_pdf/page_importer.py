"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, lib


class PageImporter(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self._redactor_handle = -1

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._redactor_handle)

    def close(self):
        lib.folio_page_import_free(self.handle)

    @property
    def width(self): ...

    @property
    def height(self): ...
