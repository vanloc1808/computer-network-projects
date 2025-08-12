import hashlib
from typing import List


class Splitter:
    """Split a bytearray payload into fixed-size blocks with id and SHA1 hash.

    Layout per block:
    - 3 bytes: zero-padded block id (ASCII)
    - N bytes: payload (padded with nulls)
    - 40 bytes: hex-encoded SHA1 of the payload
    """

    def __init__(self, block_size: int):
        """Create a splitter and compute usable payload size per block."""
        # first 3 bytes for id, 40 bytes for SHA1 hash
        assert block_size > 43, "Block size must be greater than 43"
        self.block_size = block_size
        self.actual_size = block_size - 43

    def split_from_bytearray(self, payload: bytearray) -> List[bytearray]:
        """Return a list of blocks containing id, padded data and checksum."""
        result: List[bytearray] = []

        for i in range(0, len(payload), self.actual_size):
            chunk = payload[i : i + self.actual_size]
            chunk = chunk.ljust(self.actual_size, b"\x00")

            block_id = str(i // self.actual_size).rjust(3, "0").encode()
            checksum = hashlib.sha1(chunk).hexdigest().encode()
            result.append(block_id + chunk + checksum)
        return result


# Backwards compatibility alias
Spliter = Splitter
