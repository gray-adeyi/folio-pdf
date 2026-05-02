"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

from folio_pdf.exceptions import WriteOptionsException

from folio_pdf.core import lib, _with_error_handling

from folio_pdf.object import AbstractFolioObject
import ctypes as ct


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
    def set_use_xref_stream(self, enabled: bool):
        return lib.folio_write_options_set_use_xref_stream(
            self.handle, ct.c_int32(enabled)
        )

    @_with_error_handling(WriteOptionsException)
    def set_use_object_streams(self, enabled: bool):
        return lib.folio_write_options_set_use_object_streams(
            self.handle, ct.c_int32(enabled)
        )

    @_with_error_handling(WriteOptionsException)
    def set_object_stream_capacity(self, capacity: int):
        return lib.folio_write_options_set_object_stream_capacity(
            self.handle, ct.c_int32(capacity)
        )

    @_with_error_handling(WriteOptionsException)
    def set_orphan_sweep(self, enabled: bool):
        return lib.folio_write_options_set_orphan_sweep(
            self.handle, ct.c_int32(enabled)
        )

    @_with_error_handling(WriteOptionsException)
    def set_clean_content_streams(self, enabled: bool):
        return lib.folio_write_options_set_clean_content_streams(
            self.handle, ct.c_int32(enabled)
        )

    @_with_error_handling(WriteOptionsException)
    def set_deduplicate_objects(self, enabled: bool):
        return lib.folio_write_options_set_deduplicate_objects(
            self.handle, ct.c_int32(enabled)
        )

    @_with_error_handling(WriteOptionsException)
    def set_recompress_streams(self, enabled: bool):
        return lib.folio_write_options_set_recompress_streams(
            self.handle, ct.c_int32(enabled)
        )
