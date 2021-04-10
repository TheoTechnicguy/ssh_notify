# File: ext/parser
# Author: Theo Technicguy
# Interpreter: Python 3.9
# Ext: py
# -----------------------

from . import colours

# ---------- START Program Constants ----------
__author__ = "Theo Technicguy"
__version__ = "0.1.0"
# ---------- END Program Constants ----------


def colour(name: str) -> str:
    """Convert standard string colour to hexadeimal string.

    pre: Standard colours library in same package
    args:
        name: str - Standard colour name.
    return: Hexadeimal string representation of the colour.
    """
    return eval(f"colours.{name}")


def message(
    template: str, data: dict, start_flag: str = "{", end_flag: str = "}"
) -> str:
    """Insert data values into template.

    pre: --
    args:
        template: str - Template to fill.
        data: dict - key representing template variables.
    opts:
        start_flag: str (`{`) - Start flag.
        end_flag: str (`}`) - End flag.
    return: Filled template
    """
    if (start_flag, end_flag) == ("{", "}"):
        try:
            template = template.format(**data)
        except KeyError:
            pass
    else:
        for key, value in data.items():
            template = template.replace(
                start_flag + str(key) + end_flag,
                str(value),
            )
    return template
