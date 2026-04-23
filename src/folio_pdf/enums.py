from enum import IntEnum


class ErrorCodes(IntEnum):
    OK = 0
    ERR_HANDLE = -1  # invalid or expired handle
    ERR_ARG = -2  # invalid argument (NULL, out of range)
    ERR_IO = -3  # file I/O error
    ERR_PDF = -4  # PDF generation/parsing error
    ERR_TYPE = -5  # handle type mismatch
    ERR_INTERNAL = -6  # unexpected internal error
