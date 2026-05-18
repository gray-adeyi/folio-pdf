"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.color import Color
from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.enums import Alignments, Directions
from folio_pdf.exceptions import ParagraphException
from folio_pdf.font import Font

lib.folio_paragraph_new.argtypes = [
    ct.c_char_p,
    ct.c_uint64,
    ct.c_double,
]
lib.folio_paragraph_new.restype = ct.c_uint64

lib.folio_paragraph_new_embedded.argtypes = [ct.c_char_p, ct.c_uint64, ct.c_double]
lib.folio_paragraph_new_embedded.restype = ct.c_uint64

lib.folio_paragraph_free.argtypes = [ct.c_uint64]
lib.folio_paragraph_free.restype = None

lib.folio_paragraph_set_align.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_paragraph_set_align.restype = ct.c_int32

lib.folio_paragraph_set_leading.argtypes = [ct.c_uint64, ct.c_double]
lib.folio_paragraph_set_leading.restype = ct.c_int32

lib.folio_paragraph_set_space_before.argtypes = [ct.c_uint64, ct.c_double]
lib.folio_paragraph_set_space_before.restype = ct.c_int32

lib.folio_paragraph_set_space_after.argtypes = [ct.c_uint64, ct.c_double]
lib.folio_paragraph_set_space_after.restype = ct.c_int32

lib.folio_paragraph_set_background.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_paragraph_set_background.restype = ct.c_int32

lib.folio_paragraph_set_first_indent.argtypes = [ct.c_uint64, ct.c_double]
lib.folio_paragraph_set_first_indent.restype = ct.c_int32

lib.folio_paragraph_set_direction.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_paragraph_set_direction.restype = ct.c_int32

lib.folio_paragraph_set_orphans.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_paragraph_set_orphans.restype = ct.c_int32

lib.folio_paragraph_set_widows.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_paragraph_set_widows.restype = ct.c_int32

lib.folio_paragraph_set_ellipsis.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_paragraph_set_ellipsis.restype = ct.c_int32

lib.folio_paragraph_set_word_break.argtypes = [ct.c_uint64, ct.c_char_p]
lib.folio_paragraph_set_word_break.restype = ct.c_int32

lib.folio_paragraph_set_hyphens.argtypes = [ct.c_uint64, ct.c_char_p]
lib.folio_paragraph_set_hyphens.restype = ct.c_int32

lib.folio_paragraph_set_text_align_last.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_paragraph_set_text_align_last.restype = ct.c_int32

