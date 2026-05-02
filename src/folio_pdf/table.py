"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

from folio_pdf.table_row import TableRow
from folio_pdf.exceptions import TableException
from folio_pdf.core import lib, _with_error_handling
from folio_pdf.object import AbstractFolioObject
import ctypes as ct


class Table(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self._table_handle = lib.folio_table_new()

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._table_handle)

    def close(self):
        lib.folio_table_free(self.handle)

    @_with_error_handling(TableException)
    def set_column_widths(self, widths: list[float]):
        DoubleArray = ct.c_double * len(widths)
        return lib.folio_table_set_column_widths(
            self.handle, DoubleArray(widths), ct.c_int32(len(widths))
        )

    @_with_error_handling(TableException)
    def set_border_collapse(self, enabled: bool):
        return lib.folio_table_set_border_collapse(self.handle, ct.c_bool(enabled))

    @_with_error_handling(TableException)
    def set_cell_spacing(self, h: float, v: float):
        return lib.folio_table_set_cell_spacing(
            self.handle, ct.c_double(h), ct.c_double(v)
        )

    @_with_error_handling(TableException)
    def set_auto_column_widths(self):
        return lib.folio_table_set_auto_column_widths(self.handle)

    @_with_error_handling(TableException)
    def set_min_width(self, pts: float):
        return lib.folio_table_set_min_width(ct.c_double(pts))

    def add_row(self) -> TableRow:
        row_handle = lib.folio_table_add_row(self.handle)
        return TableRow._new_from_handle(row_handle)

    def add_header_row(self) -> TableRow:
        row_handle = lib.folio_table_add_header_row(self.handle)
        return TableRow._new_from_handle(row_handle)

    def add_footer_row(self) -> TableRow:
        row_handle = lib.folio_table_add_footer_row(self.handle)
        return TableRow._new_from_handle(row_handle)
