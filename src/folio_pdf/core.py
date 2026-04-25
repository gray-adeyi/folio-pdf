from folio_pdf.enums import ErrorCodes
from typing import Callable
import platform
import ctypes as ct
from pathlib import Path

THIS_FILE_PATH = Path(__file__).parent


def _load_lib() -> ct.CDLL:
    operating_system = platform.system()
    architecture = platform.machine()
    if operating_system == "Windows" and architecture == "x86_64":
        return ct.CDLL(THIS_FILE_PATH / "libs/folio-windows-x86_64.dll")
    if operating_system == "Linux" and architecture == "x86_64":
        return ct.CDLL(THIS_FILE_PATH / "libs/libfolio-linux-x86_64.so")
    if operating_system == "Linux" and architecture == "aarch64":
        return ct.CDLL(THIS_FILE_PATH / "libs/libfolio-linux-aarch64.so")
    if operating_system == "Darwin" and architecture == "x86_64":
        return ct.CDLL(THIS_FILE_PATH / "libs/libfolio-macos-x86_64.dylib")
    if operating_system == "Darwin" and architecture == "aarch64":
        return ct.CDLL(THIS_FILE_PATH / "libs/libfolio-macos-aarch64.dylib")
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

        return wrapper

    return decorator
