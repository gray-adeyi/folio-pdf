"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.exceptions import FormException
from folio_pdf.form_field import FormField


class Form(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self._form_handle = lib.folio_form_new()

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._form_handle)

    def close(self):
        lib.folio_form_free(self.handle)

    @_with_error_handling(FormException)
    def add_text_field(
        self, name: str, x1: float, y1: float, x2: float, y2: float, page_index: int
    ):
        return lib.folio_form_add_text_field(
            self.handle,
            ct.c_char_p(name.encode()),
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_int32(page_index),
        )

    @_with_error_handling(FormException)
    def add_checkbox(
        self,
        name: str,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        page_index: int,
        checked: bool,
    ):
        return lib.folio_form_add_checkbox(
            self.handle,
            ct.c_char_p(name.encode()),
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_int32(page_index),
            ct.c_int32(checked),
        )

    @_with_error_handling(FormException)
    def add_dropdown(
        self,
        name: str,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        page_index: int,
        options: list[str],
    ):
        CharPArray = ct.c_char_p * len(options)
        return lib.folio_form_add_dropdown(
            self.handle,
            ct.c_char_p(name.encode()),
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_int32(page_index),
            CharPArray(options),
            len(options),
        )

    @_with_error_handling(FormException)
    def add_signature(
        self,
        name: str,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        page_index: int,
    ):
        return lib.folio_form_add_signature(
            self.handle,
            ct.c_char_p(name.encode()),
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_int32(page_index),
        )

    @_with_error_handling(FormException)
    def add_multiline_text_field(
        self,
        name: str,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        page_index: int,
    ):
        return lib.folio_form_add_multiline_text_field(
            self.handle,
            ct.c_char_p(name.encode()),
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_int32(page_index),
        )

    @_with_error_handling(FormException)
    def add_password_field(
        self,
        name: str,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        page_index: int,
    ):
        return lib.folio_form_add_password_field(
            self.handle,
            ct.c_char_p(name.encode()),
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_int32(page_index),
        )

    @_with_error_handling(FormException)
    def add_listbox(
        self,
        name: str,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        page_index: int,
        options: list[str],
    ):
        CharPArray = ct.c_char_p * len(options)
        return lib.folio_form_add_listbox(
            self.handle,
            ct.c_char_p(name.encode()),
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_int32(page_index),
            CharPArray(options),
            ct.c_int32(len(options)),
        )

    def add_radio_group(self): ...

    @_with_error_handling(FormException)
    def add_field(self, field: FormField):
        return lib.folio_form_add_field(self.handle, field.handle)
