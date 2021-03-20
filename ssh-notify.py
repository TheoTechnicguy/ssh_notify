# File: ssh-notify
# Author: Theo Technicguy
# Interpreter: Python 3.9
# Ext: py
# Licensed under MIT. See LICENSE for details.
# -----------------------

import argparse
import base64
import json
import re
from pathlib import Path

# ---------- START Program Constants ----------
__author__ = "Theo Technicguy"
__version__ = "0.0.1"
WORK_DIR = Path(".")
RECORD_PATH = Path("~/.ssh/record.json").expanduser()
# ---------- END Program Constants ----------

# ---------- START Argument Parser ----------
parser = argparse.ArgumentParser(prog="ssh-notify")
subparser = parser.add_subparsers(dest="action", required=True)

# ~~~~~~~~~ START IP Parser ~~~~~~~~~
ip_parser = subparser.add_parser(
    "ip", help="IP related stuff like adding, listing and so."
)

ip_sub_parser = ip_parser.add_subparsers(dest="ip_action", required=True)

ip_list_parser = ip_sub_parser.add_parser("list", help="List recorded IPs.")
ip_add_parser = ip_sub_parser.add_parser("add", help="Add IPs to record.")
ip_rm_parser = ip_sub_parser.add_parser("del", help="Delete IPs from record.")
ip_reset_parser = ip_sub_parser.add_parser("reset", help="Reset data for an IP.")

ip_add_parser.add_argument("ip_addr", nargs="+", help="IP address to add.")
ip_rm_parser.add_argument("ip_addr", nargs="+", help="IP address to delete.")
ip_reset_parser.add_argument("ip_addr", nargs="+", help="IP address to reset.")

ip_list_parser.add_argument(
    "--no-hide",
    action="store_true",
    help="Do not hide IPs. IPs are hidden by default.",
)
ip_list_parser.add_argument(
    "--padd-zero",
    action="store_true",
    help="Padd IPs with leading zeros.",
)
# ~~~~~~~~~ END IP Parser ~~~~~~~~~

args = parser.parse_args()

# ---------- END Argument Parser ----------

print("#" * 15)
print(args)
print("#" * 15)

if args.action == "ip":

    # Start by checking if there is a record file.
    try:
        with RECORD_PATH.open("rb") as file:
            record = json.loads(base64.b64decode(file.read()))
    except FileNotFoundError:
        print("You do not have a record file setup.")
        exit()

    if args.ip_action == "list":
        sep = "-" * 91
        print(sep)
        print(
            f"| {'':6}IP{'':7} | {'':5}First Connection{'':5} |"
            + f" {'':5}Last Connection{'':6} | Connections |"
        )
        print(sep)
        for ip, info in record.items():
            ip_segments = ip.split(".")

            # Zero-fill/padding
            if args.padd_zero:
                for idx, segment in enumerate(ip_segments):
                    while len(segment) < 3:
                        segment = "0" + segment
                    ip_segments[idx] = segment

            # Hide bytes 2 and 3 in IP.
            if not args.no_hide:
                ip_segments[1:3] = ["***"] * 2

            ip = ".".join(ip_segments)
            print(
                f"| {ip:15} | {info['first_connection']:26} |"
                + f" {info['last_connection']:26} | {info['count']!s:11} |"
            )
        print(sep)
        exit()

    # Input validation and cleaning of IPs.
    ips = []
    for ipdx, ip in enumerate(args.ip_addr):
        # Clean leading zeros from input
        ip_segments = ip.split(".")

        for sdx, segment in enumerate(ip_segments):
            had_non_zero = False
            out_segment = ""

            for ddx, digit in enumerate(segment):
                if digit != "0":
                    out_segment += digit
                    had_non_zero = True
                elif digit == "0" and had_non_zero or ddx == len(segment) - 1:
                    out_segment += digit
                ip_segments[sdx] = out_segment

        ip = ".".join(ip_segments)

        # Validate IP by exact regex match.
        if re.fullmatch(r"(?:\d{1,3}\.){3}\d{1,3}", ip) is None:
            print(ip, "is not a valid IPv4 address, skipping.")
        else:
            ips.append(ip)

    if not len(ips):
        print("No valid IPs found. Exiting.")
        exit()

    if args.ip_action == "add":
        for ip in ips:
            if ip in record.keys():
                print(ip, "is already recorded, skipping.")
            else:
                record[ip] = {
                    "first_connection": "Never",
                    "last_connection": "Never",
                    "count": 0,
                }
                print("Added", ip, "to known IPs.")

        with RECORD_PATH.open("wb") as file:
            file.write(base64.b64encode(json.dumps(record).encode()))
        exit()

    if args.ip_action == "del":
        for ip in ips:
            if ip not in record.keys():
                print(ip, "is not recorded, skipping.")
            else:
                del record[ip]
                print("Deleted", ip, "from known IPs.")

        with RECORD_PATH.open("wb") as file:
            file.write(base64.b64encode(json.dumps(record).encode()))
        exit()

    if args.ip_action == "reset":
        for ip in ips:
            if ip not in record.keys():
                print(ip, "is not recorded, skipping.")
            else:
                record[ip] = {
                    "first_connection": "Never",
                    "last_connection": "Never",
                    "count": 0,
                }
                print("Reset", ip)

        with RECORD_PATH.open("wb") as file:
            file.write(base64.b64encode(json.dumps(record).encode()))
        exit()
