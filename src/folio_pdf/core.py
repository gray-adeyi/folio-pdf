"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct
import platform
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable, Concatenate, ParamSpec, TypeVar

from folio_pdf.enums import ErrorCode

THIS_FILE_PATH = Path(__file__).parent
_FuncParams = ParamSpec("_FuncParams")
_ReturnType = TypeVar("_ReturnType")
_Self = TypeVar("_Self")


def _load_lib() -> ct.CDLL:
    os_name = platform.system()
    arch = platform.machine().lower()

    arch_aliases = {
        "amd64": "x86_64",
        "x86_64": "x86_64",
        "arm64": "aarch64",
        "aarch64": "aarch64",
    }

    arch = arch_aliases.get(arch, arch)

    extensions = {
        "Windows": "dll",
        "Linux": "so",
        "Darwin": "dylib",
    }

    prefixes = {
        "Windows": "",
        "Linux": "lib",
        "Darwin": "lib",
    }

    if os_name not in extensions:
        raise RuntimeError(f"Unsupported OS: {os_name} Arch: {arch}")

    filename = (
        f"{prefixes[os_name]}folio-{os_name.lower()}-{arch}.{extensions[os_name]}"
    )

    lib_path = THIS_FILE_PATH / "libs" / filename

    if not lib_path.exists():
        raise RuntimeError(f"folio shared library not found at: {lib_path}")

    return ct.CDLL(str(lib_path))


lib = _load_lib()

# Core
lib.folio_version.argtypes = []
lib.folio_version.restype = ct.c_char_p

lib.folio_last_error.argtypes = []
lib.folio_last_error.restype = ct.c_char_p

lib.folio_string_free.argtypes = [ct.c_char_p]
lib.folio_string_free.restype = None

# Buffer
lib.folio_buffer_data.argtypes = [ct.c_int64]
lib.folio_buffer_data.restype = ct.c_void_p

lib.folio_buffer_len.argtypes = [ct.c_int64]
lib.folio_buffer_len.restype = ct.c_int32

lib.folio_buffer_len64.argtypes = [ct.c_int64]
lib.folio_buffer_len64.restype = ct.c_int64

lib.folio_buffer_free.argtypes = [ct.c_int64]
lib.folio_buffer_free.restype = None


def get_folio_version() -> str:
    """Get the version of the underlying folio shared lib

    Note: Not to be confused with folio-pdf (the package) version.
    This version number is the version number of the shared library
    `folio` that this package depends on.
    """
    return str(lib.folio_version())


def _with_error_handling(
    exception: type[Exception],
):
    def decorator(
        func: Callable[Concatenate[_Self, _FuncParams], int],
    ) -> Callable[Concatenate[_Self, _FuncParams], _Self]:

        def wrapper(
            self: _Self,
            *args: _FuncParams.args,
            **kwargs: _FuncParams.kwargs,
        ) -> _Self:
            res_code = func(self, *args, **kwargs)

            err_code = ErrorCode(res_code)
            if err_code != ErrorCode.OK:
                msg_bytes = lib.folio_last_error()
                lib.folio_string_free(ct.c_char_p(msg_bytes))
                raise exception(str(msg_bytes))

            return self

        return wrapper

    return decorator


def _read_from_obj_buffer(buf: int):
    size = lib.folio_buffer_len64(buf)
    ptr = lib.folio_buffer_data(buf)
    data = ct.string_at(ptr, size)
    lib.folio_buffer_free(buf)
    return data


class AbstractFolioObject(ABC):
    # Flag to determine if the obj needs to call `close` to free memory
    _requires_close: bool
    # Flag to determine if `close` has been called i.e. memory is already freed
    _is_closed: bool
    _binding_resource_free_fn: Callable[[ct.c_uint64], None]

    @property
    @abstractmethod
    def _handle(self) -> ct.c_uint64:
        """Returns the native object handle"""
        ...

    def close(self):
        if self._requires_close and not self._is_closed:
            self._binding_resource_free_fn(self._handle)
            self._is_closed = True

    @staticmethod
    def _read_from_obj_buffer(buf: int):
        return _read_from_obj_buffer(buf)

    def __enter__(self):
        return self

    def __exit__(self, *_args, **_kwargs):
        if self._requires_close:
            self.close()

    def __del__(self):
        # A non-deterministice approach to freeing memory handled by the GC
        # From what i've read, __del__ is called when the reference count to
        # an object becomes zero, but it's not called immediately, it is called
        # when the GC wants to free memory, this will serve as a backup strategy
        # to freeing memory when the package consumer forgets to call `close`
        # explicitly or as a context manager
        self.close()