lib.folio_paragraph_add_run.argtypes = [
    ct.c_uint64,
    ct.c_char_p,
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_paragraph_add_run.restype = ct.c_int32


class Paragraph(AbstractFolioObject):
    """
    Represents a styled paragraph of text.
    """

    _requires_close = True

    def __init__(self, text: str, font: Font, font_size: float):
        self.__handle = lib.folio_paragraph_new(
            ct.c_char_p(text.encode()), font._handle, ct.c_double(font_size)
        )

    @classmethod
    def new_embedded(cls, text: str, font: Font, font_size: float):
        """
        Creates a paragraph that embeds the font subset in the PDF output.

        Args:
            text: the paragraph text
            font: the font to embed
            font_size: the font size in points

        Returns:
            a new `Paragraph` with an embedded font
        """
        obj = cls.__new__(cls)
        obj.__handle = lib.folio_paragraph_new_embedded(
            ct.c_char_p(text.encode()), font._handle, ct.c_double(font_size)
        )
        return obj

    @_with_error_handling(ParagraphException)
    def align(self, align: Alignments):
        """
        Sets the text alignment for this paragraph.

        Args:
            align: the desired `Alignments` value

        Returns:
            this paragraph, for chaining
        """
        return lib.folio_paragraph_set_align(self._handle, ct.c_int32(align.value))

    @_with_error_handling(ParagraphException)
    def leading(self, leading: float):
        """
        Sets the line-height multiplier for this paragraph.

        Args:
            leading: line height as a multiple of the font size (e.g., `1.5`)

        Returns:
            this paragraph, for chaining
        """
        return lib.folio_paragraph_set_leading(self._handle, ct.c_double(leading))

    @_with_error_handling(ParagraphException)
    def space_before(self, pts: float):
        """
        Sets the amount of space to add before this paragraph.

        Args:
            pts: vertical space in points

        Returns:
            this paragraph, for chaining
        """
        return lib.folio_paragraph_set_space_before(self._handle, ct.c_double(pts))

    @_with_error_handling(ParagraphException)
    def space_after(self, pts: float):
        """
        Sets the amount of space to add after this paragraph.

        Args:
            pts: vertical space in points

        Returns:
            this paragraph, for chaining
        """
        return lib.folio_paragraph_set_space_after(self._handle, ct.c_double(pts))

    @_with_error_handling(ParagraphException)
    def background(self, color: Color):
        """
        Sets the background color behind the paragraph text.

        Args:
            color: the background `Color`

        Returns:
            this paragraph, for chaining
        """
        return lib.folio_paragraph_set_background(
            self._handle,
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    @_with_error_handling(ParagraphException)
    def first_indent(self, pts: float):
        """
        Sets the first-line indent for this paragraph.

        Args:
            pts indent in points

        Returns:
            this paragraph, for chaining
        """
        return lib.folio_paragraph_set_first_indent(self._handle, ct.c_double(pts))

    @_with_error_handling(ParagraphException)
    def direction(self, dir: Directions):
        """
        Sets the writing direction (LTR, RTL, or AUTO) for this paragraph.

        `Directions.AUTO` runs the Unicode Bidi algorithm over the
        paragraph contents to infer direction from the dominant script.
        Direction influences the {@code /Lang} entry and structure attributes
        in tagged-PDF output (ISO 32000-2 §14.8.2).

        Args:
            dir: the desired `Directions` variant.

        Returns:
            this paragraph, for chaining
        """
        return lib.folio_paragraph_set_direction(self._handle, ct.c_int32(dir.value))

    @_with_error_handling(ParagraphException)
    def orphans(self, n: int):
        """
        Sets the minimum number of lines to keep at the bottom
        of a page (orphan control).

        Args:
            n: minimum orphan lines

        Returns:
            this paragraph, for chaining
        """
        return lib.folio_paragraph_set_orphans(self._handle, ct.c_int32(n))

    @_with_error_handling(ParagraphException)
    def widows(self, n: int):
        """
        Sets the minimum number of lines to keep at the top of a page (widow control).

        Args:
            n: minimum widow lines

        Returns
            this paragraph, for chaining
        """
        return lib.folio_paragraph_set_widows(self._handle, ct.c_int32(n))

    @_with_error_handling(ParagraphException)
    def ellipsis(self, enabled: bool):
        """
        Enables or disables ellipsis truncation when text overflows.

        Args:
            enabled: `True` to append an ellipsis on overflow

        Returns:
            this paragraph, for chaining
        """
        return lib.folio_paragraph_set_ellipsis(self._handle, ct.c_int32(enabled))

    @_with_error_handling(ParagraphException)
    def word_break(self, mode: str):
        """
        Sets the word-break mode for this paragraph.

        Args:
            mode: word-break mode string (e.g., `"break-all"`)

        Returns:
            this paragraph, for chaining
        """
        return lib.folio_paragraph_set_word_break(
            self._handle,
            ct.c_char_p(mode.encode()),
        )

    @_with_error_handling(ParagraphException)
    def hyphens(self, mode: str):
        """
        Sets the hyphenation mode for this paragraph.

        Args:
            mode: hyphenation mode string (e.g., `"auto"`)

        Returns:
            this paragraph, for chaining
        """
        return lib.folio_paragraph_set_hyphens(self._handle, ct.c_char_p(mode.encode()))

    @_with_error_handling(ParagraphException)
    def text_align_last(self, align: Alignments):
        """
        Controls the alignment of the last line in a justified paragraph.

        Args:
            align: alignment to apply to the final line

        Returns:
            this paragraph, for chaining
        """
        return lib.folio_paragraph_set_text_align_last(
            self._handle, ct.c_int32(align.value)
        )

    @_with_error_handling(ParagraphException)
    def add_run(
        self,
        text: str,
        font: Font,
        font_size: float,
        color: Color,
    ):
        """
        Appends a styled text run to this paragraph.

        Args:
            text: the run text
            font: the font for this run
            font_size: the font size in points
            color: the text color

        Returns:
            this paragraph, for chaining
        """
        return lib.folio_paragraph_add_run(
            self._handle,
            ct.c_char_p(text.encode()),
            font._handle,
            ct.c_double(font_size),
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    def close(self):
        lib.folio_paragraph_free(self._handle)

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)
