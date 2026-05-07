"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.enums import Alignments
from folio_pdf.exceptions import LinkException
from folio_pdf.font import Font


class Link(AbstractFolioObject):
    _requires_close = True

    def __init__(self, text: str, uri: str, font: Font, font_size: float):
        self._link_handle = lib.folio_link_new(
            ct.c_char_p(text.encode()),
            ct.c_char_p(uri.encode()),
            font.handle,
            ct.c_double(font_size),
        )

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._link_handle)

    def close(self):
        lib.folio_link_free(self.handle)

    @classmethod
    def new_embedded(cls, text: str, uri: str, font: Font, font_size: float):
        obj = cls.__new__(cls)
        obj._link_handle = lib.folio_link_new_embedded(
            ct.c_char_p(text.encode()),
            ct.c_char_p(uri.encode()),
            font.handle,
            ct.c_double(font_size),
        )
        return obj

    @classmethod
    def new_internal(cls, text: str, dest_name: str, font: Font, font_size: float):
        obj = cls.__new__(cls)
        obj._link_handle = lib.folio_link_new_internal(
            ct.c_char_p(text.encode()),
            ct.c_char_p(dest_name.encode()),
            font.handle,
            ct.c_double(font_size),
        )

    @_with_error_handling(LinkException)
    def set_color(self, r: float, g: float, b: float):
        return lib.folio_link_set_color(
            self.handle, ct.c_double(r), ct.c_double(g), ct.c_double(b)
        )

    @_with_error_handling(LinkException)
    def set_underline(self):
        return lib.folio_link_set_underline(self.handle)

    @_with_error_handling(LinkException)
    def set_align(self, align: Alignments):
        return lib.folio_link_set_align(self.handle, ct.c_int32(align.value))
