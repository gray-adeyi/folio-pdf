"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, lib


class Column(AbstractFolioObject):
    _requires_close = True

    def __init__(self, cols: int):
        self._column_handle = lib.folio_columns_new(ct.c_int32(cols))

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._column_handle)

    def close(self):
        lib.folio_columns_free(self.handle)

    def set_gap(self, gap: float): ...

    def set_widths(self): ...

    def set_balanced(self): ...

    def add(self): ...
