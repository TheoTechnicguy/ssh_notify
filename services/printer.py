# File: services/printer
# Author: Theo Technicguy
# Interpreter: Python 3.9
# Ext: py
# Licensed under MIT. See LICENSE for details.
# -----------------------


# ---------- START Program Constants ----------
__author__ = "Theo Technicguy"
__version__ = "1.0.0"
# ---------- END Program Constants ----------


def notify(data: dict, message: dict):
    """Print notifiction data."""
    print("data", data)
    print("message", message)
