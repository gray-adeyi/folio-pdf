"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.color import Color
from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.exceptions import RedactorOptionsException


class RedactorOptions(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self._redactor_options_handle = lib.folio_redact_opts_new()

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._redactor_options_handle)

    def close(self):
        lib.folio_redact_opts_free(self.handle)

    @_with_error_handling(RedactorOptionsException)
    def fill_color(self, color: Color):
        return lib.folio_redact_opts_set_fill_color(
            self.handle,
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    @_with_error_handling(RedactorOptionsException)
    def overlay(self, text: str, font_size: float, color: Color):
        return lib.folio_redact_opts_set_overlay(
            self.handle,
            ct.c_char_p(text.encode()),
            ct.c_double(font_size),
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    @_with_error_handling(RedactorOptionsException)
    def strip_metadata(self, strip: bool):
        return lib.folio_redact_opts_set_strip_metadata(self.handle, ct.c_int32(strip))
