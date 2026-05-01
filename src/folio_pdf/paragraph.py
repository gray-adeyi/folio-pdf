from folio_pdf.enums import Alignments
from folio_pdf.exceptions import ParagraphException
from folio_pdf.core import lib, _with_error_handling
from folio_pdf.object import AbstractFolioObject
from folio_pdf.font import Font
import ctypes as ct


class Paragraph(AbstractFolioObject):
    def __init__(self, text: str, font: Font, font_size: float):
        self._paragraph_handle = lib.folio_paragraph_new(
            ct.c_char_p(text.encode()), font.handle, ct.c_double(font_size)
        )

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._paragraph_handle)

    @classmethod
    def new_embedded(cls, text: str, font: Font, font_size: float):
        obj = cls.__new__(cls)
        obj._paragraph_handle = lib.folio_paragraph_new_embedded(
            ct.c_char_p(text.encode()), font.handle, ct.c_double(font_size)
        )
        return obj

    def close(self):
        lib.folio_paragraph_free(self.handle)

    @_with_error_handling(ParagraphException)
    def set_align(self, align: Alignments):
        return lib.folio_paragraph_set_align(self.handle, ct.c_int32(align.value))

    @_with_error_handling(ParagraphException)
    def set_leading(self, leading: float):
        return lib.folio_paragraph_set_leading(self.handle, ct.c_double(leading))

    @_with_error_handling(ParagraphException)
    def set_space_before(self, pts: float):
        return lib.folio_paragraph_set_space_before(self.handle, ct.c_double(pts))

    @_with_error_handling(ParagraphException)
    def set_space_after(self, pts: float):
        return lib.folio_paragraph_set_space_after(self.handle, ct.c_double(pts))

    @_with_error_handling(ParagraphException)
    def set_background(self, r: float, g: float, b: float):
        return lib.folio_paragraph_set_background(
            self.handle, ct.c_double(r), ct.c_double(g), ct.c_double(b)
        )

    @_with_error_handling(ParagraphException)
    def set_first_indent(self, pts: float):
        return lib.folio_paragraph_set_first_indent(self.handle, ct.c_double(pts))

    @_with_error_handling(ParagraphException)
    def set_orphans(self, n: int):
        return lib.folio_paragraph_set_orphans(self.handle, ct.c_int32(n))

    @_with_error_handling(ParagraphException)
    def set_widows(self, n: int):
        return lib.folio_paragraph_set_widows(self.handle, ct.c_int32(n))

    @_with_error_handling(ParagraphException)
    def set_ellipsis(self, enabled: bool):
        return lib.folio_paragraph_set_ellipsis(self.handle, ct.c_int32(enabled))

    @_with_error_handling(ParagraphException)
    def set_word_break(self, mode: str):
        return lib.folio_paragraph_set_word_break(
            self.handle,
            ct.c_char_p(mode.encode()),
        )

    @_with_error_handling(ParagraphException)
    def set_hyphens(self, mode: str):
        return lib.folio_paragraph_set_hyphens(self.handle, ct.c_char_p(mode.encode()))

    @_with_error_handling(ParagraphException)
    def set_text_align_last(self, align: Alignments):
        return lib.folio_paragraph_set_text_align_last(
            self.handle, ct.c_int32(align.value)
        )

    @_with_error_handling(ParagraphException)
    def add_run(
        self,
        text: str,
        font: Font,
        font_size: float,
        r: float,
        g: float,
        b: float,
    ):
        return lib.folio_paragraph_add_run(
            self.handle,
            ct.c_char_p(text.encode()),
            font.handle,
            ct.c_double(font_size),
            ct.c_double(r),
            ct.c_double(g),
            ct.c_double(b),
        )

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()
