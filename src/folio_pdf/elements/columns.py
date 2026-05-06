"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

from folio_pdf.object import AbstractFolioObject
from folio_pdf.core import lib
import ctypes as ct


class Column(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self._column_handle = lib.folio_column_new()

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._column_handle)

    def close(self):
        lib.folio_grid_free(self.handle)
