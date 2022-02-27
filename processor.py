from logger import Logger
from stoppable_thread import StoppableThread
from socket import socket, timeout
from flag import Flag


class Processor(StoppableThread):
    _conn: socket
    _logger: Logger

    def __init__(self, conn: socket, flag: Flag = None, logger: Logger = None) -> None:
        super().__init__(flag)

        if logger is None:
            logger = Logger()

        self._logger = logger
        self._conn = conn

    def run(self) -> None:
        try:
            while not self.is_stopped():
                try:
                    data = self._recv_all()

                    if len(data) < 1:
                        break

                    msg = data.decode('utf-8')
                    (host, port) = self._conn.getsockname()
                    self._logger.log(f'({host}:{port}): {msg}')
                except timeout:
                    continue
        finally:
            self._conn.close()

    def _recv_all(self) -> bytes:
        data = b''

        while True:
            part = self._conn.recv(1024)
            data += part

            if len(part) < 1024:
                break

        return data
