def shutdown(conn):
    conn.sendall(bytes("SHUTDOWN", "utf8"))

def logout(conn):
    conn.sendall(bytes("LOGOUT", "utf8"))

def restart(conn):
    conn.sendall(bytes("RESTART", "utf8"))
