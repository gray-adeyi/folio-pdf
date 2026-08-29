"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct
from pathlib import Path

from folio_pdf.core import AbstractFolioObject, lib

lib.folio_reader_open.argtypes = [ct.c_char_p]
lib.folio_reader_open.restype = ct.c_uint64

lib.folio_reader_parse.argtypes = [ct.c_void_p, ct.c_int32]
lib.folio_reader_parse.restype = ct.c_uint64

lib.folio_reader_free.argtypes = [ct.c_uint64]
lib.folio_reader_free.restype = None

lib.folio_reader_page_count.argtypes = [ct.c_uint64]
lib.folio_reader_page_count.restype = ct.c_int32

lib.folio_reader_version.argtypes = [ct.c_uint64]
lib.folio_reader_version.restype = ct.c_uint64

lib.folio_reader_info_title.argtypes = [ct.c_uint64]
lib.folio_reader_info_title.restype = ct.c_uint64

lib.folio_reader_info_author.argtypes = [ct.c_uint64]
lib.folio_reader_info_author.restype = ct.c_uint64

lib.folio_reader_extract_text.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_reader_extract_text.restype = ct.c_uint64

lib.folio_reader_page_width.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_reader_page_width.restype = ct.c_double

lib.folio_reader_page_height.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_reader_page_height.restype = ct.c_double

lib.folio_reader_structure_tree.argtypes = [ct.c_uint64]
lib.folio_reader_structure_tree.restype = ct.c_uint64

lib.folio_reader_text_spans.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_reader_text_spans.restype = ct.c_uint64

lib.folio_reader_images.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_reader_images.restype = ct.c_uint64

lib.folio_reader_paths.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_reader_paths.restype = ct.c_uint64


class PDFReader(AbstractFolioObject):
    """
    Opens an existing PDF for inspection — reading metadata, page dimensions, and
    extracting text.
    """

    _requires_close = True

    def __init__(self, path: str | Path):
        """
        Opens a PDF file from disk.

        Args:
            path: absolute path to the PDF file

        Returns:
            a new `PDFReader` for the file
        """
        _path = path
        if isinstance(_path, Path):
            _path = _path.as_posix()
        self.__handle = lib.folio_reader_open(ct.c_char_p(_path.encode()))

    @classmethod
    def parse(cls, data: bytes) -> "PDFReader":
        """
        Parses a PDF from raw bytes.

        Args:
            data: the raw PDF bytes

        Returns:
            a new `PDFReader` for the in-memory PDF
        """
        obj = cls.__new__(cls)
        obj._reader_handle = lib.folio_reader_parse(
            ct.c_char_p(data), ct.c_int32(len(data))
        )
        return obj

    @property
    def page_count(self) -> int:
        """
        Returns the total number of pages in the PDF.
        """
        return lib.folio_reader_page_count(self._handle)

    @property
    def version(self) -> str:
        """
        Returns the PDF version string (e.g., `"1.7"`).
        """
        buf = lib.folio_reader_version(self._handle)
        return str(self._read_from_obj_buffer(buf))

    @property
    def info_title(self) -> str:
        """
        Returns the document title from PDF metadata, or an empty string if not set.
        """
        buf = lib.folio_reader_info_title(self._handle)
        return str(self._read_from_obj_buffer(buf))

    @property
    def info_author(self) -> str:
        """
        Returns the document author from PDF metadata, or an empty string if not set.
        """
        buf = lib.folio_reader_info_author(self._handle)
        return str(self._read_from_obj_buffer(buf))

    def extract_text(self, page_index: int) -> str:
        """
        Extracts the plain text content from the specified page.

        Args:
            page_index: zero-based page index

        Returns:
            the extracted text, or an empty string if the page has no text
        """
        buf = lib.folio_reader_extract_text(self._handle, ct.c_int32(page_index))
        return str(self._read_from_obj_buffer(buf))

    def page_width(self, page_index: int) -> float:
        """
        Returns the width of the specified page in points.

        Args:
            page_index: zero-based page index

        Returns:
            page width in points
        """
        return lib.folio_reader_page_width(self._handle, ct.c_int32(page_index))

    def page_height(self, page_index: int) -> float:
        """
        Returns the height of the specified page in points.

        Args:
            page_index: zero-based page index

        Returns:
            page height in points
        """
        return lib.folio_reader_page_height(self._handle, ct.c_int32(page_index))

    def structure_tree(self) -> bytes:
        """
        Returns the PDF/UA structure tree as JSON. Returns null if the
        document is not tagged.

        Returns:
            JSON string of the tag structure tree, or null
        """
        buf = lib.folio_reader_structure_tree(self._handle)
        return self._read_from_obj_buffer(buf)

    def text_spans(self, page_index: int) -> bytes:
        """
        Returns structured text spans (with positions and fonts) from a page.

        The result is a JSON string describing each span.

        Args:
            page_index: zero-based page index

        Returns:
            JSON string of text spans, or null
        """
        buf = lib.folio_reader_text_spans(self._handle, ct.c_int32(page_index))
        return self._read_from_obj_buffer(buf)

    def images(self, page_index: int) -> bytes:
        """
        Returns image metadata from a page.

        The result is a JSON string describing each embedded image.

        Args:
            page_index: zero-based page index

        Returns:
            JSON string of image data, or null
        """
        buf = lib.folio_reader_images(self._handle, ct.c_int32(page_index))
        return self._read_from_obj_buffer(buf)

    def paths(self, page_index: int) -> bytes:
        """
        Returns vector path data from a page.

        The result is a JSON string describing each drawing path.

        Args:
            page_index: zero-based page index

        Returns:
            JSON string of path data, or null
        """
        buf = lib.folio_reader_paths(self._handle, ct.c_int32(page_index))
        return self._read_from_obj_buffer(buf)

    def close(self):
        lib.folio_reader_free(self._handle)

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)
