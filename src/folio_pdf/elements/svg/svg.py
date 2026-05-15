"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, lib


class SVG(AbstractFolioObject):
    _requires_close = True

    def __init__(self, svg_xml: str):
        self._svg_handle = lib.folio_svg_parse(ct.c_char_p(svg_xml.encode()))

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._svg_handle)

    def close(self):
        lib.folio_svg_free(self.handle)

    @classmethod
    def parse_bytes(cls, data: bytes):
        obj = cls.__new__(cls)
        obj._svg_handle = lib.folio_svg_parse_bytes(
            ct.c_char_p(data), ct.c_int32(len(data))
        )
        return obj

    @property
    def width(self):
        return lib.folio_svg_width(self.handle)

    @property
    def height(self):
        return lib.folio_svg_height(self.handle)
