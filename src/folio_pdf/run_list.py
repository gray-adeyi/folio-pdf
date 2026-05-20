"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.color import Color
from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.exceptions import RunListException
from folio_pdf.font import Font

lib.folio_run_list_new.argtypes = []
lib.folio_run_list_new.restype = ct.c_uint64

lib.folio_run_list_free.argtypes = [ct.c_uint64]
lib.folio_run_list_free.restype = None

lib.folio_run_list_add.argtypes = [
    ct.c_uint64,
    ct.c_char_p,
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_run_list_add.restype = ct.c_int32

lib.folio_run_list_add_embedded.argtypes = [
    ct.c_uint64,
    ct.c_char_p,
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_run_list_add_embedded.restype = ct.c_int32

lib.folio_run_list_add_link.argtypes = [
    ct.c_uint64,
    ct.c_char_p,
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_char_p,
    ct.c_int32,
]
lib.folio_run_list_add_link.restype = ct.c_int32

lib.folio_run_list_last_set_underline.argtypes = [ct.c_uint64]
lib.folio_run_list_last_set_underline.restype = ct.c_int32

lib.folio_run_list_last_set_strikethrough.argtypes = [ct.c_uint64]
lib.folio_run_list_last_set_strikethrough.restype = ct.c_int32

lib.folio_run_list_last_set_letter_spacing.argtypes = [ct.c_uint64, ct.c_double]
lib.folio_run_list_last_set_letter_spacing.restype = ct.c_int32

lib.folio_run_list_last_set_background_color.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_run_list_last_set_background_color.restype = ct.c_int32


class RunList(AbstractFolioObject):
    """
    Accumulates styled text runs for use with headings and list items.
    Supports mixed fonts, colors, links, and decorations within a single element.
    """

    _requires_close = True

    def __init__(self):
        self.__handle = lib.folio_run_list_new()

    @_with_error_handling(RunListException)
    def add(self, text: str, font: Font, font_size: float, color: Color) -> "RunList":
        """
        Appends a styled text run using a standard (non-embedded) font.

        Args:
            text: the text content for this run
            font: the font to render with
            font_size: the font size in points
            color: the text color

        Returns:
            this run list, for chaining
        """
        return lib.folio_run_list_add(
            self._handle,
            ct.c_char_p(text.encode()),
            font._handle,
            ct.c_double(font_size),
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    @_with_error_handling(RunListException)
    def add_embedded(
        self,
        text: str,
        font: Font,
        font_size: float,
        color: Color,
    ) -> "RunList":
        """
        Appends a styled text run using an embedded font subset.

        Args:
            text: the text content for this run
            font: the embedded font to render with
            font_size: the font size in points
            color: the text color

        Returns:
            this run list, for chaining
        """
        return lib.folio_run_list_add_embedded(
            self._handle,
            ct.c_char_p(text.encode()),
            font._handle,
            ct.c_double(font_size),
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    @_with_error_handling(RunListException)
    def add_link(
        self,
        text: str,
        font: Font,
        font_size: float,
        color: Color,
        uri: str,
        underline: bool,
    ) -> "RunList":
        """
        Appends a clickable link run.

        Args:
            text:      the visible link text
            font:      the font to render with
            fontSize:  the font size in points
            color:     the text color
            uri:       the target URI
            underline whether to draw an underline decoration

        Returns:
            this run list, for chaining
        """
        return lib.folio_run_list_add_link(
            self._handle,
            ct.c_char_p(text.encode()),
            font._handle,
            ct.c_double(font_size),
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
            ct.c_char_p(uri.encode()),
            ct.c_int32(underline),
        )

    @_with_error_handling(RunListException)
    def last_underline(self) -> "RunList":
        """
        Applies underline decoration to the last added run.

        Args:
            this run list, for chaining
        """
        return lib.folio_run_list_last_set_underline(self._handle)

    @_with_error_handling(RunListException)
    def last_strikethrough(self) -> "RunList":
        """
        Applies strikethrough decoration to the last added run.

        Args:
            this run list, for chaining
        """
        return lib.folio_run_list_last_set_strikethrough(self._handle)

    @_with_error_handling(RunListException)
    def last_letter_spacing(self, spacing: float) -> "RunList":
        """
        Sets letter spacing on the last added run.

        Args:
            spacing: the letter spacing in points

        Returns:
            this run list, for chaining
        """
        return lib.folio_run_list_last_set_letter_spacing(
            self._handle, ct.c_double(spacing)
        )

    @_with_error_handling(RunListException)
    def last_background_color(self, color: Color) -> "RunList":
        """
        Applies a highlight background color to the last added run.

        Args:
            color: the highlight color

        Returns:
            this run list, for chaining
        """
        return lib.folio_run_list_last_set_background_color(
            self._handle,
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    def close(self):
        lib.folio_run_list_free(self._handle)

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)
