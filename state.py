import const
import pickle
import os
import datetime

def load_state():
    if os.path.isfile(const.saved_state):
        with open(const.saved_state, 'r') as f:
            return pickle.load(f)
    else:
        return State()

class State:
    def __init__(self):
        self.alarms = []
        self.active = True
    def save(self):
        with open(const.saved_state, 'w') as f:
            pickle.dump(self, f)
    def add_alarm(self, alarm):
        const.narrate("ADDING ALARM:" + str(alarm))
        self.alarms.append(alarm)
        self.save()
    def pop_alarms_going_off(self):
        current = datetime.datetime.now()
        out = []
        mustPop = []
        for i in range(len(self.alarms)):
            alarm = self.alarms[i]
            if alarm[0] < current:
                out.append(alarm)
                mustPop.append(i)
        mustPop.reverse()
        for i in mustPop:
            self.alarms.pop(i)
        self.save()
        return out
