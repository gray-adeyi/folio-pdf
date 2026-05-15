"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct
import platform
from abc import abstractmethod
from pathlib import Path
from typing import Callable

from folio_pdf.enums import ErrorCodes

THIS_FILE_PATH = Path(__file__).parent


def _load_lib() -> ct.CDLL:
    operating_system = platform.system()
    architecture = platform.machine()
    if operating_system == "Windows" and architecture == "x86_64":
        return ct.CDLL((THIS_FILE_PATH / "libs/folio-windows-x86_64.dll").as_posix())
    if operating_system == "Linux" and architecture == "x86_64":
        return ct.CDLL((THIS_FILE_PATH / "libs/libfolio-linux-x86_64.so").as_posix())
    if operating_system == "Linux" and architecture == "aarch64":
        return ct.CDLL((THIS_FILE_PATH / "libs/libfolio-linux-aarch64.so").as_posix())
    if operating_system == "Darwin" and architecture == "x86_64":
        return ct.CDLL((THIS_FILE_PATH / "libs/libfolio-macos-x86_64.dylib").as_posix())
    if operating_system == "Darwin" and architecture == "aarch64":
        return ct.CDLL(
            (THIS_FILE_PATH / "libs/libfolio-macos-aarch64.dylib").as_posix()
        )
    raise RuntimeError("OS or CPU architecture not supported")


lib = _load_lib()

# Core
lib.folio_version.argtypes = []
lib.folio_version.restype = ct.c_char_p

lib.folio_last_error.argtypes = []
lib.folio_last_error.restype = ct.c_char_p

# Buffer
lib.folio_buffer_data.argtypes = [ct.c_int64]
lib.folio_buffer_data.restype = ct.c_void_p

lib.folio_buffer_len.argtypes = [ct.c_int64]
lib.folio_buffer_len.restype = ct.c_int32

lib.folio_buffer_free.argtypes = [ct.c_int64]
lib.folio_buffer_free.restype = None


def _with_error_handling(exception: type[Exception]):
    def decorator(func: Callable):
        def wrapper(self, *args, **kwargs):
            res_code = func(self, *args, **kwargs)
            err = ErrorCodes(res_code)
            if err != ErrorCodes.OK:
                msg_bytes = lib.folio_last_error()
                raise exception(str(msg_bytes))
            return self

        return wrapper

    return decorator


def _read_from_obj_buffer(buf: int):
    size = lib.folio_buffer_len(buf)
    ptr = lib.folio_buffer_data(buf)
    data = ct.string_at(ptr, size)
    lib.folio_buffer_free(buf)
    return data


class AbstractFolioObject:
    _requires_close: bool

    @property
    @abstractmethod
    def handle(self) -> ct.c_uint64:
        """Returns the object handle"""
        ...

    def close(self):
        err_msg = (
            "close method has not been implemented for folio object"
            if self._requires_close
            else "folio object does not require close"
        )
        raise NotImplementedError(err_msg)

    def _read_from_obj_buffer(self, buf: int):
        return _read_from_obj_buffer(buf)

    def __enter__(self):
        return self

    def __exit__(self, *_args, **_kwargs):
        if self._requires_close:
            self.close()
