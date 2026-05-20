"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.enums import Alignments
from folio_pdf.exceptions import SVGElementException

from .svg import SVG

lib.folio_svg_element_new.argtypes = [ct.c_uint64]
lib.folio_svg_element_new.restype = ct.c_uint64

lib.folio_svg_element_set_size.argtypes = [ct.c_uint64, ct.c_double, ct.c_double]
lib.folio_svg_element_set_size.restype = ct.c_int32

lib.folio_svg_element_set_align.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_svg_element_set_align.restype = ct.c_int32

lib.folio_svg_element_set_alt_text.argtypes = [ct.c_uint64, ct.c_char_p]
lib.folio_svg_element_set_alt_text.restype = ct.c_int32

lib.folio_svg_element_free.argtypes = [ct.c_uint64]
lib.folio_svg_element_free.restype = None


class SVGElement(AbstractFolioObject):
    """
    An SVG image element that renders vector graphics into a PDF document.
    """

    _requires_close = True

    def __init__(self, svg: SVG):
        self.__handle = lib.folio_svg_element_new(svg._handle)

    @_with_error_handling(SVGElementException)
    def size(self, w: float, h: float) -> "SVGElement":
        """
        Sets the rendered dimensions of this SVG element in points.

        Args:
            width: the desired width in points
            height: the desired height in points

        Returns:
            this instance for chaining
        """
        return lib.folio_svg_element_set_size(
            self._handle, ct.c_double(w), ct.c_double(h)
        )

    @_with_error_handling(SVGElementException)
    def align(self, align: Alignments) -> "SVGElement":
        """
        Sets the horizontal alignment of this SVG element within its container.

        Args:
            align: the desired alignment

        Returns:
            this instance for chaining
        """
        return lib.folio_svg_element_set_align(self._handle, ct.c_int32(align.value))

    @_with_error_handling(SVGElementException)
    def alt_text(self, text: str) -> "SVGElement":
        """Sets alternative text for PDF/UA accessibility.

        Args:
            text: the alternative text

        Returns:
            this svg element, for chaining
        """
        return lib.folio_svg_element_set_alt_text(
            self._handle, ct.c_char_p(text.encode())
        )

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)

    def close(self):
        lib.folio_svg_element_free(self._handle)
