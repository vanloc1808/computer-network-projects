import hashlib


"""Integrity utilities for validating UDP blocks with a trailing SHA1 hash."""


def check_split_not_corrupted(s: bytearray) -> bool:
    """Return True when the block's SHA1 matches its payload segment.

    Expects the block layout: 3 bytes id, payload bytes, 40 bytes hex SHA1.
    """
    if len(s) <= 43:
        return False

    data = s[3:-40]
    expected_hash = s[-40:]

    return hashlib.sha1(data).hexdigest().encode() == expected_hash
