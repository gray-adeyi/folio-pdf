"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct
from typing import TYPE_CHECKING

from folio_pdf.core import AbstractFolioObject, lib
from folio_pdf.font import Font

from .table_cell import TableCell

if TYPE_CHECKING:
    from folio_pdf.folio_pdf import Element


class TableRow(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self.__handle = 0

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)

    @classmethod
    def _new_from_handle(cls, row_handle: int):
        obj = cls.__new__(cls)
        cls.__handle = row_handle
        return obj

    def close(self):
        lib.folio_row_free(self._handle)

    def add_cell(self, text: str, font: Font, font_size: float) -> TableCell:
        handle = lib.folio_row_add_cell(
            self._handle,
            ct.c_char_p(text.encode()),
            font._handle,
            ct.c_double(font_size),
        )
        return TableCell._new_from_handle(handle)

    def add_cell_embedded(self, text: str, font: Font, font_size: float) -> TableCell:
        handle = lib.folio_row_add_cell_embedded(
            self._handle,
            ct.c_char_p(text.encode()),
            font._handle,
            ct.c_double(font_size),
        )
        return TableCell._new_from_handle(handle)

    def add_cell_element(self, element: "Element") -> TableCell:
        handle = lib.folio_row_add_cell_element(self._handle, element._handle)
        return TableCell._new_from_handle(handle)
