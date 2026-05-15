"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.exceptions import FormFillerException
from folio_pdf.reader import PDFReader


class FormFiller(AbstractFolioObject):
    _requires_close = True

    def __init__(self, reader: PDFReader):
        self.__handle = lib.folio_form_filler_new(reader._handle)

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)

    def close(self):
        lib.folio_form_filler_free(self._handle)

    def field_names(self):
        buf = lib.folio_form_filler_field_names(self._handle)
        return self._read_from_obj_buffer(buf)

    def get_value(self, field_name: str):
        buf = lib.folio_form_filler_get_value(
            self._handle, ct.c_char_p(field_name.encode())
        )
        return self._read_from_obj_buffer(buf)

    @_with_error_handling(FormFillerException)
    def value(self, field_name: str, value: str):
        return lib.folio_form_filler_set_value(
            self._handle, ct.c_char_p(field_name.encode()), ct.c_char_p(value.encode())
        )

    @_with_error_handling(FormFillerException)
    def checkbox(self, field_name: str, checked: bool):
        return lib.folio_form_filler_set_checkbox(
            self._handle, ct.c_char_p(field_name.encode()), ct.c_int32(checked)
        )
