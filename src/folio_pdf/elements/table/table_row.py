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

lib.folio_row_free.argtypes = [ct.c_uint64]
lib.folio_row_free.restype = None

lib.folio_row_add_cell.argtypes = [ct.c_uint64, ct.c_char_p, ct.c_uint64, ct.c_double]
lib.folio_row_add_cell.restype = ct.c_uint64

lib.folio_row_add_cell_embedded.argtypes = [
    ct.c_uint64,
    ct.c_char_p,
    ct.c_uint64,
    ct.c_double,
]
lib.folio_row_add_cell_embedded.restype = ct.c_uint64

lib.folio_row_add_cell_element.argtypes = [ct.c_uint64, ct.c_uint64]
lib.folio_row_add_cell_element.restype = ct.c_uint64


class TableRow(AbstractFolioObject):
    """
    Represents a row within a `TableRow`.
    """

    _requires_close = True

    def __init__(self):
        self.__handle = 0

    def add_cell(self, text: str, font: Font, font_size: float) -> TableCell:
        """
        Adds a text cell with a custom font and font size.

        Args:
            text: the cell text
            font: the font for this cell
            font_size: the font size in points for this cell

        Returns:
            the new `TableCell`, for further styling
        """
        handle = lib.folio_row_add_cell(
            self._handle,
            ct.c_char_p(text.encode()),
            font._handle,
            ct.c_double(font_size),
        )
        return TableCell._new_from_handle(handle)

    def add_cell_embedded(self, text: str, font: Font, font_size: float) -> TableCell:
        """
        Adds a text cell with an embedded custom font subset.

        Args:
            text: the cell text
            font: the font to embed for this cell
            font_size: the font size in points for this cell

        Returns:
            the new `TableCell`, for further styling
        """
        handle = lib.folio_row_add_cell_embedded(
            self._handle,
            ct.c_char_p(text.encode()),
            font._handle,
            ct.c_double(font_size),
        )
        return TableCell._new_from_handle(handle)

    def add_cell_element(self, element: "Element") -> TableCell:
        """
        Adds a cell whose content is rendered from an element.

        Args:
            element: the element to place inside the cell

        Returns:
            the new `TableCell`, for further styling
        """
        handle = lib.folio_row_add_cell_element(self._handle, element._handle)
        return TableCell._new_from_handle(handle)

    def close(self):
        lib.folio_row_free(self._handle)

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)

    @classmethod
    def _new_from_handle(cls, row_handle: int):
        obj = cls.__new__(cls)
        cls.__handle = row_handle
        return obj
