"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

from folio_pdf.font import Font
from folio_pdf.table_cell import TableCell
from folio_pdf.core import lib

from folio_pdf.object import AbstractFolioObject
import ctypes as ct


class TableRow(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self._row_handle = -1

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._row_handle)

    @classmethod
    def _new_from_handle(cls, row_handle: int):
        obj = cls.__new__(cls)
        cls._row_handle = row_handle
        return obj

    def close(self):
        lib.folio_row_free(self.handle)

    def add_cell(self, text: str, font: Font, font_size: float) -> TableCell:
        handle = lib.folio_row_add_cell(
            self.handle, ct.c_char_p(text.encode()), font.handle, ct.c_double(font_size)
        )
        return TableCell._new_from_handle(handle)

    def add_cell_embedded(self, text: str, font: Font, font_size: float) -> TableCell:
        handle = lib.folio_row_add_cell_embedded(
            self.handle, ct.c_char_p(text.encode()), font.handle, ct.c_double(font_size)
        )
        return TableCell._new_from_handle(handle)

    def add_cell_element(self, element) -> TableCell:
        handle = lib.folio_row_add_cell_element(self.handle, element.handle)
        return TableCell._new_from_handle(handle)
