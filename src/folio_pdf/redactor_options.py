"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.color import Color
from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.exceptions import RedactorOptionsException

lib.folio_redact_opts_new.argtypes = []
lib.folio_redact_opts_new.restype = ct.c_uint64

lib.folio_redact_opts_free.argtypes = [ct.c_uint64]
lib.folio_redact_opts_free.restype = None

lib.folio_redact_opts_set_fill_color.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_redact_opts_set_fill_color.restype = ct.c_int32

lib.folio_redact_opts_set_overlay.argtypes = [
    ct.c_uint64,
    ct.c_char_p,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_redact_opts_set_overlay.restype = ct.c_int32

lib.folio_redact_opts_set_strip_metadata.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_redact_opts_set_strip_metadata.restype = ct.c_int32


class RedactorOptions(AbstractFolioObject):
    """
    Configures how `PdfRedactor` blackouts are rendered — fill color,
    optional overlay text, and whether to strip document metadata.
    """

    _requires_close = True

    def __init__(self):
        self.__handle = lib.folio_redact_opts_new()

    @_with_error_handling(RedactorOptionsException)
    def fill_color(self, color: Color):
        """
        Sets the fill color for the redaction rectangles.

        Args:
            color: the color to use over the redacted areas

        Retuns:
            this options object, for chaining
        """
        return lib.folio_redact_opts_set_fill_color(
            self._handle,
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    @_with_error_handling(RedactorOptionsException)
    def overlay(self, text: str, font_size: float, color: Color):
        """
        Sets overlay text drawn on top of each redaction rectangle.

        Args:
            text: the overlay label (e.g., `"REDACTED"`)
            font_size: font size in points
            color: background color for the redacted areas

        Returns:
            this options object, for chaining
        """
        return lib.folio_redact_opts_set_overlay(
            self._handle,
            ct.c_char_p(text.encode()),
            ct.c_double(font_size),
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    @_with_error_handling(RedactorOptionsException)
    def strip_metadata(self, strip: bool):
        """
        Controls whether document metadata (author, title, etc.) is stripped.

        Args:
            strip: `True` to remove metadata from the redacted output

        Returns:
            this options object, for chaining
        """
        return lib.folio_redact_opts_set_strip_metadata(self._handle, ct.c_int32(strip))

    def close(self):
        lib.folio_redact_opts_free(self._handle)

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)
