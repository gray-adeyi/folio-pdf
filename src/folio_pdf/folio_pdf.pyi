from folio_pdf.table import Table
from folio_pdf.svg_element import SVGElement
from folio_pdf.paragraph import Paragraph
from folio_pdf.link import Link
from folio_pdf.line_separator import LineSeparator
from folio_pdf.image_element import ImageElement
from folio_pdf.heading import Heading
from folio_pdf.grid import Grid
from folio_pdf.float import Float
from folio_pdf.flex import Flex
from folio_pdf.div import Div
from folio_pdf.columns import Column
from folio_pdf.barcode_element import BarcodeElement
from folio_pdf.area_break import AreaBreak

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
)
