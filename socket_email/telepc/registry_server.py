"""Server-side helpers for Windows Registry read/write operations.

All functions operate on fully-qualified registry paths, optionally using
short hives (HKLM, HKCU, HKCR, HKU). The network entry point is ``registry``,
which receives JSON commands and performs the requested action.
"""

import json
import os
import re
import winreg


def parse_data(full_path):
    """Split a full registry path into ``(hive, key_path, value_name)``.

    Accepts short hive aliases and normalizes them; returns ``(None, None,
    None)`` on parsing errors.
    """
    try:
        full_path = re.sub(r"/", r"\\", full_path)
        hive = re.sub(r"\\.*$", "", full_path)
        if not hive:
            raise ValueError("Invalid 'full_path' param.")
        if len(hive) <= 4:
            if hive == "HKLM":
                hive = "HKEY_LOCAL_MACHINE"
            elif hive == "HKCU":
                hive = "HKEY_CURRENT_USER"
            elif hive == "HKCR":
                hive = "HKEY_CLASSES_ROOT"
            elif hive == "HKU":
                hive = "HKEY_USERS"
        reg_key = re.sub(r"^[A-Z_]*\\", "", full_path)
        reg_key = re.sub(r"\\[^\\]+$", "", reg_key)
        reg_value = re.sub(r"^.*\\", "", full_path)
        return hive, reg_key, reg_value
    except Exception:
        return None, None, None


def query_value(full_path):
    """Return ``["1", "1"]`` when a named value exists, else ``["0", "0"]``."""
    value_list = parse_data(full_path)
    try:
        opened_key = winreg.OpenKey(
            getattr(winreg, value_list[0]), value_list[1], 0, winreg.KEY_READ
        )
        winreg.QueryValueEx(opened_key, value_list[2])
        winreg.CloseKey(opened_key)
        return ["1", "1"]
    except Exception:
        return ["0", "0"]


def get_value(full_path):
    """Fetch a value and return ``["1", actual_value]`` or ``["0", "0"]``."""
    value_list = parse_data(full_path)
    try:
        opened_key = winreg.OpenKey(
            getattr(winreg, value_list[0]), value_list[1], 0, winreg.KEY_READ
        )
        value_of_value, value_type = winreg.QueryValueEx(opened_key, value_list[2])
        winreg.CloseKey(opened_key)
        return ["1", value_of_value]
    except Exception:
        return ["0", "0"]


def dec_value(c):
    """Convert a single hex digit to its integer value (0–15)."""
    c = c.upper()
    if ord("0") <= ord(c) and ord(c) <= ord("9"):
        return ord(c) - ord("0")
    if ord("A") <= ord(c) and ord(c) <= ord("F"):
        return ord(c) - ord("A") + 10
    return 0


def str_to_bin(s):
    """Convert a hexadecimal string to bytes (big-endian per byte)."""
    res = b""
    for i in range(0, len(s), 2):
        a = dec_value(s[i])
        b = dec_value(s[i + 1])
        res += (a * 16 + b).to_bytes(1, byteorder="big")
    return res


def str_to_dec(s):
    """Convert a hexadecimal string to a base-10 integer."""
    s = s.upper()
    res = 0
    for i in range(0, len(s)):
        v = dec_value(s[i])
        res = res * 16 + v
    return res


def set_value(full_path, value, value_type):
    """Create/update a value at ``full_path`` with the given ``value_type``.

    ``value_type`` is a string from the ``winreg`` constants, e.g. ``REG_SZ``,
    ``REG_DWORD``, ``REG_QWORD``, ``REG_BINARY``. Hex strings are converted for
    binary and integer types when required.
    """
    value_list = parse_data(full_path)
    try:
        winreg.CreateKey(getattr(winreg, value_list[0]), value_list[1])
        opened_key = winreg.OpenKey(
            getattr(winreg, value_list[0]), value_list[1], 0, winreg.KEY_WRITE
        )
        if "REG_BINARY" in value_type:
            if len(value) % 2 == 1:
                value += "0"
            value = str_to_bin(value)
        if "REG_DWORD" in value_type:
            if len(value) > 8:
                value = value[:8]
            value = str_to_dec(value)
        if "REG_QWORD" in value_type:
            if len(value) > 16:
                value = value[:16]
            value = str_to_dec(value)

        winreg.SetValueEx(
            opened_key, value_list[2], 0, getattr(winreg, value_type), value
        )
        winreg.CloseKey(opened_key)
        return ["1", "1"]
    except Exception:
        return ["0", "0"]


