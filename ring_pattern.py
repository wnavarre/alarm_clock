import time
class ring_pattern: 
    def __init__(self, ringer):
        self.active = True
        self.ringer = ringer

    def idle(self, t, max_delay=.5):
        '''
        Spin for approximately t seconds, then return true
        EXCEPT, if a self.active is observed to be false. In that
        case, return false as soon as that is observed. 
        '''
        start = time.time()
        while time.time() - start < t:
            time.sleep(min(t * .1, max_delay))
            if not self.active:
                return False
        return True

    def stop_ringing(self):
        self.active = False

    def standard_ring(self, first=False):
        self.active = True
        if first:
            self.ringer.ring()
            self.idle(2, max_delay=.01)
            self.ringer.stop()
            self.idle(8)
        while self.active:
            self.ringer.ring()
            self.idle(30, max_delay=.01)
            self.ringer.stop()
            self.idle(20)

    def continuous_ring(self):
        self.active = True
        self.ringer.ring()
        self.idle(float("inf"), max_delay=.01)
        self.ringer.stop()
