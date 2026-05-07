"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.enums import Alignments
from folio_pdf.exceptions import SVGElementException
from folio_pdf.svg import SVG


class SVGElement(AbstractFolioObject):
    _requires_close = True

    def __init__(self, svg: SVG):
        self._svg_element_handle = lib.folio_svg_element_new(svg.handle)

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._svg_element_handle)

    def close(self):
        lib.folio_svg_element_free(self.handle)

    @_with_error_handling(SVGElementException)
    def set_size(self, w: float, h: float):
        return lib.folio_svg_element_set_size(
            self.handle, ct.c_double(w), ct.c_double(h)
        )

    @_with_error_handling(SVGElementException)
    def set_align(self, align: Alignments):
        return lib.folio_svg_element_set_align(self.handle, ct.c_int32(align.value))

    @_with_error_handling(SVGElementException)
    def set_alt_text(self, text: str):
        return lib.folio_svg_element_set_alt_text(
            self.handle, ct.c_char_p(text.encode())
        )