def delete_value(full_path):
    """Delete a named value at ``full_path`` if it exists."""
    value_list = parse_data(full_path)
    try:
        opened_key = winreg.OpenKey(
            getattr(winreg, value_list[0]), value_list[1], 0, winreg.KEY_WRITE
        )
        winreg.DeleteValue(opened_key, value_list[2])
        winreg.CloseKey(opened_key)
        return ["1", "1"]
    except Exception:
        return ["0", "0"]


def query_key(full_path):
    """Return success when a subkey exists under the given path."""
    value_list = parse_data(full_path)
    try:
        opened_key = winreg.OpenKey(
            getattr(winreg, value_list[0]),
            value_list[1] + r"\\" + value_list[2],
            0,
            winreg.KEY_READ,
        )
        winreg.CloseKey(opened_key)
        return ["1", "1"]
    except Exception:
        return ["0", "0"]


def create_key(full_path):
    """Create a new subkey at ``full_path`` and return a success flag."""
    value_list = parse_data(full_path)
    try:
        winreg.CreateKey(
            getattr(winreg, value_list[0]), value_list[1] + r"\\" + value_list[2]
        )
        return ["1", "1"]
    except Exception:
        return ["0", "0"]


def delete_key(full_path):
    """Delete a subkey at ``full_path`` and return a success flag."""
    value_list = parse_data(full_path)
    try:
        winreg.DeleteKey(
            getattr(winreg, value_list[0]), value_list[1] + r"\\" + value_list[2]
        )
        return ["1", "1"]
    except Exception:
        return ["0", "0"]


def registry(client):
    """Serve a registry editing session over ``client`` socket.

    Receives message headers that indicate payload size, then a JSON command
    with fields ``ID``, ``path``, ``name_value``, ``value``, and ``v_type``.
    Dispatches to helpers and returns a pair-like list flag and value.
    """
    BUFSIZ = 32768
    while True:
        header = client.recv(BUFSIZ).decode("utf8")
        if "STOP_EDIT_REGISTRY" in header:
            break
        data_sz = int(header)
        data = b""
        while len(data) < data_sz:
            packet = client.recv(BUFSIZ)
            data += packet

        msg = json.loads(data.decode("utf8"))
        # extract elements
        ID = msg["ID"]
        full_path = msg["path"]
        name_value = msg["name_value"]
        value = msg["value"]
        v_type = msg["v_type"]
        res = ["0", "0"]

        print(ID)
        print(full_path)
        print(name_value)
        print(value)
        print(v_type)

        # ID==0 run file.reg
        # path is detail of file .reg
        if ID == 0:
            try:
                outout_file = os.getcwd() + "\\run.reg"
                with open(outout_file, "w+") as f:
                    f.write(full_path)
                os.system(r"regedit /s " + os.getcwd() + "\\run.reg")
                res = ["1", "1"]
                print("file reg created")
            except Exception:
                res = ["0", "0"]
                print("cannot create file reg")

        elif ID == 1:
            res = get_value(full_path + r"\\" + name_value)

        elif ID == 2:
            res = set_value(full_path + r"\\" + name_value, value, v_type)

        elif ID == 3:
            res = create_key(full_path)

        elif ID == 4:
            res = delete_key(full_path + r"\\")
        client.sendall(bytes(res[0], "utf8"))
        client.sendall(bytes(str(res[1]), "utf8"))

    return
