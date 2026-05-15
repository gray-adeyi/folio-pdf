"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.color import Color
from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.exceptions import FormFieldException


class FormField(AbstractFolioObject):
    _requires_close = True

    def __init__(
        self, name: str, x1: float, y1: float, x2: float, y2: float, page_index: int
    ):
        self.__handle = lib.folio_form_create_text_field(
            ct.c_char_p(name.encode()),
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_int32(page_index),
        )

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)

    def close(self):
        lib.folio_form_field_free(self._handle)

    @classmethod
    def create_checkbox(
        cls,
        name: str,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        page_index: int,
        checked: bool,
    ):
        obj = cls.__new__(cls)
        obj._form_field_handle = lib.folio_form_create_checkbox(
            ct.c_char_p(name.encode()),
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_int32(page_index),
            ct.c_int32(checked),
        )
        return obj

    @_with_error_handling(FormFieldException)
    def value(self, value: str):
        return lib.folio_form_field_set_value(ct.c_char_p(value.encode()))

    @_with_error_handling(FormFieldException)
    def read_only(self):
        return lib.folio_form_field_set_read_only()

    @_with_error_handling(FormFieldException)
    def required(self):
        return lib.folio_form_field_set_required()

    @_with_error_handling(FormFieldException)
    def background_color(self, color: Color):
        return lib.folio_form_field_set_background_color(
            self._handle,
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    @_with_error_handling(FormFieldException)
    def border_color(self, color: Color):
        return lib.folio_form_field_set_border_color(
            self._handle,
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )
