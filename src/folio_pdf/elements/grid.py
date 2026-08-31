"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct
from typing import TYPE_CHECKING

from folio_pdf.color import Color
from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.enums import AlignItem, GridTrackType, JustifyContent
from folio_pdf.exceptions import GridException

if TYPE_CHECKING:
    from folio_pdf.folio_pdf import Element


if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

_ErrorCode = int

lib.folio_grid_new.argtypes = []
lib.folio_grid_new.restype = ct.c_uint64

lib.folio_grid_free.argtypes = [ct.c_uint64]
lib.folio_grid_free.restype = None

lib.folio_grid_add_child.argtypes = [ct.c_uint64, ct.c_uint64]
lib.folio_grid_add_child.restype = ct.c_int32

lib.folio_grid_set_border.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_grid_set_border.restype = ct.c_int32

lib.folio_grid_set_borders.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_grid_set_borders.restype = ct.c_int32

lib.folio_grid_set_gap.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
]
lib.folio_grid_set_gap.restype = ct.c_int32

lib.folio_grid_set_placement.argtypes = [
    ct.c_uint64,
    ct.c_int32,
    ct.c_int32,
    ct.c_int32,
    ct.c_int32,
    ct.c_int32,
]
lib.folio_grid_set_placement.restype = ct.c_int32

lib.folio_grid_set_padding.argtypes = [ct.c_uint64, ct.c_double]
lib.folio_grid_set_padding.restype = ct.c_int32

lib.folio_grid_set_background.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_grid_set_background.restype = ct.c_int32

lib.folio_grid_set_justify_items.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_grid_set_justify_items.restype = ct.c_int32

lib.folio_grid_set_align_items.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_grid_set_align_items.restype = ct.c_int32

lib.folio_grid_set_justify_content.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_grid_set_justify_content.restype = ct.c_int32

lib.folio_grid_set_align_content.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_grid_set_align_content.restype = ct.c_int32

lib.folio_grid_set_space_before.argtypes = [ct.c_uint64, ct.c_double]
lib.folio_grid_set_space_before.restype = ct.c_int32

lib.folio_grid_set_space_after.argtypes = [ct.c_uint64, ct.c_double]
lib.folio_grid_set_space_after.restype = ct.c_int32


