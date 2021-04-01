# File: ssh_connect
# Author: Theo Technicguy
# Interpreter: Python 3.9
# Ext: py
# Licensed under MIT. See LICENSE for details.
# -----------------------

import datetime
import getpass
import socket
import subprocess
from pathlib import Path

from ext import file_ops, parser

# ---------- START Program Constants ----------
__author__ = "Theo Technicguy"
__version__ = "0.1.0"

# === Paths ===
RECORD_PATH = Path("~/.ssh/record.json").expanduser()
CONFIG_PATH = Path("/etc/ssh/ssh-notify/ssh-notify.cfg")

# datetimes
NOW = datetime.datetime.now()
NOW_UTC = datetime.datetime.utcnow()
# ---------- END Program Constants ----------
iso_timestamp_utc = NOW_UTC.isoformat()

# Get current user
current_user = getpass.getuser()

# Get host name
host = socket.gethostname()

# Get client-side IP
# Styled `IP client_port host_port`
ip = subprocess.run("echo $SSH_CLIENT", shell=True, capture_output=True)
try:
    ip, client_port, host_port = ip.stdout.decode().strip().split()
except ValueError:
    # Connection from localhost
    ip, client_port, host_port = "localhost", -1, -1

# Load user record data
records = file_ops.read(RECORD_PATH)
ip_history = records.get(ip, None)

# Get first_conn and last_conn then set last_conn
if ip_history is None:
    first_conn = last_conn = NOW_UTC
    records[ip] = {
        "first_connection": NOW_UTC.isoformat(),
        "last_connection": NOW_UTC.isoformat(),
    }
else:
    first_conn = datetime.datetime.fromisoformat(
        ip_history.get("first_connection"),
    )
    last_conn = datetime.datetime.fromisoformat(
        ip_history.get("last_connection"),
    )
    records[ip]["last_connection"] = iso_timestamp_utc


# Read configutation file
config = file_ops.read(CONFIG_PATH)

config_tdelta = config["validation"]
tdelta = datetime.timedelta

# Get timedeltas
too_young = NOW_UTC - tdelta(days=config_tdelta["too_young"])
young = NOW_UTC - tdelta(days=config_tdelta["young"])
old = NOW_UTC - tdelta(days=config_tdelta["old"])
too_old = NOW_UTC - tdelta(days=config_tdelta["too_old"])

# Evaluate validation state
if first_conn > too_young or last_conn < too_old:
    state = 0
elif first_conn > young or last_conn < old:
    state = 1
else:
    state = 2
validation = ("new", "validating", "trusted")[state]

# Assemble export data
connection_data = {
    "user": current_user,
    "host": host,
    "client_ip": ip,
    "client_port": client_port,
    "host_port": host_port,
    "timestamp": NOW.isoformat(),
    "timestamp_utc": iso_timestamp_utc,
    "state": state,
    "validation": validation,
}

# Write to user records file.
file_ops.write(RECORD_PATH, records)

message = config["messages"][validation]

message["title"] = parser.message(message["title"], connection_data)
message["content"] = parser.message(message["content"], connection_data)
message["colour"] = parser.colour(message["colour"])


for service in config["services"]:
    exec(f"from services import {service}")
    exec(f"{service}.notify(data={connection_data}, message={message})")
