"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

from folio_pdf.exceptions import RunListException

from folio_pdf.font import Font

from folio_pdf.object import AbstractFolioObject
from folio_pdf.core import lib, _with_error_handling
import ctypes as ct


class RunList(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self._run_list_handle = lib.folio_run_list_new()

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._run_list_handle)

    def close(self):
        lib.folio_run_list_free(self.handle)

    @_with_error_handling(RunListException)
    def add(
        self, text: str, font: Font, font_size: float, r: float, g: float, b: float
    ):
        return lib.folio_run_list_add(
            self.handle,
            ct.c_char_p(text.encode()),
            font.handle,
            ct.c_double(font_size),
            ct.c_double(r),
            ct.c_double(g),
            ct.c_double(b),
        )

    @_with_error_handling(RunListException)
    def add_embedded(
        self, text: str, font: Font, font_size: float, r: float, g: float, b: float
    ):
        return lib.folio_run_list_add_embedded(
            self.handle,
            ct.c_char_p(text.encode()),
            font.handle,
            ct.c_double(font_size),
            ct.c_double(r),
            ct.c_double(g),
            ct.c_double(b),
        )

    @_with_error_handling(RunListException)
    def add_link(self, text: str, font: Font, font_size: float):
        return lib.folio_run_list_add_link(
            self.handle, ct.c_char_p(text.encode()), font.handle, ct.c_double(font_size)
        )

    @_with_error_handling(RunListException)
    def last_set_underline(self):
        return lib.folio_run_list_last_set_underline(self.handle)

    @_with_error_handling(RunListException)
    def last_set_strikethrough(self):
        return lib.folio_run_list_last_set_strikethrough(self.handle)

    @_with_error_handling(RunListException)
    def last_set_letter_spacing(self, spacing: float):
        return lib.folio_run_list_last_set_letter_spacing(
            self.handle, ct.c_double(spacing)
        )

    @_with_error_handling(RunListException)
    def last_set_background_color(self, r: float, g: float, b: float):
        return lib.folio_run_list_last_set_background_color(
            self.handle, ct.c_double(r), ct.c_double(g), ct.c_double(b)
        )
