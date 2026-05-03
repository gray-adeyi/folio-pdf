"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

from folio_pdf.exceptions import ImageException

from pathlib import Path
from enum import Enum

from folio_pdf.core import lib
from folio_pdf.object import AbstractFolioObject
import ctypes as ct


class Image(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self._image_handle = -1

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._image_handle)

    def close(self):
        lib.folio_image_free(self.handle)

    @classmethod
    def load(cls, path: str | Path):
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
    def load_jpeg(cls, path: str | Path):
        _path = path
        if isinstance(_path, Path):
            _path = _path.as_posix()
        obj = cls.__new__(cls)
        obj._image_handle = lib.folio_image_load_jpeg(ct.c_char_p(_path.encode()))
        return obj

    @classmethod
    def load_png(cls, path: str | Path):
        _path = path
        if isinstance(_path, Path):
            _path = _path.as_posix()
        obj = cls.__new__(cls)
        obj._image_handle = lib.folio_image_load_png(ct.c_char_p(_path.encode()))
        return obj

    @classmethod
    def load_tiff(cls, path: str | Path):
        _path = path
        if isinstance(_path, Path):
            _path = _path.as_posix()
        obj = cls.__new__(cls)
        obj._image_handle = lib.folio_image_load_tiff(ct.c_char_p(_path.encode()))
        return obj

    @classmethod
    def parse_jpeg(cls): ...

    @classmethod
    def parse_png(cls): ...

    @property
    def width(self):
        return lib.folio_image_width(self.handle)

    @property
    def height(self):
        return lib.folio_image_height(self.handle)
