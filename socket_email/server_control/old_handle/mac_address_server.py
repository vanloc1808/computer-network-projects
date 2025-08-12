"""Legacy helper to query MAC address via old socket protocol."""

BUFSIZ = 1024 * 4


def mac_address(client):
    """Return the formatted MAC address string received from the server."""
    res = client.recv(BUFSIZ).decode("utf8")
    res = res[2:].upper()
    res = ":".join(res[i : i + 2] for i in range(0, len(res), 2))
    return res
