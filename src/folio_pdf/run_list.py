"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.color import Color
from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.exceptions import RunListException
from folio_pdf.font import Font


class RunList(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self.__handle = lib.folio_run_list_new()

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)

    def close(self):
        lib.folio_run_list_free(self._handle)

    @_with_error_handling(RunListException)
    def add(self, text: str, font: Font, font_size: float, color: Color):
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
    ):
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
    def add_link(self, text: str, font: Font, font_size: float):
        return lib.folio_run_list_add_link(
            self._handle,
            ct.c_char_p(text.encode()),
            font._handle,
            ct.c_double(font_size),
        )

    @_with_error_handling(RunListException)
    def last_set_underline(self):
        return lib.folio_run_list_last_set_underline(self._handle)

    @_with_error_handling(RunListException)
    def last_set_strikethrough(self):
        return lib.folio_run_list_last_set_strikethrough(self._handle)

    @_with_error_handling(RunListException)
    def last_set_letter_spacing(self, spacing: float):
        return lib.folio_run_list_last_set_letter_spacing(
            self._handle, ct.c_double(spacing)
        )

    @_with_error_handling(RunListException)
    def last_set_background_color(self, color: Color):
        return lib.folio_run_list_last_set_background_color(
            self._handle,
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )
