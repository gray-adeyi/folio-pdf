import platform
import ctypes
from pathlib import Path

THIS_FILE_PATH = Path(__file__).parent


def _load_lib() -> ctypes.CDLL:
    operating_system = platform.system()
    architecture = platform.machine()
    if operating_system == "Windows" and architecture == "x86_64":
        return ctypes.CDLL(THIS_FILE_PATH / "libs/folio-windows-x86_64.dll")
    if operating_system == "Linux" and architecture == "x86_64":
        return ctypes.CDLL(THIS_FILE_PATH / "libs/libfolio-linux-x86_64.so")
    if operating_system == "Linux" and architecture == "aarch64":
        return ctypes.CDLL(THIS_FILE_PATH / "libs/libfolio-linux-aarch64.so")
    if operating_system == "Darwin" and architecture == "x86_64":
        return ctypes.CDLL(THIS_FILE_PATH / "libs/libfolio-macos-x86_64.dylib")
    if operating_system == "Darwin" and architecture == "aarch64":
        return ctypes.CDLL(THIS_FILE_PATH / "libs/libfolio-macos-aarch64.dylib")
    raise RuntimeError("OS or CPU architecture not supported")


lib = _load_lib()


lib.folio_buffer_data.argtypes = [ctypes.c_int64]
lib.folio_buffer_data.restype = ctypes.c_void_p

lib.folio_buffer_len.argtypes = [ctypes.c_int64]
lib.folio_buffer_len.restype = ctypes.c_int32

lib.folio_buffer_free.argtypes = [ctypes.c_int64]
lib.folio_buffer_free.restype = None
