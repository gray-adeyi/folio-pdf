"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct
from io import BytesIO
from pathlib import Path

from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.exceptions import PDFMergerException
from folio_pdf.font import Font
from folio_pdf.reader import PDFReader

lib.folio_merge_set_info.argtypes = [ct.c_uint64, ct.c_char_p, ct.c_char_p]
lib.folio_merge_set_info.restype = ct.c_int32

lib.folio_merge_add_blank_page.argtypes = [ct.c_uint64, ct.c_double, ct.c_double]
lib.folio_merge_add_blank_page.restype = ct.c_int32

lib.folio_merge_add_page_with_text.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_char_p,
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_merge_add_page_with_text.restype = ct.c_int32

lib.folio_merge_save.argtypes = [ct.c_uint64, ct.c_char_p]
lib.folio_merge_save.restype = ct.c_int32

lib.folio_merge_write_to_buffer.argtypes = [ct.c_uint64]
lib.folio_merge_write_to_buffer.restype = ct.c_uint64

lib.folio_merge_flatten_forms.argtypes = [ct.c_uint64]
lib.folio_merge_flatten_forms.restype = ct.c_int32

lib.folio_merge_page_count.argtypes = [ct.c_uint64]
lib.folio_merge_page_count.restype = ct.c_int32

lib.folio_merge_remove_page.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_merge_remove_page.restype = ct.c_int32

lib.folio_merge_rotate_page.argtypes = [ct.c_uint64, ct.c_int32, ct.c_int32]
lib.folio_merge_rotate_page.restype = ct.c_int32

