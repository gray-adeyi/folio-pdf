"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.color import Color
from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.elements import Image
from folio_pdf.exceptions import PageException
from folio_pdf.font import Font
from folio_pdf.page_importer import PageImporter

lib.folio_page_add_text.argtypes = [
    ct.c_uint64,
    ct.c_char_p,
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_page_add_text.restype = ct.c_int32

lib.folio_page_add_text_embedded.argtypes = [
    ct.c_uint64,
    ct.c_char_p,
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_page_add_text_embedded.restype = ct.c_int32

lib.folio_page_add_image.argtypes = [
    ct.c_uint64,
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_page_add_image.restype = ct.c_int32

lib.folio_page_add_link.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_char_p,
]
lib.folio_page_add_link.restype = ct.c_int32

lib.folio_page_add_internal_link.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_char_p,
]
lib.folio_page_add_internal_link.restype = ct.c_int32

lib.folio_page_add_text_annotation.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_char_p,
    ct.c_char_p,
]
lib.folio_page_add_text_annotation.restype = ct.c_int32

lib.folio_page_set_opacity.argtypes = [ct.c_uint64, ct.c_double]
lib.folio_page_set_opacity.restype = ct.c_int32

lib.folio_page_set_rotate.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_page_set_rotate.restype = ct.c_int32

lib.folio_page_set_crop_box.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_page_set_crop_box.restype = ct.c_int32

lib.folio_page_set_trim_box.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_page_set_trim_box.restype = ct.c_int32

lib.folio_page_set_trim_box.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_page_set_trim_box.restype = ct.c_int32

lib.folio_page_set_size.argtypes = [ct.c_uint64, ct.c_double, ct.c_double]
lib.folio_page_set_size.restype = ct.c_int32

lib.folio_page_add_page_link.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_int32,
]
lib.folio_page_add_page_link.restype = ct.c_int32

lib.folio_page_set_opacity_fill_stroke.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
]
lib.folio_page_set_opacity_fill_stroke.restype = ct.c_int32

lib.folio_page_add_highlight.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_int32,
]
lib.folio_page_add_highlight.restype = ct.c_int32

lib.folio_page_add_underline_annotation.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_int32,
]
lib.folio_page_add_underline_annotation.restype = ct.c_int32

lib.folio_page_add_squiggly.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_int32,
]
lib.folio_page_add_squiggly.restype = ct.c_int32

lib.folio_page_add_strikeout.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_int32,
]
lib.folio_page_add_strikeout.restype = ct.c_int32


lib.folio_page_import_apply.argtypes = [ct.c_uint64, ct.c_uint64]
lib.folio_page_import_apply.restype = ct.c_int32

lib.folio_page_add_line.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_page_add_line.restype = ct.c_int32

lib.folio_page_add_rect.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_page_add_rect.restype = ct.c_int32


lib.folio_page_add_rect_filled.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_page_add_rect_filled.restype = ct.c_int32


