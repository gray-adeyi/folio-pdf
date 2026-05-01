from folio_pdf.image import Image
from folio_pdf.exceptions import PageException
from folio_pdf.object import AbstractFolioObject
from folio_pdf.font import Font
from folio_pdf.core import lib, _with_error_handling
import ctypes as ct

lib.folio_page_add_text.argtypes = [
    ct.c_uint64,
    ct.c_char_p,
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_page_add_text.restype = ct.c_int32

lib.folio_page_add_text_embedded.argtypes = [
    ct.c_uint64,
    ct.c_char_p,
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_page_add_text_embedded.restype = ct.c_int32

lib.folio_page_add_image.argtypes = [
    ct.c_uint64,
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_page_add_image.restype = ct.c_int32

lib.folio_page_add_link.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_char_p,
]
lib.folio_page_add_link.restype = ct.c_int32

lib.folio_page_add_internal_link.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_char_p,
]
lib.folio_page_add_internal_link.restype = ct.c_int32

lib.folio_page_add_text_annotation.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_char_p,
    ct.c_char_p,
]
lib.folio_page_add_text_annotation.restype = ct.c_int32

lib.folio_page_set_opacity.argtypes = [ct.c_uint64, ct.c_double]
lib.folio_page_set_opacity.restype = ct.c_int32

lib.folio_page_set_rotate.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_page_set_rotate.restype = ct.c_int32

lib.folio_page_set_crop_box.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_page_set_crop_box.restype = ct.c_int32

lib.folio_page_set_trim_box.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_page_set_trim_box.restype = ct.c_int32

lib.folio_page_set_trim_box.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_page_set_trim_box.restype = ct.c_int32

lib.folio_page_set_size.argtypes = [ct.c_uint64, ct.c_double, ct.c_double]
lib.folio_page_set_size.restype = ct.c_int32

lib.folio_page_add_page_link.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_int32,
]
lib.folio_page_add_page_link.restype = ct.c_int32

lib.folio_page_set_opacity_fill_stroke.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
]
lib.folio_page_set_opacity_fill_stroke.restype = ct.c_int32

lib.folio_page_add_highlight.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_int32,
]
lib.folio_page_add_highlight.restype = ct.c_int32

lib.folio_page_add_underline_annotation.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_int32,
]
lib.folio_page_add_underline_annotation.restype = ct.c_int32

lib.folio_page_add_squiggly.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_int32,
]
lib.folio_page_add_squiggly.restype = ct.c_int32

lib.folio_page_add_strikeout.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_int32,
]
lib.folio_page_add_strikeout.restype = ct.c_int32


