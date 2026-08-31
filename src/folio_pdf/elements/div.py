"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct
from typing import TYPE_CHECKING, Literal

from folio_pdf.color import Color
from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.exceptions import DivException

if TYPE_CHECKING:
    from folio_pdf.folio_pdf import Element


_ErrorCode = int


class Div(AbstractFolioObject):
    """
    A block-level container that can hold other layout elements such as
    `Paragraph`, `Heading`, `Table`, `List`, and `ImageElement`.

    Use it to apply shared padding, background, border,
    or sizing to a group of elements.
    """

    _requires_close = True
    _binding_resource_free_fn = lib.folio_div_free

    def __init__(self):
        self._is_closed = False
        self.__handle = 0

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)

    @_with_error_handling(DivException)
    def add(self, element: "Element") -> _ErrorCode:
        """Appends a {@link Paragraph} to this div.

        Args:
            element: the paragraph to add

        Returns:
            this div, for chaining
        """
        return lib.folio_div_add(self._handle, element._handle)

    @_with_error_handling(DivException)
    def padding(
        self, top: float, right: float, bottom: float, left: float
    ) -> _ErrorCode:
        """Sets individual padding values for each side of this div.

        Args:
            top: top padding in points
            right: right padding in points
            bottom: bottom padding in points
            left: left padding in points

        Returns:
            this div, for chaining
        """
        return lib.folio_div_set_padding(
            self._handle,
            ct.c_double(top),
            ct.c_double(right),
            ct.c_double(bottom),
            ct.c_double(left),
        )

    @_with_error_handling(DivException)
    def background(self, color: Color) -> _ErrorCode:
        """
        Sets the background fill color of this div.

        Args:
            color: the background `Color`

        Returns:
            this div, for chaining
        """
        return lib.folio_div_set_background(
            self._handle,
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    @_with_error_handling(DivException)
    def border(self, width: float, color: Color) -> _ErrorCode:
        """
        Sets the border width and color for this div.

        Args:
            width: border line width in points
            color: the background `Color`

        Returns:
            this div, for chaining
        """
        return lib.folio_div_set_border(
            self._handle,
            ct.c_double(width),
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    @_with_error_handling(DivException)
    def width(self, pts: float) -> _ErrorCode:
        """
        Sets the explicit width of this div in points.

        Args:
            pts: width in points

        Returns:
            this div, for chaining
        """
        return lib.folio_div_set_width(self._handle, ct.c_double(pts))

    @_with_error_handling(DivException)
    def min_height(self, pts: float) -> _ErrorCode:
        """
        Sets the minimum height of this div in points.

        Args:
            pts: minimum height in points

        Returns:
            this div, for chaining
        """
        return lib.folio_div_set_min_height(self._handle, ct.c_double(pts))

    @_with_error_handling(DivException)
    def max_width(self, pts: float) -> _ErrorCode:
        """
        Sets the maximum width of this div in points.

        Args:
            pts: maximum width in points

        Returns:
            this div, for chaining
        """
        return lib.folio_div_set_max_width(self._handle, ct.c_double(pts))

    @_with_error_handling(DivException)
    def min_width(self, pts: float) -> _ErrorCode:
        """
        Sets the minimum width of this div in points.

        Args:
            pts: minimum width in points

        Returns:
            this div, for chaining
        """
        return lib.folio_div_set_min_width(self._handle, ct.c_double(pts))

    @_with_error_handling(DivException)
    def width_percent(self, pct: float) -> _ErrorCode:
        """
        Sets this div's width as a percentage of its containing block.

        Args:
            pct: percent width (e.g., `50.0` for half-width)

        Returns:
            this div, for chaining
        """
        return lib.folio_div_set_width_percent(self._handle, ct.c_double(pct))

    @_with_error_handling(DivException)
    def aspect_ratio(self, ratio: float) -> _ErrorCode:
        """
        Sets a fixed width/height aspect ratio for this div.

        Args:
            ratio: width divided by height

        Returns:
            this div, for chaining
        """
        return lib.folio_div_set_aspect_ratio(self._handle, ct.c_double(ratio))

    @_with_error_handling(DivException)
    def keep_together(self, enabled: bool) -> _ErrorCode:
        """
        Requests that the layout engine keep this div on a single page rather
        than splitting it across a page break.

        Args:
            enabled: whether to keep the div together

        Returns:
            this div, for chaining
        """
        return lib.folio_div_set_keep_together(self._handle, ct.c_bool(enabled))

    @_with_error_handling(DivException)
    def border_radius_per_corner(
        self, top_left: float, top_right: float, bottom_right: float, bottom_left: float
    ) -> _ErrorCode:
        """
        Sets individual border radii for each corner.

        Args:
            top_left: top-left radius in points
            top_right: top-right radius in points
            bottom_right: bottom-right radius in points
            bottom_left: bottom-left radius in points

        Returns:
            this div, for chaining
        """
        return lib.folio_div_set_border_radius_per_corner(
            self._handle,
            ct.c_double(top_left),
            ct.c_double(top_right),
            ct.c_double(bottom_right),
            ct.c_double(bottom_left),
        )

    @_with_error_handling(DivException)
    def hcenter(self, enabled: bool) -> _ErrorCode:
        """
        Centers this div horizontally within its container.

        Args:
            enabled: whether to apply horizontal centering

        Returns:
            this div, for chaining
        """
        return lib.folio_div_set_hcenter(self._handle, ct.c_int32(enabled))

    @_with_error_handling(DivException)
    def hright(self, enabled: bool) -> _ErrorCode:
        """
        Right-aligns this div within its container.

        Args:
            enabled: whether to right-align

        Returns:
            this div, for chaining
        """
        return lib.folio_div_set_hright(self._handle, ct.c_int32(enabled))

    @_with_error_handling(DivException)
    def clear(self, value: Literal["left", "right", "both"]) -> _ErrorCode:
        """
        Sets the CSS-style `clear` property for this div.

        Args:
            value: one of `left`,`right` or, `both`

        Returns:
            this div, for chaining
        """
        return lib.folio_div_set_clear(self._handle, ct.c_char_p(value.encode()))

    @_with_error_handling(DivException)
    def outline(
        self,
        width: float,
        style: Literal[
            "none",
            "hidden",
            "solid",
            "dotted",
            "dashed",
            "double",
            "groove",
            "ridge",
            "inset",
            "outset",
        ],
        color: Color,
        offset: float,
    ) -> _ErrorCode:
        """
        Draws an outline around this div that sits outside the border box.

        Args:
            width: width in points
            style: outline style (e.g., `"solid"`, `"dashed"`)
            color: outline color `Color`
            offset: outline offset from the border box

        Returns:
            this div, for chaining
        """
        return lib.folio_div_set_outline(
            self._handle,
            ct.c_double(width),
            ct.c_char_p(style.encode()),
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
            ct.c_double(offset),
        )

    @_with_error_handling(DivException)
    def add_box_shadow(
        self,
        offset_x: float,
        offset_y: float,
        blur: float,
        spread: float,
        color: Color,
    ) -> _ErrorCode:
        """
        Adds a box shadow to this div. Multiple shadows may be layered
        with repeated calls.

        Args:
            offset_x: horizontal offset in points
            offset_y: Vertical offset in points
            blur: blur radius in points
            spread: spread radius in points
            color: the color of the box shadow

        Returns:
            this div, for chaining
        """
        return lib.folio_div_add_box_shadow(
            self._handle,
            ct.c_double(offset_x),
            ct.c_double(offset_y),
            ct.c_double(blur),
            ct.c_double(spread),
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    @_with_error_handling(DivException)
    def space_before(self, pts: float) -> _ErrorCode:
        """
        Sets the amount of vertical space to add before this div.

        Args:
            pts: space before in points

        Returns:
            this div, for chaining
        """
        return lib.folio_div_set_space_before(self._handle, ct.c_double(pts))

    @_with_error_handling(DivException)
    def space_after(self, pts: float) -> _ErrorCode:
        """
        Sets the amount of vertical space to add before this div.

        Args:
            pts: space after in points

        Returns:
            this div, for chaining
        """
        return lib.folio_div_set_space_after(self._handle, ct.c_double(pts))

    @_with_error_handling(DivException)
    def border_radius(self, radius: float) -> _ErrorCode:
        """
        Sets the corner radius for rounded borders on this div.

        Args:
            radius: border radius in points

        Returns:
            this div, for chaining
        """
        return lib.folio_div_set_boarder_radius(self._handle, ct.c_double(radius))

    @_with_error_handling(DivException)
    def opacity(self, opacity: float) -> _ErrorCode:
        """
        Sets the opacity of this div and its contents.

        Args:
            opacity: opacity in the range `0.0 - 1.0`

        Returns:
            this div, for chaining
        """
        return lib.folio_div_set_opacity(self._handle, ct.c_double(opacity))

    @_with_error_handling(DivException)
    def overflow(self, mode: str) -> _ErrorCode:
        """
        Sets the overflow behaviour when content exceeds this div's bounds.

        Args:
            mode: overflow mode string (e.g., `"hidden"`)

        Returns:
            this div, for chaining
        """
        return lib.folio_div_set_overflow(self._handle, ct.c_char_p(mode.encode()))

    @_with_error_handling(DivException)
    def tag(self, tag: str) -> _ErrorCode:
        """
        Overrides the PDF/UA structure tag for this div (e.g., "Note", "Aside").

        Args:
            tag: the PDF structure tag name

        Returns:
            this div, for chaining
        """
        return lib.folio_div_set_tag(self._handle, ct.c_char_p(tag.encode()))

    @_with_error_handling(DivException)
    def box_shadow(
        self,
        offset_x: float,
        offset_y: float,
        blur: float,
        spread: float,
        color: Color,
    ) -> _ErrorCode:
        """
        Adds a drop shadow to this div.

        Args:
            offset_x: horizontal shadow offset in points
            offset_y: vertical shadow offset in points
            blur: blur radius in points
            spread: spread radius in points
            color: shadow `Color`

        Returns:
            this div, for chaining
        """
        return lib.folio_div_set_box_shadow(
            self._handle,
            ct.c_double(offset_x),
            ct.c_double(offset_y),
            ct.c_double(blur),
            ct.c_double(spread),
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    @_with_error_handling(DivException)
    def max_height(self, pts: float) -> _ErrorCode:
        """
        Sets the maximum height of this div in points.

        Args:
            pts: maximum height in points

        Returns:
            this div, for chaining
        """
        return lib.folio_div_set_max_height(self._handle, ct.c_double(pts))
