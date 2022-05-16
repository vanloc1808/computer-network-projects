
# Ensure you check integrity before joining!
def join(arr) -> bytearray:
    result = b''

    arr = sorted(arr)

    for sp in arr:
        result += sp[3 : -40] # Data part
    return result