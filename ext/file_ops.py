# File: ext/file_ops
# Author: Theo Technicguy
# Interpreter: Python 3.9
# Ext: py
# Licensed under MIT. See LICENSE for details.
# -----------------------

import base64
import json
from pathlib import Path
from typing import Union

# ---------- START Program Constants ----------
__author__ = "Theo Technicguy"
__version__ = "0.1.0"
# ---------- END Program Constants ----------


def read(file: Union[Path, str]):
    """Read record file.

    pre: record file exists.
    post: Read file.
    return: file content: dict
    """
    if isinstance(file, str):
        file = Path(file)

    with file.open("rb") as file:
        return json.loads(base64.b64decode(file.read()).decode())


def write(file: Union[Path, str], data: dict):
    """Write or create record file.

    pre: --
    post: write file in 50 char block. Create file if it desn't exist.
    return: file content: dict
    """
    if isinstance(file, str):
        file = Path(file)
    enc = base64.b64encode(json.dumps(data).encode())

    # Armor output into 50-char long lines.
    out = b""
    for idx in range(len(enc) // 50 + 1):
        out += enc[idx * 50 : (idx + 1) * 50] + b"\n"

    with file.open("wb+") as file:
        file.write(out)