class Page(AbstractFolioObject):
    def __init__(self):
        self._page_handle = -1

    @property
    def handle(self) -> int:
        return self._page_handle

    @classmethod
    def _new_from_handle(cls, page_handle: int):
        obj = cls.__new__(cls)
        cls._page_handle = page_handle
        return obj

    @_with_error_handling(PageException)
    def add_text(self, text: str, font: Font, size: float, x: float, y: float):
        return lib.folio_page_add_text(
            ct.c_char_p(text.encode()),
            ct.c_uint64(font.handle),
            ct.c_double(size),
            ct.c_double(x),
            ct.c_double(y),
        )

    @_with_error_handling(PageException)
    def add_text_embedded(self, text: str, font: Font, size: float, x: float, y: float):
        return lib.folio_page_add_text_embedded(
            ct.c_uint64(self.handle),
            ct.c_char_p(text.encode()),
            ct.c_uint64(font.handle),
            ct.c_double(size),
            ct.c_double(x),
            ct.c_double(y),
        )

    @_with_error_handling(PageException)
    def add_image(self, img: Image, x: float, y: float, w: float, h: float):
        return lib.folio_page_add_image(
            ct.c_uint64(self.handle),
            ct.c_uint64(img.handle),
            ct.c_double(x),
            ct.c_double(y),
            ct.c_double(w),
            ct.c_double(h),
        )

    @_with_error_handling(PageException)
    def add_link(self, x1: float, y1: float, x2: float, y2: float, uri: str):
        return lib.folio_page_add_link(
            ct.c_uint64(self.handle),
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_char_p(uri.encode()),
        )

    @_with_error_handling(PageException)
    def add_internal_link(
        self, x1: float, y1: float, x2: float, y2: float, dest_name: str
    ):
        return lib.folio_page_add_internal_link(
            ct.c_uint64(self.handle),
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_char_p(dest_name.encode()),
        )

    @_with_error_handling(PageException)
    def add_text_annotation(
        self, x1: float, y1: float, x2: float, y2: float, text: str, icon: str
    ):
        return lib.folio_page_add_text_annotation(
            ct.c_uint64(self.handle),
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_char_p(text.encode()),
            ct.c_char_p(icon.encode()),
        )

    @_with_error_handling(PageException)
    def set_opacity(self, alpha: float):
        return lib.folio_page_set_opacity(ct.c_uint64(self.handle), ct.c_double(alpha))

    @_with_error_handling(PageException)
    def set_rotate(self, degress: int):
        return lib.folio_page_set_rotate(ct.c_uint64(self.handle), ct.c_int32(degress))

    @_with_error_handling(PageException)
    def set_crop_box(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
    ):
        return lib.folio_page_set_crop_box(
            ct.c_uint64(self.handle),
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
        )

    @_with_error_handling(PageException)
    def set_trim_box(self, x1: float, y1: float, x2: float, y2: float):
        return lib.folio_page_set_trim_box(
            ct.c_uint64(self.handle),
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
        )

    @_with_error_handling(PageException)
    def set_bleed_box(self, x1: float, y1: float, x2: float, y2: float):
        return lib.folio_page_set_bleed_box(
            ct.c_uint64(self.handle),
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
        )

    @_with_error_handling(PageException)
    def set_art_box(self, x1: float, y1: float, x2: float, y2: float):
        return lib.folio_page_set_art_box(
            ct.c_uint64(self.handle),
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
        )

    @_with_error_handling(PageException)
    def set_size(self, width: float, height: float):
        return lib.folio_page_set_size(
            ct.c_uint64(self.handle), ct.c_double(width), ct.c_double(height)
        )

    @_with_error_handling(PageException)
    def add_page_link(
        self, x1: float, y1: float, x2: float, y2: float, target_page: int
    ):
        return lib.folio_page_add_page_link(
            ct.c_uint64(self.handle),
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_int32(target_page),
        )

    @_with_error_handling(PageException)
    def set_opacity_fill_stroke(self, fill_alpha: float, stroke_alpha: float):
        return lib.folio_page_set_opacity(
            ct.c_uint64(self.handle), ct.c_double(fill_alpha), ct.c_double(stroke_alpha)
        )

    @_with_error_handling(PageException)
    def add_highlight(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        r: float,
        g: float,
        b: float,
        quad_points: float,
        quad_count: int,
    ):  # TODO: quad_points might be an array
        return lib.folio_page_add_highlight(
            ct.c_uint64(self.handle),
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_double(r),
            ct.c_double(g),
            ct.c_double(b),
            ct.c_double(quad_points),
            ct.c_double(quad_count),
        )

    @_with_error_handling(PageException)
    def add_underline_annotation(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        r: float,
        g: float,
        b: float,
        quad_points: float,
        quad_count: int,
    ):  # TODO: quad_points might be an array
        return lib.folio_page_add_underline_annotation(
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_double(r),
            ct.c_double(g),
            ct.c_double(b),
            ct.c_double(quad_points),
            ct.c_double(quad_count),
        )

    @_with_error_handling(PageException)
    def add_squiggly(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        r: float,
        g: float,
        b: float,
        quad_points: float,
        quad_count: int,
    ):  # TODO: quad_points might be an array
        return lib.folio_page_add_squiggly(
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_double(r),
            ct.c_double(g),
            ct.c_double(b),
            ct.c_double(quad_points),
            ct.c_double(quad_count),
        )

    @_with_error_handling(PageException)
    def add_strikeout(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        r: float,
        g: float,
        b: float,
        quad_points: float,
        quad_count: int,
    ):  # TODO: quad_points might be an array
        return lib.folio_page_add_strikeout(
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_double(r),
            ct.c_double(g),
            ct.c_double(b),
            ct.c_double(quad_points),
            ct.c_double(quad_count),
        )
