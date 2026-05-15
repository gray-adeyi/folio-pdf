"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct
from typing import TYPE_CHECKING

from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.exceptions import ColumnException

if TYPE_CHECKING:
    from folio_pdf.folio_pdf import Element


class Column(AbstractFolioObject):
    _requires_close = True

    def __init__(self, cols: int):
        self._column_handle = lib.folio_columns_new(ct.c_int32(cols))

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._column_handle)

    def close(self):
        lib.folio_columns_free(self.handle)

    @_with_error_handling(ColumnException)
    def gap(self, gap: float):
        return lib.folio_columns_set_gap(self.handle, ct.c_double(gap))

    @_with_error_handling(ColumnException)
    def widths(self, widths: list[float]):
        DoubleArray = ct.c_double * len(widths)
        return lib.folio_columns_set_widths(
            self.handle, DoubleArray(widths), ct.c_int32(len(widths))
        )

    @_with_error_handling(ColumnException)
    def balanced(self, enabled: bool):
        return lib.folio_columns_set_balanced(self.handle, ct.c_int32(enabled))

    @_with_error_handling(ColumnException)
    def add(self, col_index: int, element: "Element"):
        return lib.folio_columns_add(self.handle, ct.c_int32(col_index), element.handle)
