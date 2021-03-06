import thread
import wake_cycle
import time
import const
import state
import parsing
import Queue
import sys
import calendar
import abstract_ringer
import subprocess

queues = {}
state = state.load_state()
ringer = abstract_ringer.Ringer()

def wait_for_alarms():
    while True:
        time.sleep(1)
        for alarm in state.pop_alarms_going_off():
            const.narrate("Setting off alarm: " + str(alarm))
            wake_cycle.wake(queues, ringer, deadline=alarm[1])

def run_command(command):
    if command == "SHOW":
        print state.alarms
        return
    if command == "ACTIVES?":
        print len(queues)
        return
    try:
        state.add_alarm(parsing.parseRange(command))
    except ValueError:
        sys.stderr.write("ERROR!\n")

def listen_for_commands():
    while True:
        command = raw_input("alarm> ")
        if command == "":
            continue
        if command[0] == "/":
            dispatch_command(command[1:])
            continue
        run_command(command)

def listen_for_buttons():
    P = subprocess.Popen(["python", "-u", "button_inputs.py"], bufsize=0, shell=False, stderr=None, stdout=subprocess.PIPE)
    print "ITERABLE TO READ FROM BUTTON INPUTS!"
    while True:
        command = P.stdout.readline()
        command = command.strip()
        print command
        if not dispatch_command(command):
            print "ATTEMPT TO RING!"
            ringer.ring()
            time.sleep(1)
            ringer.stop()

def try_to_deliver(command, q):
    try:
        q.put(command, True, 3600)
    except Queue.Full:
        pass

def dispatch_command(command):
    need_note = queues.values()
    for q in need_note:
        thread.start_new_thread(try_to_deliver, (command, q))
    out = len(need_note) != 0
    if out:
        print "DID DISPATCH!"
    else:
        print "NO QUEUES TO DISPATCH TO!"
    return out

thread.start_new_thread(wait_for_alarms, ())
thread.start_new_thread(listen_for_buttons, ())
listen_for_commands()