class Page(AbstractFolioObject):
    """
    Represents a single page within a `Document`, providing low-level absolute
    positioning for text, images, links, and annotations.
    """

    _requires_close = False

    def __init__(self):
        self.__handle = 0

    @_with_error_handling(PageException)
    def add_text(
        self, text: str, font: Font, size: float, x: float, y: float
    ) -> "Page":
        """
        Places text at an absolute position on this page using a standard font.

        Args:
            text: the text to draw
            font: the font to use
            size: the font size in points
            x: x coordinate in points from the left edge
            y: y coordinate in points from the bottom edge

        Returns:
            this page, for chaining
        """
        return lib.folio_page_add_text(
            self._handle,
            ct.c_char_p(text.encode()),
            font._handle,
            ct.c_double(size),
            ct.c_double(x),
            ct.c_double(y),
        )

    @_with_error_handling(PageException)
    def add_text_embedded(
        self, text: str, font: Font, size: float, x: float, y: float
    ) -> "Page":
        """
        Places text at an absolute position using a font whose subset is embedded.

        Args:
            text: the text to draw
            font: the font to embed
            size: the font size in points
            x: x coordinate in points from the left edge
            y: y coordinate in points from the bottom edge

        Returns:
            this page, for chaining
        """
        return lib.folio_page_add_text_embedded(
            self._handle,
            ct.c_char_p(text.encode()),
            font._handle,
            ct.c_double(size),
            ct.c_double(x),
            ct.c_double(y),
        )

    @_with_error_handling(PageException)
    def add_image(self, img: Image, x: float, y: float, w: float, h: float) -> "Page":
        """
        Draws an image at an absolute position and size on this page.

        Args:
            image: the image to draw
            x: x coordinate in points from the left edge
            y: y coordinate in points from the bottom edge
            width: display width in points
            height: display height in points

        Returns:
            this page, for chaining
        """
        return lib.folio_page_add_image(
            self._handle,
            img._handle,
            ct.c_double(x),
            ct.c_double(y),
            ct.c_double(w),
            ct.c_double(h),
        )

    @_with_error_handling(PageException)
    def add_link(self, x1: float, y1: float, x2: float, y2: float, uri: str) -> "Page":
        """
        Adds a URI hyperlink annotation over the specified rectangle.

        Args:
            x1: left coordinate in points
            y1: bottom coordinate in points
            x2: right coordinate in points
            y2: top coordinate in points
            uri: the target URI

        Returns:
            this page, for chaining
        """
        return lib.folio_page_add_link(
            self._handle,
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_char_p(uri.encode()),
        )

    @_with_error_handling(PageException)
    def add_internal_link(
        self, x1: float, y1: float, x2: float, y2: float, dest_name: str
    ) -> "Page":
        """
        Adds an internal link annotation that navigates to a named destination.

        Args:
            x1: left coordinate in points
            y1: bottom coordinate in points
            x2: right coordinate in points
            y2: top coordinate in points
            dest_name: the target named destination

        Returns:
            this page, for chaining
        """
        return lib.folio_page_add_internal_link(
            self._handle,
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_char_p(dest_name.encode()),
        )

    @_with_error_handling(PageException)
    def add_text_annotation(
        self, x1: float, y1: float, x2: float, y2: float, text: str, icon: str
    ) -> "Page":
        """
        Adds a text (sticky-note) annotation on this page.

        Args:
            x1: left coordinate in points
            y1: bottom coordinate in points
            x2: right coordinate in points
            y2: top coordinate in points
            text: the annotation content text
            icon: the icon name (e.g., {@code "Note"}, {@code "Comment"})

        Returns:
            this page, for chaining
        """
        return lib.folio_page_add_text_annotation(
            self._handle,
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_char_p(text.encode()),
            ct.c_char_p(icon.encode()),
        )

    @_with_error_handling(PageException)
    def opacity(self, alpha: float) -> "Page":
        """
        Sets a uniform opacity for all content drawn on this page.

        Args:
            alpha: opacity in the range `0.0 - 1.0`

        Returns:
            this page, for chaining
        """
        return lib.folio_page_set_opacity(self._handle, ct.c_double(alpha))

    @_with_error_handling(PageException)
    def rotate(self, degress: int) -> "Page":
        """
        Rotates this page by the given number of degrees (must be a multiple of 90).

        Args:
            degrees: rotation in degrees (e.g., 90, 180, 270)

        Returns:
            this page, for chaining
        """
        return lib.folio_page_set_rotate(self._handle, ct.c_int32(degress))

    @_with_error_handling(PageException)
    def crop_box(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
    ) -> "Page":
        """
        Sets the crop box for this page, defining the visible region.

        Args:
            x1: left coordinate in points
            y1: bottom coordinate in points
            x2: right coordinate in points
            y2: top coordinate in points

        Returns:
            this page, for chaining
        """
        return lib.folio_page_set_crop_box(
            self._handle,
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
        )

    @_with_error_handling(PageException)
    def trim_box(self, x1: float, y1: float, x2: float, y2: float) -> "Page":
        """
        Sets the trim box for this page, defining the intended
        final size after trimming.

        Args:
            x1: left coordinate in points
            y1: bottom coordinate in points
            x2: right coordinate in points
            y2: top coordinate in points

        Returns:
            this page, for chaining
        """
        return lib.folio_page_set_trim_box(
            self._handle,
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
        )

    @_with_error_handling(PageException)
    def bleed_box(self, x1: float, y1: float, x2: float, y2: float) -> "Page":
        """
        Sets the bleed box for this page, defining the region to
        which content may bleed.

        Args:
            x1: left coordinate in points
            y1: bottom coordinate in points
            x2: right coordinate in points
            y2: top coordinate in points

        Returns:
            this page, for chaining
        """
        return lib.folio_page_set_bleed_box(
            self._handle,
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
        )

    @_with_error_handling(PageException)
    def art_box(self, x1: float, y1: float, x2: float, y2: float) -> "Page":
        """
        Sets the art box for this page, defining the extent of meaningful content.

        Args:
            x1: left coordinate in points
            y1: bottom coordinate in points
            x2: right coordinate in points
            y2: top coordinate in points

        Returns:
            this page, for chaining
        """
        return lib.folio_page_set_art_box(
            self._handle,
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
        )

    @_with_error_handling(PageException)
    def size(self, width: float, height: float) -> "Page":
        """
        Sets the media box dimensions (page size) for this page.

        Args:
            width: page width in points
            height: page height in points

        Returns:
            this page, for chaining
        """
        return lib.folio_page_set_size(
            self._handle, ct.c_double(width), ct.c_double(height)
        )

    @_with_error_handling(PageException)
    def add_page_link(
        self, x1: float, y1: float, x2: float, y2: float, target_page: int
    ) -> "Page":
        """
        Adds a page-navigation link that jumps to another page in the document.

        Args:
            x1: left coordinate in points
            y1: bottom coordinate in points
            x2: right coordinate in points
            y2: top coordinate in points
            target_page: zero-based target page index

        Returns:
            this page, for chaining
        """
        return lib.folio_page_add_page_link(
            self._handle,
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_int32(target_page),
        )

    @_with_error_handling(PageException)
    def opacity_fill_stroke(self, fill_alpha: float, stroke_alpha: float) -> "Page":
        """
        Sets independent fill and stroke opacity for content drawn on this page.

        Args:
            fill_alpha: fill opacity in the range {@code [0.0, 1.0]}
            stroke_alpha: stroke opacity in the range {@code [0.0, 1.0]}

        Returns:
            this page, for chaining
        """
        return lib.folio_page_set_opacity(
            self._handle, ct.c_double(fill_alpha), ct.c_double(stroke_alpha)
        )

    @_with_error_handling(PageException)
    def add_highlight(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        color: Color,
        quad_points: list[float],
    ) -> "Page":
        """
        Adds a highlight markup annotation over the specified area.

        Args:
            x1: left coordinate in points
            y1: bottom coordinate in points
            x2: right coordinate in points
            y2: top coordinate in points
            color: the highlight `Color`
            quad_points: flat array of quad-point coordinates defining the
            highlighted region

        Returns:
            this page, for chaining
        """
        DoubleArray = ct.c_double * len(quad_points)
        return lib.folio_page_add_highlight(
            self._handle,
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
            DoubleArray(quad_points),
            ct.c_int32(len(quad_points)),
        )

    @_with_error_handling(PageException)
    def add_underline_annotation(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        color: Color,
        quad_points: list[float],
    ) -> "Page":
        """
        Adds an underline markup annotation over the specified area.

        Args:
            x1: left coordinate in points
            y1: bottom coordinate in points
            x2: right coordinate in points
            y2: top coordinate in points
            color: the underline {@link Color}
            quad_points: flat array of quad-point coordinates

        Returns:
            this page, for chaining
        """
        DoubleArray = ct.c_double * len(quad_points)
        return lib.folio_page_add_underline_annotation(
            self._handle,
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
            DoubleArray(quad_points),
            ct.c_int32(len(quad_points)),
        )

    @_with_error_handling(PageException)
    def add_squiggly(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        color: Color,
        quad_points: list[float],
    ) -> "Page":
        """
        Adds a squiggly underline markup annotation over the specified area.

        Args:
            x1: left coordinate in points
            y1: bottom coordinate in points
            x2: right coordinate in points
            y2: top coordinate in points
            color: the squiggly line {@link Color}
            quad_points: flat array of quad-point coordinates

        Returns:
            this page, for chaining
        """
        DoubleArray = ct.c_double * len(quad_points)
        return lib.folio_page_add_squiggly(
            self._handle,
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
            DoubleArray(quad_points),
            ct.c_int32(len(quad_points)),
        )

    @_with_error_handling(PageException)
    def add_strikeout(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        color: Color,
        quad_points: list[float],
    ) -> "Page":
        """
        Adds a strikeout markup annotation over the specified area.

        Args:
            x1: left coordinate in points
            y1: bottom coordinate in points
            x2: right coordinate in points
            y2: top coordinate in points
            color: the strikeout line {@link Color}
            quad_points: flat array of quad-point coordinates

        Returns:
            this page, for chaining
        """
        DoubleArray = ct.c_double * len(quad_points)
        return lib.folio_page_add_strikeout(
            self._handle,
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
            DoubleArray(quad_points),
            ct.c_int32(len(quad_points)),
        )

    @_with_error_handling(PageException)
    def import_apply(self, imp: PageImporter) -> "Page":
        """
        Stamps the imported page content onto this page.

        Args:
            imp: the page importer with the imported page content

        Returns:
            this page, for chaining
        """
        return lib.folio_page_import_apply(self._handle, imp._handle)

    @_with_error_handling(PageException)
    def add_line(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        width: float,
        color: Color,
    ) -> "Page":
        """
        Draws a straight line between two points on this page.

        Args:
            x1: start x coordinate in points
            y1: start y coordinate in points
            x2: end x coordinate in points
            y2: end y coordinate in points
            width: line width in points
            color: the color of the line

        Returns:
            this page, for chaining
        """
        return lib.folio_page_add_line(
            self._handle,
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_double(width),
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    @_with_error_handling(PageException)
    def add_rect(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        stroke_width: float,
        color: Color,
    ) -> "Page":
        """
        Draws a stroked rectangle on this page.

        Args:
            x: left coordinate in points
            y: bottom coordinate in points
            w: width in points
            h: height in points
            stroke_width: stroke width in points
            color: the stroke color

        Returns:
            this page, for chaining
        """
        return lib.folio_page_add_rect(
            self._handle,
            ct.c_double(x),
            ct.c_double(y),
            ct.c_double(w),
            ct.c_double(h),
            ct.c_double(stroke_width),
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    @_with_error_handling(PageException)
    def add_rect_filled(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        color: Color,
    ) -> "Page":
        """
        Draws a filled rectangle on this page.

        Args:
            x: left coordinate in points
            y: bottom coordinate in points
            w: width in points
            h: height in points
            color: fill color

        Returns:
            this page, for chaining
        """
        return lib.folio_page_add_rect_filled(
            self._handle,
            ct.c_double(x),
            ct.c_double(y),
            ct.c_double(w),
            ct.c_double(h),
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)

    @classmethod
    def _new_from_handle(cls, page_handle: int):
        obj = cls.__new__(cls)
        cls.__handle = page_handle
        return obj
