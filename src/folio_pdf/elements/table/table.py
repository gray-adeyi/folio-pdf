"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.enums import Direction
from folio_pdf.exceptions import TableException

from .table_row import TableRow

_ErrorCode = int

lib.folio_table_new.argtypes = []
lib.folio_table_new.restype = ct.c_uint64

lib.folio_table_free.argtypes = [ct.c_uint64]
lib.folio_table_free.restype = None

lib.folio_table_set_border_collapse.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_table_set_border_collapse.restype = ct.c_int32

lib.folio_table_set_cell_spacing.argtypes = [ct.c_uint64, ct.c_double, ct.c_double]
lib.folio_table_set_cell_spacing.restype = ct.c_int32

lib.folio_table_set_auto_column_widths.argtypes = [ct.c_uint64]
lib.folio_table_set_auto_column_widths.restype = ct.c_int32

lib.folio_table_set_direction.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_table_set_direction.restype = ct.c_int32

lib.folio_table_set_min_width.argtypes = [ct.c_uint64, ct.c_double]
lib.folio_table_set_min_width.restype = ct.c_int32

lib.folio_table_add_row.argtypes = [ct.c_uint64]
lib.folio_table_add_row.restype = ct.c_uint64

lib.folio_table_add_header_row.argtypes = [ct.c_uint64]
lib.folio_table_add_header_row.restype = ct.c_uint64

lib.folio_table_add_footer_row.argtypes = [ct.c_uint64]
lib.folio_table_add_footer_row.restype = ct.c_uint64


class Table(AbstractFolioObject):
    """
    Represents a PDF table.
    """

    _requires_close = True
    _binding_resource_free_fn = lib.folio_table_free

    def __init__(self):
        self._is_closed = False
        self.__handle = lib.folio_table_new()

    @_with_error_handling(TableException)
    def column_widths(self, widths: list[float]) -> _ErrorCode:
        """
        Sets explicit column widths in points.

        Args:
            widths: one width value per column

        Returns:
            this table instance, for chaining
        """
        DoubleArray = ct.c_double * len(widths)
        lib.folio_table_set_column_widths.argtypes = [
            ct.c_uint64,
            DoubleArray,
            ct.c_int32,
        ]
        lib.folio_table_set_column_widths.restype = ct.c_int32

        return lib.folio_table_set_column_widths(
            self._handle, DoubleArray(widths), ct.c_int32(len(widths))
        )

    @_with_error_handling(TableException)
    def border_collapse(self, enabled: bool) -> _ErrorCode:
        """
        Enables or disables border-collapse mode (adjacent borders share a single line).

        Args:
            enabled: `True` to collapse borders

        Returns:
            this table instance, for chaining
        """
        return lib.folio_table_set_border_collapse(self._handle, ct.c_bool(enabled))

    @_with_error_handling(TableException)
    def cell_spacing(self, h: float, v: float) -> _ErrorCode:
        """
        Sets the horizontal and vertical spacing between cells.

        Args:
            h: horizontal cell spacing in points
            v: vertical cell spacing in points

        Returns:
            this table instance, for chaining
        """
        return lib.folio_table_set_cell_spacing(
            self._handle, ct.c_double(h), ct.c_double(v)
        )

    @_with_error_handling(TableException)
    def auto_column_widths(self) -> _ErrorCode:
        """
        Enables automatic column width calculation based on cell content.

        Returns:
            this table instance, for chaining
        """
        return lib.folio_table_set_auto_column_widths(self._handle)

    @_with_error_handling(TableException)
    def direction(self, dir: Direction) -> _ErrorCode:
        """
        Sets the writing direction (LTR, RTL, or AUTO) for this table.

        An RTL table reverses the visual order of its columns: the first
        column added becomes the rightmost cell on each row. `Directions.AUTO`
        defers the choice to the Bidi heuristic over the cell content. See
        ISO 32000-2 §14.8.2 (Structure Attributes) for tagged-PDF interactions.

        Args:
            direction: the desired `Directions` variant

        Returns:
            this table, for chaining
        """
        return lib.folio_table_set_direction(self._handle, ct.c_int32(dir.value))

    @_with_error_handling(TableException)
    def min_width(self, pts: float) -> _ErrorCode:
        """
        Sets the minimum total table width in points.

        Args:
            pts: minimum width in points

        Returns:
            this table instance, for chaining
        """
        return lib.folio_table_set_min_width(ct.c_double(pts))

    def add_row(self) -> TableRow:
        """
        Adds a row to the table

        Returns:
            the added row instance
        """
        row_handle = lib.folio_table_add_row(self._handle)
        return TableRow._new_from_handle(row_handle)

    def add_header_row(self) -> TableRow:
        """
        Adds an header row to the table

        Returns:
            the added header row instance
        """
        row_handle = lib.folio_table_add_header_row(self._handle)
        return TableRow._new_from_handle(row_handle)

    def add_footer_row(self) -> TableRow:
        """
        Adds a footer row to the table

        Returns:
            the added footer row instance
        """
        row_handle = lib.folio_table_add_footer_row(self._handle)
        return TableRow._new_from_handle(row_handle)

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)
