import threading
import physical_bell
from const import test

class Ringer():
    def __init__(self):
        self.lock = threading.Lock()
        self.number = 0
        self.checkrep()

    def ring(self):
        self.lock.acquire()
        if self.number == 0:
            self._ring()
        self.number += 1
        self.lock.release()
        self.checkrep()

    def stop(self):
        self.lock.acquire()
        if self.number -1 == 0:
            self._stop()
        self.number -= 1
        self.lock.release()
        self.checkrep()

    def _ring(self):
        physical_bell.physical_ring()

    def _stop(self):
        physical_bell.physical_kill()

    def checkrep(self):
        if test:
            assert(self.number >= 0)
