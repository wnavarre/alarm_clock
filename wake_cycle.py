import thread
import ring_pattern
import time
import const
import Queue
import datetime

sleep_time = 60 * 5

def readCommand(commands, timeout):
    try:
        out = commands.get(True, timeout)
    except Queue.Empty:
        return ""
    return out

def wake(command_storage, ringer, deadline=float("inf")):
    thread.start_new_thread(wake_thread, (command_storage, ringer, deadline))

def wake_thread(command_storage, ringer, deadline):
    thread_id = thread.get_ident()
    commands = Queue.Queue()
    command_storage[thread_id] = commands
    normal_alarm(commands, ringer, deadline)
    command_storage.pop(thread_id)
    

def normal_alarm(commands, ringer, deadline):
    const.narrate("Begin normal alarm...")
    ring = ring_pattern.ring_pattern(ringer)
    thread.start_new_thread(ring.standard_ring, (True,))

    while datetime.datetime.now() < deadline:
        if not ring.active:
            thread.start_new_thread(ring.standard_ring, ())
        command = readCommand(commands, 15)
        if command == "SLEEP":
            ring.stop_ringing()
            sleep(commands, ringer, deadline)
        elif command == "AWAKE":
            ring.stop_ringing()
            return
    ring.stop_ringing()
    late_alarm(commands, ringer, deadline)

def sleep(commands, ringer, deadline):
    const.narrate("Snooze...")
    wait_until = min(deadline, datetime.datetime.now() + datetime.timedelta(seconds=5))
    while datetime.datetime.now() < wait_until:
        time.sleep(30)

def late_alarm(commands, ringer, deadline):
    const.narrate("Begin late alarm...")
    ring = ring_pattern.ring_pattern(ringer)
    thread.start_new_thread(ring.continuous_ring, ())
    while True:
        command = commands.get(True)
        if command == "AWAKE":
            ring.stop_ringing()
            return
