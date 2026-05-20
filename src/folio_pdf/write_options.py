"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.exceptions import WriteOptionsException

lib.folio_write_options_new.argtypes = []
lib.folio_write_options_new.restype = ct.c_uint64

lib.folio_write_options_free.argtypes = [ct.c_ushort]
lib.folio_write_options_free.restype = None

lib.folio_write_options_set_use_xref_stream.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_write_options_set_use_xref_stream.restype = ct.c_int32

lib.folio_write_options_set_use_object_streams.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_write_options_set_use_object_streams.restype = ct.c_int32

lib.folio_write_options_set_orphan_sweep.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_write_options_set_orphan_sweep.restype = ct.c_int32

lib.folio_write_options_set_clean_content_streams.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_write_options_set_clean_content_streams.restype = ct.c_int32

lib.folio_write_options_set_deduplicate_objects.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_write_options_set_deduplicate_objects.restype = ct.c_int32

lib.folio_write_options_set_recompress_streams.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_write_options_set_recompress_streams.restype = ct.c_int32


class WriteOptions(AbstractFolioObject):
    """
    Configuration for the writer optimizer used by
    `Document.save_with_options` and
    `Document.to_buffer_with_options`.
    """

    _requires_close = True

    def __init__(self):
        self.__handle = lib.folio_write_options_new()

    @_with_error_handling(WriteOptionsException)
    def use_xref_stream(self, enabled: bool) -> "WriteOptions":
        """
        Toggles emission of a cross-reference stream
        (ISO 32000-1 §7.5.8) in place of a classic {@code xref} table
        (§7.5.4).

        Args:
            enabled: `True` to write a cross-reference stream

        Returns:
            this instance, for chaining
        """
        return lib.folio_write_options_set_use_xref_stream(
            self._handle, ct.c_int32(enabled)
        )

    @_with_error_handling(WriteOptionsException)
    def use_object_streams(self, enabled: bool) -> "WriteOptions":
        """
        Toggles packing indirect objects into compressed object streams
        (ISO 32000-1 §7.5.7). Implies `use_xref_stream`.

        Args:
         * @param enabled `True` to use object streams

        Returns:
            this instance, for chaining
        """
        return lib.folio_write_options_set_use_object_streams(
            self._handle, ct.c_int32(enabled)
        )

    @_with_error_handling(WriteOptionsException)
    def object_stream_capacity(self, capacity: int) -> "WriteOptions":
        """
        Sets the maximum number of indirect objects packed into a single
        object stream (ISO 32000-1 §7.5.7).

        Args:
            capacity: the per-stream object capacity (must be positive)

        Returns:
            this instance, for chaining
        """
        return lib.folio_write_options_set_object_stream_capacity(
            self._handle, ct.c_int32(capacity)
        )

    @_with_error_handling(WriteOptionsException)
    def orphan_sweep(self, enabled: bool) -> "WriteOptions":
        """
        Toggles dropping indirect objects that are unreachable from the
        document catalog (ISO 32000-1 §7.7.2) before writing.

        Args:
            enabled: `True` to remove orphan objects

        Returns:
            this instance, for chaining
        """
        return lib.folio_write_options_set_orphan_sweep(
            self._handle, ct.c_int32(enabled)
        )

    @_with_error_handling(WriteOptionsException)
    def clean_content_streams(self, enabled: bool) -> "WriteOptions":
        """
        Toggles normalizing and recompressing content streams
        (ISO 32000-1 §7.8) prior to writing.

        Args:
            enabled: `True` to clean content streams

        Returns:
            this instance, for chaining
        """
        return lib.folio_write_options_set_clean_content_streams(
            self._handle, ct.c_int32(enabled)
        )

    @_with_error_handling(WriteOptionsException)
    def deduplicate_objects(self, enabled: bool) -> "WriteOptions":
        """
        Toggles merging of byte-identical indirect objects so they share a
        single object number (ISO 32000-1 §7.3.10).

        Args:
            enabled: `True` to deduplicate objects

        Returns:
            this instance, for chaining
        """
        return lib.folio_write_options_set_deduplicate_objects(
            self._handle, ct.c_int32(enabled)
        )

    @_with_error_handling(WriteOptionsException)
    def recompress_streams(self, enabled: bool) -> "WriteOptions":
        """
        Toggles re-encoding existing flate streams with higher compression
        during the write pass.

        Args:
            enabled: `True` to recompress existing streams

        Returns:
            this instance, for chaining
        """
        return lib.folio_write_options_set_recompress_streams(
            self._handle, ct.c_int32(enabled)
        )

    def close(self):
        lib.folio_write_options_free(self._handle)

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)
