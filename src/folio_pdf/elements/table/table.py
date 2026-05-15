"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.enums import Directions
from folio_pdf.exceptions import TableException

from .table_row import TableRow


class Table(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self.__handle = lib.folio_table_new()

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)

    def close(self):
        lib.folio_table_free(self._handle)

    @_with_error_handling(TableException)
    def column_widths(self, widths: list[float]):
        DoubleArray = ct.c_double * len(widths)
        return lib.folio_table_set_column_widths(
            self._handle, DoubleArray(widths), ct.c_int32(len(widths))
        )

    @_with_error_handling(TableException)
    def border_collapse(self, enabled: bool):
        return lib.folio_table_set_border_collapse(self._handle, ct.c_bool(enabled))

    @_with_error_handling(TableException)
    def cell_spacing(self, h: float, v: float):
        return lib.folio_table_set_cell_spacing(
            self._handle, ct.c_double(h), ct.c_double(v)
        )

    @_with_error_handling(TableException)
    def auto_column_widths(self):
        return lib.folio_table_set_auto_column_widths(self._handle)

    @_with_error_handling(TableException)
    def direction(self, dir: Directions):
        return lib.folio_table_set_direction(self._handle, ct.c_int32(dir.value))

    @_with_error_handling(TableException)
    def min_width(self, pts: float):
        return lib.folio_table_set_min_width(ct.c_double(pts))

    def add_row(self) -> TableRow:
        row_handle = lib.folio_table_add_row(self._handle)
        return TableRow._new_from_handle(row_handle)

    def add_header_row(self) -> TableRow:
        row_handle = lib.folio_table_add_header_row(self._handle)
        return TableRow._new_from_handle(row_handle)

    def add_footer_row(self) -> TableRow:
        row_handle = lib.folio_table_add_footer_row(self._handle)
        return TableRow._new_from_handle(row_handle)