class Grid(AbstractFolioObject):
    """
    A CSS grid-style layout container that arranges child elements into explicit
    rows and columns.
    """

    _requires_close = True
    _binding_resource_free_fn = lib.folio_grid_free

    def __init__(self):
        self._is_closed = False
        self.__handle = lib.folio_grid_new()

    @_with_error_handling(GridException)
    def add_child(self, element: "Element") -> _ErrorCode:
        """
        Adds an element as the next child in this grid.

        Args:
            element: the element to add

        Returns:
            this instance for chaining
        """
        return lib.folio_grid_add_child(self._handle, element._handle)

    @_with_error_handling(GridException)
    def template_columns(
        self, types: list[GridTrackType], values: list[float]
    ) -> _ErrorCode:
        """
        Defines the explicit column track sizes for the grid.

        Each entry in `types` corresponds to a variant of track types
        (`GridTrackTypes`) and the matching entry in `values` provides the
        numeric size for that track.

        Args:
        types: list of track type specifiers
        values: list of track size values

        Returns:
            this instance for chaining
        """
        Int32Array = ct.c_int32 * len(types)
        DoubleArray = ct.c_double * len(values)
        lib.folio_grid_set_template_columns.argtypes = [
            ct.c_uint64,
            Int32Array,
            DoubleArray,
            ct.c_int32,
        ]
        lib.folio_grid_set_template_columns.restype = ct.c_int32
        return lib.folio_grid_set_template_columns(
            self._handle,
            Int32Array([type_.value for type_ in types]),
            DoubleArray(values),
            ct.c_int32(len(values)),
        )

    @_with_error_handling(GridException)
    def template_rows(self, types: list[GridTrackType], values: list[float]) -> _ErrorCode:
        """
        Defines the explicit row track sizes for the grid.


        Each entry in `types` corresponds to a track type and
        the matching entry in `values` provides the numeric size.

        Args:
            types: list of track type specifiers
            values: list of track size values

        Returns:
            this instance for chaining
        """
        Int32Array = ct.c_int32 * len(types)
        DoubleArray = ct.c_double * len(values)
        lib.folio_grid_set_template_rows.argtypes = [
            ct.c_uint64,
            Int32Array,
            DoubleArray,
            ct.c_int32,
        ]
        lib.folio_grid_set_template_rows.restype = ct.c_int32
        return lib.folio_grid_set_template_rows(
            self._handle,
            Int32Array([type_.value for type_ in types]),
            DoubleArray(values),
            ct.c_int32(len(values)),
        )

    @_with_error_handling(GridException)
    def border(self, width: float, color: Color) -> _ErrorCode:
        """
        Sets a uniform border around this grid container.

        Args:
            width: border width in points
            color: the color of the border

        Returns:
            this instance for chaining
        """
        return lib.folio_grid_set_border(
            self._handle,
            ct.c_double(width),
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    @_with_error_handling(GridException)
    def borders(
        self,
        top_width: float,
        top_color: Color,
        right_width: float,
        right_color: Color,
        bottom_width: float,
        bottom_color: Color,
        left_width: float,
        left_color: Color,
    ) -> _ErrorCode:
        """
        Sets individual borders for each edge of the grid container.

        Args:
            top_width: top border width
            top_color: top border color
            right_width: right border width
            right_color: right border color
            bottom_width: bottom border width
            bottom_color: bottom border color
            left_width: left border width
            left_color: left border color

        Returns:
            this instance for chaining
        """
        return lib.folio_grid_set_borders(
            self._handle,
            ct.c_double(top_width),
            ct.c_double(top_color.r),
            ct.c_double(top_color.g),
            ct.c_double(top_color.b),
            ct.c_double(right_width),
            ct.c_double(right_color.r),
            ct.c_double(right_color.g),
            ct.c_double(right_color.b),
            ct.c_double(bottom_width),
            ct.c_double(bottom_color.r),
            ct.c_double(bottom_color.g),
            ct.c_double(bottom_color.b),
            ct.c_double(left_width),
            ct.c_double(left_color.r),
            ct.c_double(left_color.g),
            ct.c_double(left_color.b),
        )

    @_with_error_handling(GridException)
    def template_areas(self, rows: list[str]) -> _ErrorCode:
        """
        Defines CSS-style named grid areas. Each row string lists area names
        separated by whitespace (e.g., `"header header"`, `"nav main"`).

        Args:
            rows: the template area rows. (e.g., `"header header"`, `"nav main"`)

        Returns:
            this instance for chaining
        """
        cols: list[int] = []
        for idx, r in enumerate(rows):
            r = r.strip()
            if r == "":
                cols[idx] = 0
            else:
                cols[idx] = len(r.split(" "))

        CharPArray = ct.c_char_p * len(rows)
        Int32Array = ct.c_int32 * len(cols)
        lib.folio_grid_set_template_areas.argtypes = [
            ct.c_int64,
            CharPArray,
            Int32Array,
            ct.c_int32,
        ]
        lib.folio_grid_set_template_areas.restype = ct.c_int32
        return lib.folio_grid_set_template_areas(
            self._handle, CharPArray(rows), Int32Array(cols), ct.c_int32(len(rows))
        )

    @_with_error_handling(GridException)
    def auto_rows(self, types: list[GridTrackType], values: list[float]) -> _ErrorCode:
        """
        Sets the implicit row track sizes used for rows created outside
        the explicit template.

        Args:
            types: array of track type specifiers
            values: array of track size values

        Returns:
            this instance for chaining
        """
        Int32Array = ct.c_int32 * len(types)
        DoubleArray = ct.c_double * len(values)
        lib.folio_grid_set_auto_rows.argtypes = [
            ct.c_uint64,
            Int32Array,
            DoubleArray,
            ct.c_int32,
        ]
        lib.folio_grid_set_auto_rows.restype = ct.c_int32
        return lib.folio_grid_set_auto_rows(
            self._handle,
            Int32Array([type_.value for type_ in types]),
            DoubleArray(values),
            ct.c_int32(len(values)),
        )

    @_with_error_handling(GridException)
    def gap(self, row_gap: float, col_gap: float) -> _ErrorCode:
        """
        Sets the row and column gaps between grid cells.

        Args:
            row_gap: the gap between rows in points
                col_gap: the gap between columns in points

        Returns:
            this instance for chaining
        """
        return lib.folio_grid_set_gap(
            self._handle, ct.c_double(row_gap), ct.c_double(col_gap)
        )

    @_with_error_handling(GridException)
    def placement(
        self,
        child_index: int,
        col_start: int,
        col_end: int,
        row_start: int,
        row_end: int,
    ) -> _ErrorCode:
        """
        Explicitly places a child element into a specific grid area.

        Grid lines are 1-based. Use 0 for any boundary to indicate auto placement.

        Args:
            child_index: the zero-based index of the child (in the order it was added)
            col_start: the starting column line (1-based)
            col_end: the ending column line (exclusive, 1-based)
            row_start: the starting row line (1-based)
            row_end: the ending row line (exclusive, 1-based)

        Returns:
            this instance for chaining
        """
        return lib.folio_grid_set_placement(
            self._handle,
            ct.c_int32(child_index),
            ct.c_int32(col_start),
            ct.c_int32(col_end),
            ct.c_int32(row_start),
            ct.c_int32(row_end),
        )

    @_with_error_handling(GridException)
    def padding(self, padding: float) -> _ErrorCode:
        """
        Sets uniform padding on all sides of this grid container.

        Args:
            padding: the padding in points

        Returns:
            this instance for chaining
        """
        return lib.folio_grid_set_padding(self._handle, ct.c_double(padding))

    @_with_error_handling(GridException)
    def background(self, color: Color) -> _ErrorCode:
        """
        Sets the background color of this grid container.

        Args:
            color: the RGB background color

        Returns:
            this instance for chaining
        """
        return lib.folio_grid_set_background(
            self._handle,
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    @_with_error_handling(GridException)
    def justify_items(self, align: AlignItem) -> _ErrorCode:
        """
        Sets the default horizontal alignment of items within their grid cells.

        Args:
            align: the horizontal alignment

        Returns:
            this instance for chaining
        """
        return lib.folio_grid_set_justify_items(self._handle, ct.c_int32(align.value))

    @_with_error_handling(GridException)
    def align_items(self, align: AlignItem) -> _ErrorCode:
        """
        Sets the default vertical alignment of items within their grid cells.

        Args:
            align the vertical alignment

        Returns:
            this instance for chaining
        """
        return lib.folio_grid_set_align_items(self._handle, ct.c_int32(align.value))

    @_with_error_handling(GridException)
    def justify_content(self, justify: JustifyContent) -> _ErrorCode:
        """
        Sets how the grid tracks are distributed along the inline (column) axis.

        Args:
            justify: the justify-content strategy

        Returns:
            this instance for chaining
        """
        return lib.folio_grid_set_justify_content(
            self._handle, ct.c_int32(justify.value)
        )

    @_with_error_handling(GridException)
    def align_content(self, align: JustifyContent) -> _ErrorCode:
        """
        Sets how the grid tracks are distributed along the block (row) axis.

        Args:
            align: the align-content strategy

        Returns:
            this instance for chaining
        """
        return lib.folio_grid_set_align_content(self._handle, ct.c_int32(align.value))

    @_with_error_handling(GridException)
    def space_before(self, pts: float) -> _ErrorCode:
        """
        Sets extra vertical space before this grid container in the document flow.

        Args:
            pts: space in points

        Returns:
            this instance for chaining
        """
        return lib.folio_grid_set_space_before(self._handle, ct.c_double(pts))

    @_with_error_handling(GridException)
    def space_after(self, pts: float) -> _ErrorCode:
        """
        Sets extra vertical space after this grid container in the document flow.

        Args:
            pts: space in points

        Returns:
            this instance for chaining
        """
        return lib.folio_grid_set_space_after(self._handle, ct.c_double(pts))

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)
