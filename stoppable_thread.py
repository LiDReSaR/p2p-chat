from flag import Flag
from threading import Thread


class StoppableThread(Thread):
    _flag: Flag

    def __init__(self, flag: Flag = None) -> None:
        super().__init__()

        if flag is None:
            flag = Flag()

        self._flag = flag

    def stop(self, wait: bool = False) -> None:
        self._flag.set(True)

        if wait:
            self.join()

    def is_stopped(self) -> bool:
        return self._flag.get()
