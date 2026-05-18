"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.color import Color
from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.enums import Alignments
from folio_pdf.exceptions import LinkException
from folio_pdf.font import Font

lib.folio_link_new.argtypes = [ct.c_char_p, ct.c_char_p, ct.c_uint64, ct.c_double]
lib.folio_link_new.restype = ct.c_uint64

lib.folio_link_new_embedded.argtypes = [
    ct.c_char_p,
    ct.c_char_p,
    ct.c_uint64,
    ct.c_double,
]
lib.folio_link_new_embedded.restype = ct.c_uint64

lib.folio_link_new_internal.argtypes = [
    ct.c_char_p,
    ct.c_char_p,
    ct.c_uint64,
    ct.c_double,
]
lib.folio_link_new_internal.restype = ct.c_uint64

lib.folio_link_free.argtypes = [ct.c_uint64]
lib.folio_link_free.restype = None

lib.folio_link_set_color.argtypes = [ct.c_uint64, ct.c_double, ct.c_double, ct.c_double]
lib.folio_link_set_color.restype = ct.c_int32

lib.folio_link_set_underline.argtypes = [ct.c_uint64]
lib.folio_link_set_underline.restype = ct.c_int32

lib.folio_link_set_align.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_link_set_align.restype = ct.c_int32


class Link(AbstractFolioObject):
    """
    A clickable hyperlink element that can be added to a document.

    Supports external URIs, file-embedded links, and internal named-destination links.
    """

    _requires_close = True

    def __init__(self, text: str, uri: str, font: Font, font_size: float):
        self.__handle = lib.folio_link_new(
            ct.c_char_p(text.encode()),
            ct.c_char_p(uri.encode()),
            font._handle,
            ct.c_double(font_size),
        )

    @classmethod
    def new_embedded(cls, text: str, uri: str, font: Font, font_size: float) -> "Link":
        """
        Creates a link using an embedded (subset) font.

        Args:
            text: the visible link text
            uri: the target URI
            font: the embedded font
            font_size: the font size in points

        Returns:
            a new `Link` instance
        """
        obj = cls.__new__(cls)
        obj.__handle = lib.folio_link_new_embedded(
            ct.c_char_p(text.encode()),
            ct.c_char_p(uri.encode()),
            font._handle,
            ct.c_double(font_size),
        )
        return obj

    @classmethod
    def new_internal(
        cls, text: str, dest_name: str, font: Font, font_size: float
    ) -> "Link":
        """
        Creates an internal link that navigates to a named destination within
        the same document.

        Args:
            text: the visible link text
            dest_name: the name of the destination anchor in the document
            font: the font to use for the link text
            font_size: the font size in points

        Returns:
            a new `Link` instance
        """
        obj = cls.__new__(cls)
        obj.__handle = lib.folio_link_new_internal(
            ct.c_char_p(text.encode()),
            ct.c_char_p(dest_name.encode()),
            font._handle,
            ct.c_double(font_size),
        )
        return obj

    @_with_error_handling(LinkException)
    def color(self, color: Color) -> "Link":
        """
        Sets the text color of the link.

        Args:
            color: the RGB color to apply

        Returns:
            this instance for chaining
        """
        return lib.folio_link_set_color(
            self._handle,
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    @_with_error_handling(LinkException)
    def underline(self) -> "Link":
        """
        Enables underlining for the link text.

        Returns:
            this instance for chaining
        """
        return lib.folio_link_set_underline(self._handle)

    @_with_error_handling(LinkException)
    def align(self, align: Alignments) -> "Link":
        """
        Sets the horizontal alignment of the link within its container.

        Args:
            align: the desired alignment

        Returns:
            this instance for chaining
        """
        return lib.folio_link_set_align(self._handle, ct.c_int32(align.value))

    def close(self):
        lib.folio_link_free(self._handle)

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)
