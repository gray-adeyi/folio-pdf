"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.exceptions import FormFillerException
from folio_pdf.reader import PDFReader

_ErrorCode = int

lib.folio_form_filler_new.argtypes = [ct.c_uint64]
lib.folio_form_filler_new.restype = ct.c_uint64

lib.folio_form_filler_free.argtypes = [ct.c_uint64]
lib.folio_form_filler_free.restype = None

lib.folio_form_filler_field_names.argtypes = [ct.c_uint64]
lib.folio_form_filler_field_names.restype = ct.c_uint64

lib.folio_form_filler_get_value.argtypes = [ct.c_uint64, ct.c_char_p]
lib.folio_form_filler_get_value.restype = ct.c_uint64

lib.folio_form_filler_set_value.argtypes = [ct.c_uint64, ct.c_char_p, ct.c_char_p]
lib.folio_form_filler_set_value.restype = ct.c_int32

lib.folio_form_filler_set_checkbox.argtypes = [ct.c_uint64, ct.c_char_p, ct.c_int32]
lib.folio_form_filler_set_checkbox.restype = ct.c_int32


class FormFiller(AbstractFolioObject):
    """
    Fills interactive form fields in an existing PDF.
    """

    _requires_close = True
    _binding_resource_free_fn = lib.folio_form_filler_free

    def __init__(self, reader: PDFReader):
        self._is_closed = False
        self.__handle = lib.folio_form_filler_new(reader._handle)

    def field_names(self) -> str:
        """
        Returns a newline-separated list of all form field names in the PDF.

        Returns:
            field names as a single string
        """
        buf = lib.folio_form_filler_field_names(self._handle)
        return str(self._read_from_obj_buffer(buf))

    def get_value(self, field_name: str) -> str:
        """
        Returns the current value of the named form field.

        Args:
            field_name: the form field name

        Returns:
            the current value, or an empty string if the field is empty
        """
        buf = lib.folio_form_filler_get_value(
            self._handle, ct.c_char_p(field_name.encode())
        )
        return str(self._read_from_obj_buffer(buf))

    @_with_error_handling(FormFillerException)
    def value(self, field_name: str, value: str) -> _ErrorCode:
        """
        Sets the value of a text form field.

        Args:
            field_name: the form field name
            value: the new value to set

        Returns:
            this filler, for chaining
        """
        return lib.folio_form_filler_set_value(
            self._handle, ct.c_char_p(field_name.encode()), ct.c_char_p(value.encode())
        )

    @_with_error_handling(FormFillerException)
    def checkbox(self, field_name: str, checked: bool) -> _ErrorCode:
        """
        Sets the checked state of a checkbox form field.

        Args:
            field_name: the checkbox field name
            checked: `True` to check, `False` to uncheck

        Returns:
            this filler, for chaining
        """
        return lib.folio_form_filler_set_checkbox(
            self._handle, ct.c_char_p(field_name.encode()), ct.c_int32(checked)
        )

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)