lib.folio_merge_crop_page.argtypes = [
    ct.c_uint64,
    ct.c_int32,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_merge_crop_page.restype = ct.c_int32

lib.folio_merge_free.argtypes = [ct.c_uint64]
lib.folio_merge_free.restype = None


class PDFMerger(AbstractFolioObject):
    """
    Merges multiple PDF documents into a single output.
    """

    _requires_close = True

    def __init__(self, readers: list[PDFReader]):
        """
        Merges multiple `PDFReader` instances into a single document.

        Args:
            readers: the PDF readers to merge (in order)

        Returns:
            a new `PDFMerger` with the combined pages
        """
        readers_handles = [reader._handle for reader in readers]
        UInt64Array = ct.c_uint64 * len(readers_handles)
        lib.folio_reader_merge.argtypes = [
            UInt64Array,
            ct.c_int32,
        ]
        lib.folio_reader_merge.restype = ct.c_uint64
        self.__handle = lib.folio_reader_merge(
            UInt64Array(readers_handles), ct.c_int32(len(readers_handles))
        )

    @classmethod
    def merge_files(cls, paths: list[str | Path]) -> "PDFMerger":
        """
        Merges PDF files by path.

        Call `save` on the returned `PDFMerger` to save the merged pdf to file.

        Args:
            paths: the file paths of the PDFs to merge (in order)

        Returns:
            a `PDFMerger` with all the merged PDFs
        """
        obj = cls.__new__(cls)
        _paths = [path.as_posix() if isinstance(path, Path) else path for path in paths]
        CharPArray = ct.c_char_p * len(_paths)
        lib.folio_merge_files.argtypes = [CharPArray, ct.c_int32]
        lib.folio_merge_files.restype = ct.c_uint64
        obj._merger_handle = lib.folio_merge_files(
            CharPArray(_paths), ct.c_int32(len(_paths))
        )
        return obj

    @_with_error_handling(PDFMergerException)
    def info(self, title: str, author: str) -> "PDFMerger":
        """
        Sets the title and author metadata on the merged document.

        Args:
            title: the document title
            author: the document author

        Returns:
            this merger, for chaining
        """
        return lib.folio_merge_set_info(
            ct.c_char_p(title.encode()),
            ct.c_char_p(author.encode()),
        )

    @_with_error_handling(PDFMergerException)
    def add_blank_page(self, width: float, height: float) -> "PDFMerger":
        """
        Appends a blank page with the given dimensions.

        Args:
            width: page width in points
            height: page height in points

        Returns:
            this merger, for chaining
        """
        return lib.folio_merge_add_blank_page(ct.c_double(width), ct.c_double(height))

    @_with_error_handling(PDFMergerException)
    def add_page_with_text(
        self,
        width: float,
        height: float,
        text: str,
        font: Font,
        font_size: float,
        x: float,
        y: float,
    ) -> "PDFMerger":
        """
        Appends a page with text at a specific position.

        Args:
            width: page width in points
            height: page height in points
            text: text to place on the page
            font: the font to use
            font_size: font size in points
            x: x coordinate
            y: y coordinate

        Returns:
            this merger, for chaining
        """
        return lib.folio_merge_add_page_with_text(
            ct.c_double(width),
            ct.c_double(height),
            ct.c_char_p(text.encode()),
            font._handle,
            ct.c_double(font_size),
            ct.c_double(x),
            ct.c_double(y),
        )

    @_with_error_handling(PDFMergerException)
    def save(self, path: str | Path) -> "PDFMerger":
        """
        Saves the merged document to a file.

        Args:
            path: the output file path
        """
        _path = path
        if isinstance(_path, Path):
            _path = _path.as_posix()
        return lib.folio_merge_save(self._handle, ct.c_char_p(_path.encode()))

    def write_to_buffer(self) -> BytesIO:
        """
        Renders the merged document to an in-memory buffer.

        Returns:
            the PDF in an in-memory buffer
        """
        buf = lib.folio_merge_write_to_buffer(self._handle)
        data = self._read_from_obj_buffer(buf)
        return BytesIO(data)

    @_with_error_handling(PDFMergerException)
    def flatten_forms(self) -> "PDFMerger":
        """
        Flattens all interactive form fields into static content.

        After flattening, fields are no longer editable.

        Returns:
            this merger, for chaining
        """
        return lib.folio_merge_flatten_forms()

    @property
    def page_count(self) -> int:
        """
        Returns the number of pages in the merged document.
        """
        return lib.folio_merge_page_count()

    @_with_error_handling(PDFMergerException)
    def remove_page(self, index: int) -> "PDFMerger":
        """
        Removes the page at the given zero-based index.

        Args:
            index: The zero-based index of the page to remove

        Returns:
            this merger, for chaining
        """
        return lib.folio_merge_remove_page(self._handle, ct.c_int32(index))

    @_with_error_handling(PDFMergerException)
    def rotate_page(self, index: int, degrees: int) -> "PDFMerger":
        """
        Rotates the page at the given index by the specified degrees (90, 180, 270).

        Args:
            index: The zero-based index of the page to rotate
            degrees: The angle to rotate the page in degrees

        Returns:
            this merger, for chaining
        """
        return lib.folio_merge_rotate_page(
            self._handle, ct.c_int32(index), ct.c_int32(degrees)
        )

    @_with_error_handling(PDFMergerException)
    def reorder_pages(self, order: list[int]) -> "PDFMerger":
        """
        Reorders pages.

        The array specifies the new order by old page indices.
        For example, `[2, 0, 1]` moves page 2 to first position.

        Args:
            order: the new order of the pages based on the zero-based indexes of the
            old order.

        Returns:
            this merger, for chaining
        """
        Int32Array = ct.c_int32 * len(order)
        lib.folio_merge_reorder_pages.argtypes = [ct.c_uint64, Int32Array, ct.c_int32]
        lib.folio_merge_reorder_pages.restype = ct.c_int32
        return lib.folio_merge_reorder_pages(
            self._handle, Int32Array(order), ct.c_int32(len(order))
        )

    @_with_error_handling(PDFMergerException)
    def crop_page(
        self, index: float, x1: float, y1: float, x2: float, y2: float
    ) -> "PDFMerger":
        """
        Crops the page at the given index to the specified rectangle.

        Args:
            index: the zero-based index of the page to crop
            x1: left coordinate in points
            y1: bottom coordinate in points
            x2: right coordinate in points
            y2: top coordinate in points

        Returns:
            this merger, for chaining
        """
        return lib.folio_merge_crop_page(
            self._handle,
            ct.c_double(index),
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
        )

    def close(self):
        lib.folio_merge_free(self._handle)

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)
