"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

_NOT_IMPLEMENTED_ERROR = NotImplementedError(
    "this functionality is yet to be implemented"
)


class FolioPDFException(Exception): ...


class DocumentException(FolioPDFException): ...


class PageException(FolioPDFException): ...


class ParagraphException(FolioPDFException): ...


class HeadingException(FolioPDFException): ...


class TableException(FolioPDFException): ...


class TableCellException(FolioPDFException): ...


class WriteOptionsException(FolioPDFException): ...


class ImageException(FolioPDFException): ...


class ImageElementException(FolioPDFException): ...


class DivException(FolioPDFException): ...


class ListException(FolioPDFException): ...


class LinkException(FolioPDFException): ...


class RunListException(FolioPDFException): ...


class BarcodeElementException(FolioPDFException): ...


class SVGElementException(FolioPDFException): ...


class FlexException(FolioPDFException): ...


class FlexItemException(FolioPDFException): ...


class SignerOptionsException(FolioPDFException): ...


class PDFMergerException(FolioPDFException): ...


class FloatException(FolioPDFException): ...


class RedactorOptionsException(FolioPDFException): ...
