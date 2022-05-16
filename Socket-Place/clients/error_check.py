import hashlib

def check_split_not_corrupted(s: bytearray) -> bool:
    assert len(s) > 43
    
    data = s[3: -40]
    _hash = s[-40: ]

    return hashlib.sha1(data).hexdigest().encode() == _hash