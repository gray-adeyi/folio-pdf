"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

from folio_pdf.elements import (
    AreaBreak,
    BarcodeElement,
    Columns,
    Div,
    Flex,
    Float,
    Grid,
    Heading,
    ImageElement,
    LineSeparator,
    Link,
    List,
    Paragraph,
    SVGElement,
    TabbedLine,
    Table,
)

Element = (
    AreaBreak
    | BarcodeElement
    | Columns
    | Div
    | Flex
    | Float
    | Grid
    | Heading
    | ImageElement
    | LineSeparator
    | Link
    | Paragraph
    | SVGElement
    | Table
    | List
    | TabbedLine
)
