# File: services/discord
# Author: Theo Technicguy
# Interpreter: Python 3.9
# Ext: py
# Licensed under MIT. See LICENSE for details.
# -----------------------

import json
from pathlib import Path

import requests

from ext import file_ops, parser

# ---------- START Program Constants ----------
__author__ = "Theo Technicguy"
__version__ = "0.0.1"
DISCORD_CONFIG_PATH = Path("/etc/ssh/ssh-notify/discord.cfg")
# ---------- END Program Constants ----------

discord_config = file_ops.read(DISCORD_CONFIG_PATH)
discord_webhook = discord_config["webhook"]


def notify(data: dict, message: dict):
    """Get data from connection module."""
    discord_message = discord_config["messages"][data["validation"]]
    discord_message["content"] = parser.message(
        discord_message["content"],
        data,
    )

    for key, value in discord_message["embed"].items():
        if key == "color":
            parsed = eval(parser.colour(value))
            print(parsed)
        else:
            parsed = parser.message(value, data)
        discord_message["embed"][key] = parsed

    print(
        requests.post(
            discord_webhook,
            headers={"Content-Type": "application/json"},
            data=json.dumps(
                {
                    "username": data["host"],
                    "content": discord_message["content"],
                    "embeds": [discord_message["embed"]],
                }
            ),
        )
    )
