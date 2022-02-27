from socket import socket, create_connection, AF_INET, SOCK_STREAM
from typing import Tuple
from threading import Lock
from listener import Listener
from logger import Logger


class Client:
    _sock: socket
    _listener: Listener
    _send_lock: Lock
    _timeout: float
    _logger: Logger

    def __init__(self, logger: Logger = None) -> None:
        if logger is None:
            logger = Logger()

        self._logger = logger
        self._sock = socket(AF_INET, SOCK_STREAM)
        self._listener = Listener(self._sock, logger=self._logger)
        self._send_lock = Lock()
        self._timeout = 5.0

    def start(self) -> None:
        self._logger.log('starting')
        self._listener.start()
        self._logger.log('started')

    def stop(self) -> None:
        self._logger.log('stopping')
        self._listener.stop(True)
        self._logger.log('stopped')

    def send(self, addr: Tuple[str, int], msg: str) -> None:
        with self._send_lock:
            with create_connection(addr, self._timeout) as conn:
                conn.sendall(msg.encode('utf-8'))

    def get_addr(self) -> Tuple[str, int]:
        return self._sock.getsockname()

    def __enter__(self) -> 'Client':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.stop()
        self._sock.close()
