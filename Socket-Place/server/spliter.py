from typing import List
import hashlib

class Spliter(object):
    def __init__(self, block_size: int):
        # first 3 bytes for id, 40 bytes for SHA1 hash!
        assert block_size > 43, "Block size must greater than 43!"
        self.block_size = block_size
        self.actual_size = block_size - 43
    
    
    def split_from_bytearray(self, s: bytearray) -> List[bytearray]:
        result = []

        for i in range(0, len(s), self.actual_size):
            tmp = s[i: i + self.actual_size]
            tmp = tmp.ljust(self.actual_size, b'\x00')
            
            _id = str(i // self.actual_size).rjust(3, "0").encode()
            _hash = hashlib.sha1(tmp).hexdigest().encode()
            result.append(_id + tmp + _hash)
        return result
