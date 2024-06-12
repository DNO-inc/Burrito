import socket

from burrito.utils.logger import get_logger


def burrito_ping(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((host, int(port)))
    except socket.error:
        get_logger().critical(f"({host}, {port}) is unreachable")
    except Exception as exc:
        get_logger().error(exc)
