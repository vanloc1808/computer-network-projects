"""Legacy helpers to request shutdown, logout or restart on the client."""


def shutdown(conn):
    """Send a shutdown command over the socket connection."""
    conn.sendall(bytes("SHUTDOWN", "utf8"))


def logout(conn):
    """Send a logout command over the socket connection."""
    conn.sendall(bytes("LOGOUT", "utf8"))


def restart(conn):
    """Send a restart command over the socket connection."""
    conn.sendall(bytes("RESTART", "utf8"))
