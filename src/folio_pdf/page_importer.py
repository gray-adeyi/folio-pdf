"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf import PDFReader
from folio_pdf.core import AbstractFolioObject, lib

lib.folio_extract_page_import.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_extract_page_import.restype = ct.c_uint64

lib.folio_page_import_free.argtypes = [ct.c_uint64]
lib.folio_page_import_free.restype = None

lib.folio_page_import_width.argtypes = [ct.c_uint64]
lib.folio_page_import_width.restype = ct.c_double

lib.folio_page_import_height.argtypes = [ct.c_uint64]
lib.folio_page_import_height.restype = ct.c_double


class PageImporter(AbstractFolioObject):
    """
    A handle to a page extracted from an existing PDF that can be stamped onto
    a new `Page` as a template or background.
    """

    _requires_close = True

    def __init__(self, reader: PDFReader, page_index: int):
        """
        Extracts the given page from an open `PDFReader`.

        Args:
            reader: source PDF reader
            page_index: zero-based page index

        Returns:
            a new `PageImporter` handle
        """
        self.__handle = lib.folio_extract_page_import(
            reader._handle, ct.c_int32(page_index)
        )

    @property
    def width(self) -> float:
        """
        Returns the source page width in points.
        """
        return lib.folio_page_import_width(self._handle)

    @property
    def height(self) -> float:
        """
        Returns the source page height in points.
        """
        return lib.folio_page_import_height(self._handle)

    def close(self):
        lib.folio_page_import_free(self._handle)

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)
