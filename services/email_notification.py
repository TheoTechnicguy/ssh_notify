# File: services/email
# Author: Theo Technicguy
# Interpreter: Python 3.9
# Ext: py
# Licensed under MIT. See LICENSE for details.
# -----------------------

import smtplib
from email.message import EmailMessage
from email.utils import make_msgid
from pathlib import Path

from ext import file_ops, parser, colours

# ---------- START Program Constants ----------
__author__ = "Theo Technicguy"
__version__ = "0.0.1"
EMAIL_CONFIG_PATH = Path("/etc/ssh/ssh-notify/email.cfg")
# ---------- END Program Constants ----------

email_config = file_ops.read(EMAIL_CONFIG_PATH)


def notify(data: dict, message: dict):
    """Get data from connection module and send notification email."""
    # Get message overwrite
    message_overwrite = email_config.get("message", message)
    message = message_overwrite.get(data["validation"], message)

    # Merge data and message dicts
    fill = data | message
    fill["colour"] = colours.hex_to_html(fill["colour"])

    sender = email_config["sender_email"]
    # ---------- START Compose Email ----------
    email = EmailMessage()
    asparagus_cid = make_msgid()

    with open(email_config["template_path"], "r") as template_file:
        template = parser.message(template_file.read(), fill)

    email.add_alternative(
        template.format(asparagus_cid=asparagus_cid[1:-1]), subtype="html"
    )

    email["Subject"] = message["title"]
    email["From"] = sender
    email["To"] = email_config["receivers"]
    # ---------- END Compose Email ----------

    # Get SSL connection according to configuration
    if email_config["ssl"]:
        connection = smtplib.SMTP_SSL
    else:
        connection = smtplib.SMTP

    host, port = email_config["host"], email_config["port"]
    with connection(host=host, port=port) as server:
        server.login(sender, email_config["password"])

        # Use TLS according to configuration
        if email_config["tls"]:
            server.starttls()

        server.send_message(email)
