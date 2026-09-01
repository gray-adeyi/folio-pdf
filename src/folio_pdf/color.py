from dataclasses import dataclass

from folio_pdf.enums import NamedColor


@dataclass
class Color:
    """
    Represents an RGB color with each channel in the range `0.0 - 1.0`.

    Common colors are available via the `Colors` enum that can be used to call
    the `from_named` class method. New colors can be created from
    normalized floats from instantiating the color class, 8-bit integers via `from_rgb`
    class method, or a CSS hex string via `from_hex` class method.

    Examples:
        ```python
        from folio_pdf import Color
        from folio_pdf.enums import Colors

        red = Color.from_named(Colors.RED)
        blue = Color.from_named('blue')
        green = Color.from_rgb(0,255,0)
        black = Color.from_hex("#000000") # with `#` prefix
        white = Color.from_hex("ffffff")
        ```
    """

    r: float
    g: float
    b: float

    @classmethod
    def from_named(cls, color: str | NamedColor):
        _color = color
        if isinstance(_color, str):
            _color = NamedColor(_color.lower())
        match _color:
            case NamedColor.BLACK:
                return cls(0, 0, 0)
            case NamedColor.WHITE:
                return cls(1, 1, 1)
            case NamedColor.RED:
                return cls(1, 0, 0)
            case NamedColor.GREEN:
                return cls(0, 1, 0)
            case NamedColor.BLUE:
                return cls(0, 0, 1)
            case NamedColor.GRAY:
                return cls(0.5, 0.5, 0.5)
            case NamedColor.LIGHT_GRAY:
                return cls(0.75, 0.75, 0.75)
            case NamedColor.DARK_GRAY:
                return cls(0.25, 0.25, 0.25)
            case NamedColor.NAVY:
                return cls(0, 0, 0.5)
            case NamedColor.TEAL:
                return cls(0, 0.5, 0.5)
            case NamedColor.ORANGE:
                return cls(1, 0.65, 0)
            case NamedColor.PURPLE:
                return cls(0.5, 0, 0.5)
            case NamedColor.YELLOW:
                return cls(1, 1, 0)
            case NamedColor.CYAN:
                return cls(0, 1, 1)
            case NamedColor.MAGENTA:
                return cls(1, 0, 1)
            case NamedColor.BROWN:
                return cls(0.6, 0.3, 0)
            case NamedColor.PINK:
                return cls(1, 0.75, 0.8)

    @classmethod
    def from_rgb(cls, r: float, g: float, b: float):
        return cls(r / 255, g / 255, b / 255)

    @classmethod
    def from_hex(cls, hex: str):
        _hex = hex[1:] if hex.startswith("#") else hex
        return cls.from_rgb(
            int(_hex[:2], 16),
            int(_hex[2:4], 16),
            int(_hex[4:], 16),
        )
