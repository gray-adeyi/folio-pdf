from enum import IntEnum, IntFlag, StrEnum


class ErrorCodes(IntEnum):
    OK = 0
    HANDLE = -1  # invalid or expired handle
    ARG = -2  # invalid argument (NULL, out of range)
    IO = -3  # file I/O error
    PDF = -4  # PDF generation/parsing error
    TYPE = -5  # handle type mismatch
    INTERNAL = -6  # unexpected internal error


class Alignments(IntEnum):
    LEFT = 0
    CENTER = 1
    RIGHT = 2
    JUSTIFY = 3


class VerticalAlignments(IntEnum):
    TOP = 0
    MIDDLE = 1
    BOTTOM = 2


class HeadingLevels(IntEnum):
    H1 = 1
    H2 = 2
    H3 = 3
    H4 = 4
    H5 = 5
    H6 = 6


class ListStyles(IntEnum):
    BULLET = 0
    DECIMAL = 1
    LOWER_ALPHA = 2
    UPPER_ALPHA = 3
    LOWER_ROMAN = 4
    UPPER_ROMAN = 5


class PDFALevels(IntEnum):
    PDFA_2B = 0
    PDFA_2U = 1
    PDFA_2A = 2
    PDFA_3B = 3
    PDFA_1B = 4
    PDFA_1A = 5


class EncryptionAlgorithms(IntEnum):
    RC4_128 = 0
    AES_128 = 1
    AES_256 = 2


class EncryptionPermissions(IntFlag):
    PRINT = 1 << 2  # bit 3: print
    MODIFY = 1 << 3  # bit 4: modify contents
    EXTRACT = 1 << 4  # bit 5: copy/extract text
    ANNOTATE = 1 << 5  # bit 6: annotations, fill forms
    FILL_FORMS = 1 << 8  # bit 9: fill form fields
    EXTRACT_ACCESS = 1 << 9  # bit 10: extract for accessibility
    ASSEMBLE = 1 << 10  # bit 11: insert/rotate/delete pages
    PRINT_HIGH = 1 << 11  # bit 12: high-quality print
    ALL = 0x0F3C


class ECCLevels(IntEnum):
    L = 0  # 7% recovery
    M = 1  # 15% recovery
    Q = 2  # 25% recovery
    H = 3  # 30% recovery


class FlexDirections(IntEnum):
    ROW = 0
    COLUMN = 1


class JustifyContents(IntEnum):
    START = 0
    END = 1
    CENTER = 2
    SPACE_BETWEEN = 3
    SPACE_AROUND = 4
    SPACE_EVENLY = 5


class AlignItems(IntEnum):
    STRETCH = 0
    START = 1
    END = 2
    CENTER = 3


class FlexWraps(IntEnum):
    NOWRAP = 0
    WRAP = 1


class StandardPDFFonts(StrEnum):
    HELVETICA = "Helvetica"
    HELVETICA_BOLD = "Helvetica-Bold"
    HELVETICA_OBLIQUE = "Helvetica-Oblique"
    HELVETICA_BOLD_OBLIQUE = "Helvetica-BoldOblique"

    TIMES_ROMAN = "Times-Roman"
    TIMES_BOLD = "Times-Bold"
    TIMES_ITALIC = "Times-Italic"
    TIMES_BOLD_ITALIC = "Times-BoldItalic"

    COURIER = "Courier"
    COURIER_BOLD = "Courier-Bold"
    COURIER_OBLIQUE = "Courier-Oblique"
    COURIER_BOLD_OBLIQUE = "Courier-BoldOblique"

    SYMBOL = "Symbol"
    ZAPF_DINGBATS = "ZapfDingbats"
