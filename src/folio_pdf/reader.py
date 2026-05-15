"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct
from pathlib import Path

from folio_pdf.core import AbstractFolioObject, lib


class PDFReader(AbstractFolioObject):
    _requires_close = True

    def __init__(self, path: str | Path):
        _path = path
        if isinstance(_path, Path):
            _path = _path.as_posix()
        self.__handle = lib.folio_reader_open(ct.c_char_p(_path.encode()))

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)

    def close(self):
        lib.folio_reader_free(self._handle)

    @classmethod
    def parse(cls, data: bytes):
        obj = cls.__new__(cls)
        obj._reader_handle = lib.folo_reader_parse(
            ct.c_char_p(data), ct.c_int32(len(data))
        )
        return obj

    @property
    def page_count(self):
        return lib.folio_reader_page_count(self._handle)

    @property
    def version(self):
        buf = lib.folio_reader_version(self._handle)
        return self._read_from_obj_buffer(buf)

    @property
    def info_title(self):
        buf = lib.folio_reader_info_title(self._handle)
        return self._read_from_obj_buffer(buf)

    @property
    def info_author(self):
        buf = lib.folio_reader_info_author(self._handle)
        return self._read_from_obj_buffer(buf)

    def extract_text(self):
        buf = lib.folio_reader_extract_text(self._handle)
        return self._read_from_obj_buffer(buf)

    def page_width(self, page_index: int):
        return lib.folio_reader_page_width(self._handle, ct.c_int32(page_index))

    def page_height(self, page_index: int):
        return lib.folio_reader_page_height(self._handle, ct.c_int32(page_index))

    def structure_tree(self):
        buf = lib.folio_reader_structure_tree(self._handle)
        return self._read_from_obj_buffer(buf)

    def text_spans(self, page_index: int):
        buf = lib.folio_reader_text_spans(self._handle, ct.c_int32(page_index))
        return self._read_from_obj_buffer(buf)

    def images(self, page_index: int):
        buf = lib.folio_reader_images(self._handle, ct.c_int32(page_index))
        return self._read_from_obj_buffer(buf)

    def paths(self, page_index: int):
        buf = lib.folio_reader_paths(self._handle, ct.c_int32(page_index))
        return self._read_from_obj_buffer(buf)
