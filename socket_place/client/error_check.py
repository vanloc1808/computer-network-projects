import hashlib


def check_split_not_corrupted(s: bytearray) -> bool:
    if len(s) <= 43:
        return False

    data = s[3:-40]
    expected_hash = s[-40:]

    return hashlib.sha1(data).hexdigest().encode() == expected_hash