"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct
import sys
from pathlib import Path

from folio_pdf.core import AbstractFolioObject, lib
from folio_pdf.exceptions import ImageException

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


lib.folio_image_load_jpeg.argtypes = [ct.c_char_p]
lib.folio_image_load_jpeg.restype = ct.c_uint64

lib.folio_image_load_png.argtypes = [ct.c_char_p]
lib.folio_image_load_png.restype = ct.c_uint64

lib.folio_image_load_tiff.argtypes = [ct.c_char_p]
lib.folio_image_load_tiff.restype = ct.c_uint64

lib.folio_image_parse_jpeg.argtypes = [ct.c_void_p, ct.c_int32]
lib.folio_image_parse_jpeg.restype = ct.c_uint64

lib.folio_image_parse_png.argtypes = [ct.c_void_p, ct.c_int32]
lib.folio_image_parse_png.restype = ct.c_uint64

lib.folio_image_width.argtypes = [ct.c_uint64]
lib.folio_image_width.restype = ct.c_int32

lib.folio_image_height.argtypes = [ct.c_uint64]
lib.folio_image_height.restype = ct.c_int32

lib.folio_image_free.argtypes = [ct.c_uint64]
lib.folio_image_free.restype = None


class Image(AbstractFolioObject):
    """
    Represents an image that can be added to a `ImageElement`.
    """

    _requires_close = True
    _binding_resource_free_fn = lib.folio_flex_item_free

    def __init__(self):
        self._is_closed = False
        self.__handle = 0

    @classmethod
    def load(cls, path: str | Path) -> Self:
        """
        Loads an image from the given file path.

        This uses the extension in the path to determin how to load
        the iamge and only currently supports, jpeg, png and tiff.

        Args:
            path: absolute path to the image file

        Returns:
            a new `Image` which can then be used to create and `ImageElement`,
            which can then be added to a document or div
        """
        _path = path
        if isinstance(_path, str):
            _path = Path(_path)
        ext = _path.suffix
        if ext == ".jpg" or ext == ".jpeg":
            return cls.load_jpeg(_path)
        if ext == ".png":
            return cls.load_jpeg(_path)
        if ext == ".tiff":
            return cls.load_tiff(_path)
        raise ImageException(f"loading image with the extension {ext} is not supported")

    @classmethod
    def load_jpeg(cls, path: str | Path) -> Self:
        """
        Loads a JPEG image from the given file path.

        Args:
            path: absolute path to the `.jpg` / `.jpeg` file

        Returns:
            a new `Image` which can then be used to create and `ImageElement`,
            which can then be added to a document or div
        """
        _path = path
        if isinstance(_path, Path):
            _path = _path.as_posix()
        obj = cls.__new__(cls)
        obj._is_closed = False
        obj.__handle = lib.folio_image_load_jpeg(ct.c_char_p(_path.encode()))
        return obj

    @classmethod
    def load_png(cls, path: str | Path) -> Self:
        """
        Loads a PNG image from the given file path.

        Args:
            path: absolute path to the `.png` file

        Returns:
            a new `Image` which can then be used to create and `ImageElement`,
            which can then be added to a document or div
        """
        _path = path
        if isinstance(_path, Path):
            _path = _path.as_posix()
        obj = cls.__new__(cls)
        obj._is_closed = False
        obj.__handle = lib.folio_image_load_png(ct.c_char_p(_path.encode()))
        return obj

    @classmethod
    def load_tiff(cls, path: str | Path) -> Self:
        """
        Loads a TIFF image from the given file path.

        Args:
            path: absolute path to the `.tif` / `.tiff` file

        Returns:
            a new `Image` which can then be used to create and `ImageElement`,
            which can then be added to a document or div
        """
        _path = path
        if isinstance(_path, Path):
            _path = _path.as_posix()
        obj = cls.__new__(cls)
        obj._is_closed = False
        obj.__handle = lib.folio_image_load_tiff(ct.c_char_p(_path.encode()))
        return obj

    @classmethod
    def parse_jpeg(cls, data: bytes) -> Self:
        """
        Parses a JPEG image from raw bytes.

        Args:
            data: the raw JPEG bytes

        Returns:
            a new `Image` which can then be used to create and `ImageElement`,
            which can then be added to a document or div
        """
        obj = cls.__new__(cls)
        obj._is_closed = False
        obj.__handle = lib.folio_image_parse_jpeg(
            ct.c_char_p(data), ct.c_int32(len(data))
        )
        return obj

    @classmethod
    def parse_png(cls, data: bytes) -> Self:
        """
        Parses a PNG image from raw bytes.

        Args:
            data: the raw PNG bytes

        Returns:
            a new `Image` which can then be used to create and `ImageElement`,
            which can then be added to a document or div
        """
        obj = cls.__new__(cls)
        obj._is_closed = False
        obj.__handle = lib.folio_image_parse_jpeg(
            ct.c_char_p(data), ct.c_int32(len(data))
        )
        return obj

    @property
    def width(self) -> int:
        """
        Returns the natural pixel width of the source image.
        """
        return lib.folio_image_width(self._handle)

    @property
    def height(self) -> int:
        """
        Returns the natural pixel height of the source image.
        """
        return lib.folio_image_height(self._handle)

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)
