import time
import datetime
import sys
import const


def parseBareTime(timeString):
    parts = timeString.split(":")
    parts = map(int, map(lambda x: x.strip(), parts))
    if len(parts) == 1:
        parts.append(0)
    if len(parts) != 2:
        sys.stderr.write("ERROR: timeString be in the form of H:MM or H")
    hour, minute = parts
    parsed = datetime.datetime.now()
    parsed = parsed.replace(hour=hour, minute=minute, second=0)
    while parsed < datetime.datetime.now():
        parsed += datetime.timedelta(days=1)
    const.narrate("Interpreting " + timeString + " as " + str(parsed))
    return parsed

def parseRange(rangeString):
    timeStrings = rangeString.split("-")
    if len(timeStrings) != 2:
        sys.stderr.write("ERROR: rangeString should contain exactly one hyphen\n")
        raise ValueError
    start, deadline = map(parseBareTime, timeStrings)
    if not (start <= deadline):
        sys.stderr.write("ERROR: start time should be before deadline\n")
        raise ValueError
    return start, deadline

