"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct
from typing import TYPE_CHECKING

from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.exceptions import ColumnsException

if TYPE_CHECKING:
    from folio_pdf.folio_pdf import Element


class Columns(AbstractFolioObject):
    """A multi-column layout container that places child elements into independently sized columns.

    Content is assigned to a specific column by index, allowing side-by-side layout without
    requiring a full grid setup.
    """

    _requires_close = True

    def __init__(self, cols: int):
        self.__handle = lib.folio_columns_new(ct.c_int32(cols))

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)

    def close(self):
        lib.folio_columns_free(self._handle)

    @_with_error_handling(ColumnsException)
    def gap(self, gap: float):
        """Sets the gap between columns in points.

        Args:
            gap: the inter-column gap in points

        Returns:
            this instance for chaining
        """
        return lib.folio_columns_set_gap(self._handle, ct.c_double(gap))

    @_with_error_handling(ColumnsException)
    def widths(self, widths: list[float]):
        """Sets the width of each column in points.

        The number of values should match the column count `cols` used to
        instantiate the object.

        Args:
            widths: one width value per column, in points

        Returns:
            this instance for chaining
        """
        DoubleArray = ct.c_double * len(widths)
        return lib.folio_columns_set_widths(
            self._handle, DoubleArray(widths), ct.c_int32(len(widths))
        )

    @_with_error_handling(ColumnsException)
    def balanced(self, enabled: bool):
        """Toggles balanced column fill. When balanced, the engine sequentially
        fills columns to roughly equal heights instead of overflowing the
        first column before starting the next. When disabled, content fills
        each column to the available height in turn.

        Balanced layout follows the model used by the CSS
        `column-fill: balance` property (CSS Multi-column Layout, level 1).

        Args:
            balanced: `True` to enable balanced filling

        Returns:
            this instance for chaining
        """
        return lib.folio_columns_set_balanced(self._handle, ct.c_int32(enabled))

    @_with_error_handling(ColumnsException)
    def add(self, col_index: int, element: "Element"):
        """Adds an element to the specified column.

        Args:
            col_index: the zero-based column index
            element: the element to add

        Returns:
            this instance for chaining
        """
        return lib.folio_columns_add(
            self._handle, ct.c_int32(col_index), element._handle
        )
