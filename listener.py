from stoppable_thread import StoppableThread
from socket import socket, timeout
from typing import List
from processor import Processor
from flag import Flag
from logger import Logger


class Listener(StoppableThread):
    _timeout: float
    _sock: socket
    _processors: List[Processor]
    _logger: Logger

    def __init__(self, sock: socket, flag: Flag = None, logger: Logger = None) -> None:
        super().__init__(flag)

        if logger is None:
            logger = Logger()

        self._sock = sock
        self._processors = []
        self._timeout = 5.0
        self._logger = logger

    def run(self) -> None:
        self._logger.log(f'listening: {host}:{port}')
        self._sock.settimeout(self._timeout)
        self._sock.listen()
        (host, port) = self._sock.getsockname()

        try:
            while not self.is_stopped():
                try:
                    (conn, _) = self._sock.accept()
                    processor = Processor(conn, self._flag, self._logger)
                    conn.settimeout(self._timeout)
                    self._processors.append(processor)
                    processor.start()
                except timeout:
                    continue
        finally:
            self._sock.close()

        self._logger.log('listened')
