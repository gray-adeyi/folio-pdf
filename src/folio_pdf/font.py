from pathlib import Path
from folio_pdf.core import lib
from folio_pdf.enums import StandardPDFFonts
import ctypes as ct


class Font:
    def __init__(self, font_family: StandardPDFFonts):
        self._font_ptr = lib.folio_font_standard(
            ct.c_char_p(font_family.value.encode())
        )

    def close(self):
        # TODO: Find out if standard fonts don't require to be freed and it only
        # applies to font loaded from ttf or parsed from ttf
        lib.font_free(ct.c_int64(self._font_ptr))

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()

    @classmethod
    def load_from_ttf(cls, path: Path | str):
        _path = path
        if isinstance(_path, Path):
            _path = _path.as_posix()
        obj = cls.__new__(cls)
        cls._font_ptr = lib.folio_font_load_ttf(ct.c_char_p(_path.encode()))
        return obj

    @classmethod
    def parse_from_ttf(cls, data: bytes):
        obj = cls.__new__(cls)
        cls._font_ptr = lib.folio_font_parse_ttf(ct.c_char_p(data), len(data))
        return obj
