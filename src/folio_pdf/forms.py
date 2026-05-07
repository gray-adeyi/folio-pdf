"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, lib
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

    def add_text_field(self): ...

    def add_checkbox(self): ...

    def add_dropdown(self): ...

    def add_signature(self): ...

    def add_multiline_text_field(self): ...

    def add_password_field(self): ...

    def add_listbox(self): ...

    def add_radio_group(self): ...

    def add_field(self, field: FormField):
        return lib.folio_form_add_field(self.handle, field.handle)
