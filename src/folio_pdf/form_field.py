"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, lib


class FormField(AbstractFolioObject):
    _requires_close = True

    def __init__(
        self, name: str, x1: float, y1: float, x2: float, y2: float, page_index: int
    ):
        self._form_field_handle = lib.folio_form_create_text_field(
            ct.c_char_p(name.encode()),
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_int32(page_index),
        )

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._form_field_handle)

    def close(self):
        lib.folio_form_field_free(self.handle)

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
