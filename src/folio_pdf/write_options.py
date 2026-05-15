"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.exceptions import WriteOptionsException


class WriteOptions(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self._write_options_handle = lib.folio_write_options_new()

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._write_options_handle)

    def close(self):
        lib.folio_write_options_free(self.handle)

    @_with_error_handling(WriteOptionsException)
    def use_xref_stream(self, enabled: bool):
        return lib.folio_write_options_set_use_xref_stream(
            self.handle, ct.c_int32(enabled)
        )

    @_with_error_handling(WriteOptionsException)
    def use_object_streams(self, enabled: bool):
        return lib.folio_write_options_set_use_object_streams(
            self.handle, ct.c_int32(enabled)
        )

    @_with_error_handling(WriteOptionsException)
    def object_stream_capacity(self, capacity: int):
        return lib.folio_write_options_set_object_stream_capacity(
            self.handle, ct.c_int32(capacity)
        )

    @_with_error_handling(WriteOptionsException)
    def orphan_sweep(self, enabled: bool):
        return lib.folio_write_options_set_orphan_sweep(
            self.handle, ct.c_int32(enabled)
        )

    @_with_error_handling(WriteOptionsException)
    def clean_content_streams(self, enabled: bool):
        return lib.folio_write_options_set_clean_content_streams(
            self.handle, ct.c_int32(enabled)
        )

    @_with_error_handling(WriteOptionsException)
    def deduplicate_objects(self, enabled: bool):
        return lib.folio_write_options_set_deduplicate_objects(
            self.handle, ct.c_int32(enabled)
        )

    @_with_error_handling(WriteOptionsException)
    def recompress_streams(self, enabled: bool):
        return lib.folio_write_options_set_recompress_streams(
            self.handle, ct.c_int32(enabled)
        )
