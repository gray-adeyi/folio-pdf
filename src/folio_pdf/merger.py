"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

from folio_pdf.exceptions import PDFMergerException

from io import BytesIO

from folio_pdf.font import Font

from pathlib import Path

from folio_pdf.reader import PDFReader

from folio_pdf.core import lib, _with_error_handling
from folio_pdf.object import AbstractFolioObject
import ctypes as ct


class PDFMerger(AbstractFolioObject):
    _requires_close = True

    def __init__(self, readers: list[PDFReader]):
        readers_handles = [reader.handle for reader in readers]
        UInt64Array = ct.c_uint64 * len(readers_handles)
        self._merger_handle = lib.folio_reader_merge(
            UInt64Array(readers_handles), ct.c_int32(len(readers_handles))
        )

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._merger_handle)

    def close(self):
        lib.folio_merge_free(self.handle)

    @classmethod
    def merge_files(cls, paths: list[str | Path]):
        obj = cls.__new__(cls)
        _paths = [path.as_posix() if isinstance(path, Path) else path for path in paths]
        CharPArray = ct.c_char_p * len(_paths)
        obj._merger_handle = lib.folio_merge_files(
            CharPArray(_paths), ct.c_int32(len(_paths))
        )
        return obj

    def set_info(self, title: str, author: str):
        return lib.folio_merge_set_info(
            ct.c_char_p(title.encode()),
            ct.c_char_p(author.encode()),
        )

    def add_blank_page(self, width: float, height: float):
        return lib.folio_merge_add_blank_page(ct.c_double(width), ct.c_double(height))

    def add_page_with_text(
        self,
        width: float,
        height: float,
        text: str,
        font: Font,
        font_size: float,
        x: float,
        y: float,
    ):
        return lib.folio_merge_add_page_with_text(
            ct.c_double(width),
            ct.c_double(height),
            ct.c_char_p(text.encode()),
            font.handle,
            ct.c_double(font_size),
            ct.c_double(x),
            ct.c_double(y),
        )

    @_with_error_handling(PDFMergerException)
    def save(self, path: str | Path):
        _path = path
        if isinstance(_path, Path):
            _path = _path.as_posix()
        return lib.folio_merge_save(self.handle, ct.c_char_p(_path.encode()))

    def write_to_buffer(self) -> BytesIO:
        buf = lib.folio_merge_write_to_buffer(self.handle)
        data = self._read_from_obj_buffer(buf)
        return BytesIO(data)

    def flatten_forms(self):
        return lib.folio_merge_flatten_forms()

    @property
    def page_count(self):
        return lib.folio_merge_page_count()

    @_with_error_handling(PDFMergerException)
    def remove_page(self, index: int):
        return lib.folio_merge_remove_page(self.handle, ct.c_int32(index))

    @_with_error_handling(PDFMergerException)
    def rotate_page(self, index: int, degrees: int):
        return lib.folio_merge_rotate_page(
            self.handle, ct.c_int32(index), ct.c_int32(degrees)
        )

    @_with_error_handling(PDFMergerException)
    def reorder_pages(self, order: list[int]):
        Int32Array = ct.c_int32 * len(order)
        return lib.folio_merge_reorder_pages(
            self.handle, Int32Array(order), ct.c_int32(len(order))
        )

    @_with_error_handling(PDFMergerException)
    def crop_page(self, index: float, x1: float, y1: float, x2: float, y2: float):
        return lib.folio_merge_crop_page(
            self.handle,
            ct.c_double(index),
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
        )
