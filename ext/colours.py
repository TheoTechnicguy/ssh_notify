# File: ext/colours
# Author: Theo Technicguy
# Interpreter: Python 3.9
# Ext: py
# Licensed under MIT. See LICENSE for details
# -----------------------

# ---------- START Program Constants ----------
__author__ = "Theo Technicguy"
__version__ = "0.1.1"
__doc__ = "Standard Colours Library"
# ---------- END Program Constants ----------

red = "0xFF0000"
dark_orange = "0xFF4000"
orange = "0xFF8000"
light_orange = "0xFFBF00"
yellow = "0xFFFF00"
lime_yellow = "0xBFFF00"
lime = "0x80FF00"
light_green = "0x80FF00"
green = "0x00FF00"
tale_green = "0x00FF40"
tale = "0x00FF80"
tale_aqua = "0x00FFBF"
aqua = "0x00FFFF"
cyan = "0x00BFFF"
dark_cyan = "0x0080FF"
light_blue = "0x0040FF"
blue = "0x0000FF"
purple = "0x4000FF"
light_purple = "0x8000FF"
light_magenta = "0xBF00FF"
magenta = "0xFF00FF"
pink = "0xFF00BF"
dark_pink = "0xFF0080"
pink_red = "0xFF0040"

colours = [
    red,
    dark_orange,
    orange,
    light_orange,
    yellow,
    lime_yellow,
    lime,
    light_green,
    green,
    tale_green,
    tale,
    tale_aqua,
    aqua,
    cyan,
    dark_cyan,
    light_blue,
    blue,
    purple,
    light_purple,
    light_magenta,
    magenta,
    pink,
    dark_pink,
    pink_red,
]


def rgb_to_hex(rgb: tuple) -> str:
    """Retrun a hexadecimal repesetation of the colour.

    pre: --
    param: rgb: tuple - a RGB tuple notation of a colour.
    post: str of len == 8
    return: str - hexadecimal repesetation of the colour.
    """
    out = "0x"
    for part in rgb:
        hx = hex(part)[2:]
        while len(hx) < 2:
            hx = "0" + hx
        out += hx
    return out


def rgb_to_int(rgb: tuple) -> int:
    """Retrun a integer repesetation of the colour.

    pre: --
    param: rgb: tuple - a RGB tuple notation of a colour.
    post: int
    return: int - integer repesetation of the colour.
    """
    return eval(rgb_to_hex(rgb))


def hex_to_rgb(hx: str) -> tuple:
    """Return a RGB tuple representation of the colour.

    pre: --
    param: hx: str - hexadecimal notation of the colour
    post: tuple.
    return: tuple - RGB notation of th colour.
    """
    hx = hx.strip("#")

    if hx.startswith("0x"):
        hx = hx[2:]

    return tuple([int(hx[i : i + 2], 16) for i in (0, 2, 4)])


def rgb_to_cmyk(rgb: tuple) -> tuple:
    """Return a CMYK tuple representation of the colour.

    pre: --
    param: rgb: tuble - RGB notation of the colour
    post: tuple.
    return: tuple - CMYK notation of th colour.
    """
    r, g, b = rgb
    if (r, g, b) == (0, 0, 0):
        # black
        return (0, 0, 0, 100)

    # rgb [0,255] -> cmy [0,1]
    c = 1 - r / 255
    m = 1 - g / 255
    y = 1 - b / 255

    # extract out k [0, 1]
    min_cmy = min(c, m, y)
    c = (c - min_cmy) / (1 - min_cmy)
    m = (m - min_cmy) / (1 - min_cmy)
    y = (y - min_cmy) / (1 - min_cmy)
    k = min_cmy

    # rescale to the range [0,CMYK_SCALE]
    return (c * 100, m * 100, y * 100, k * 100)


def hex_to_html(hx: str) -> str:
    """Return HTML expression of the hexadecimal colour."""
    return "#" + hx[2:]
