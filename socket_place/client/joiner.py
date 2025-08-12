"""Reassemble ordered payload from validated UDP blocks.

Ensure to verify each block integrity before calling this function!
"""


def join(arr) -> bytearray:
    result = b""

    arr = sorted(arr)

    for sp in arr:
        result += sp[3:-40]  # Data part
    return result
