"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct
import sys

from folio_pdf.core import AbstractFolioObject, lib

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


lib.folio_svg_parse.argtypes = [ct.c_char_p]
lib.folio_svg_parse.restype = ct.c_uint64

lib.folio_svg_parse_bytes.argtypes = [ct.c_void_p, ct.c_int32]
lib.folio_svg_parse_bytes.restype = ct.c_uint64

lib.folio_svg_width.argtypes = [ct.c_uint64]
lib.folio_svg_width.restype = ct.c_double

lib.folio_svg_height.argtypes = [ct.c_uint64]
lib.folio_svg_height.restype = ct.c_double

lib.folio_svg_free.argtypes = [ct.c_uint64]
lib.folio_svg_free.restype = None


class SVG(AbstractFolioObject):
    """
    A representation of an SVG, that can be passed to an `SVGElement` which
    can then be added to a `Document` or `Div`
    """

    _requires_close = True
    _binding_resource_free_fn = lib.folio_svg_free

    def __init__(self, svg_xml: str):
        """
        Parses an SVG document from an XML string.

        Args:
            svg_xml: the SVG XML content as a string

        Returns:
            a new `SVG` instance
        """
        self._is_closed = False
        self.__handle = lib.folio_svg_parse(ct.c_char_p(svg_xml.encode()))

    @classmethod
    def parse_bytes(cls, data: bytes) -> Self:
        """
        Parses an SVG document from raw bytes and creates a document element.

        Args:
            data: the SVG content as a byte array

        Returns:
            a new `SVG` instance
        """
        obj = cls.__new__(cls)
        obj._is_closed = False
        obj.__handle = lib.folio_svg_parse_bytes(
            ct.c_char_p(data), ct.c_int32(len(data))
        )
        return obj

    @property
    def width(self) -> float:
        """
        Returns the intrinsic width declared in the SVG source, in points.

        Returns:
            the SVG's natural width
        """
        return lib.folio_svg_width(self._handle)

    @property
    def height(self) -> float:
        """
        Returns the intrinsic height declared in the SVG source, in points.

        Returns:
            the SVG's natural height
        """
        return lib.folio_svg_height(self._handle)

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)
