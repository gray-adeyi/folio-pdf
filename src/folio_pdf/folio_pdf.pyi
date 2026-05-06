from folio_pdf.elements import (
    List,
    Table,
    SVGElement,
    Paragraph,
    Link,
    LineSeparator,
    ImageElement,
    Heading,
    Grid,
    Float,
    Flex,
    Div,
    Column,
    BarcodeElement,
    AreaBreak,
    TabbedLine,
)

Element = (
    AreaBreak
    | BarcodeElement
    | Column
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
