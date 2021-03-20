# File: ext/test_file_ops
# Author: Theo Technicguy
# Interpreter: Python 3.9
# Ext: py
# Lisenced under MIT. See LICENSE for details.
# -----------------------

import base64
import json
from pathlib import Path

import file_ops

# ---------- START Program Constants ----------
__author__ = "Theo Technicguy"
__version__ = "0.1.0"
# ---------- END Program Constants ----------

dict_data = {
    "1.1.1.1": {
        "first_connection": "2000-01-01T00:00:00.000001",
        "last_connection": "2000-01-01T00:00:00.000001",
        "count": 52,
    },
    "2.2.2.2": {
        "first_connection": "3000-01-01T00:00:00.000001",
        "last_connection": "9999-12-31T23:59:59.999999",
        "count": 99999999999,
    },
}

file_data = (
    "eyIxLjEuMS4xIjogeyJmaXJzdF9jb25uZWN0aW9uIjogIjIwMD\n"
    "AtMDEtMDFUMDA6MDA6MDAuMDAwMDAxIiwgImxhc3RfY29ubmVj\n"
    "dGlvbiI6ICIyMDAwLTAxLTAxVDAwOjAwOjAwLjAwMDAwMSIsIC\n"
    "Jjb3VudCI6IDUyfSwgIjIuMi4yLjIiOiB7ImZpcnN0X2Nvbm5l\n"
    "Y3Rpb24iOiAiMzAwMC0wMS0wMVQwMDowMDowMC4wMDAwMDEiLC\n"
    "AibGFzdF9jb25uZWN0aW9uIjogIjk5OTktMTItMzFUMjM6NTk6\n"
    "NTkuOTk5OTk5IiwgImNvdW50IjogOTk5OTk5OTk5OTl9fQ==\n"
)


def test_write_file(tmpdir):
    """Test writing operation with string."""
    # Set test variables
    file = tmpdir + "/file-w.tst"

    # Test file does not exist.
    assert not Path(file).exists(), "File already exists."

    # Run wirte operation
    file_ops.write(file, dict_data)

    # Test file exists.
    assert Path(file).exists(), "File was not created."

    # Get file contents
    with open(file, "r") as f:
        actual = f.read()

    # Compare
    assert actual == file_data


def test_write_path(tmpdir):
    """Test writing operation with Path."""
    # Set test variables
    file = Path(tmpdir) / "path-w.tst"

    # Test file does not exist.
    assert not file.exists(), "File already exists."

    # Run wirte operation
    file_ops.write(file, dict_data)

    # Test file exists.
    assert file.exists(), "File was not created."

    # Get file contents
    with file.open("r") as f:
        actual = f.read()

    # Compare
    assert actual == file_data


def test_add_file(tmpdir):
    """Test add writing operation with string."""
    # Set test variables
    file = tmpdir + "/file-a.tst"
    data_one = {list(dict_data.keys())[0]: [list(dict_data.keys())[0]]}

    # Create test file.
    with file.open("wb+") as f:
        f.write(base64.b64encode(json.dumps(data_one).encode()))

    # Test file exists.
    assert Path(file).exists(), "Test file was not created."

    # Run wirte operation
    file_ops.write(file, dict_data)

    # Test file exists.
    assert Path(file).exists(), "File was deleted."

    # Get file contents
    with open(file, "r") as f:
        actual = f.read()

    # Compare
    assert actual == file_data


def test_add_path(tmpdir):
    """Test add writing operation with Path."""
    # Set test variables
    file = Path(tmpdir) / "path-a.tst"
    data_one = {list(dict_data.keys())[0]: [list(dict_data.keys())[0]]}

    # Create test file.
    with file.open("wb+") as f:
        f.write(base64.b64encode(json.dumps(data_one).encode()))

    # Test file exists.
    assert file.exists(), "Test file was not created."

    # Run wirte operation
    file_ops.write(file, dict_data)

    # Test file exists.
    assert file.exists(), "File was deleted."

    # Get file contents
    with file.open("r") as f:
        actual = f.read()

    # Compare
    assert actual == file_data


def test_read_file(tmpdir):
    """Test reading operation with string."""
    file = tmpdir + "/file-r.tst"

    with open(file, "w+") as f:
        f.write(file_data)

    # Test file does not exist.
    assert Path(file).exists(), "Test file was not created."

    actual = file_ops.read(file)

    assert actual == dict_data


def test_read_path(tmpdir):
    """Test reading operation with string."""
    file = Path(tmpdir) / "path-r.tst"

    with file.open("w+") as f:
        f.write(file_data)

    # Test file does not exist.
    assert file.exists(), "Test file was not created."

    actual = file_ops.read(file)

    assert actual == dict_data
