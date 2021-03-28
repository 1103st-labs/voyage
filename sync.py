import waypoint_def as way
from backports import zoneinfo
import datetime
import re
from icalevents.icalevents import events as get_events


MAX_LOOK = 20
MIN_LOOK = 24
SYNC_SLEEP = (60 * 2)
HEADINGS = ["Default", "MED", "EMERGENCY", "NMT", "SOCIAL", "CLEAN"]
LOCAL_TIMEZONE = zoneinfo.ZoneInfo("America/Denver")


def add_ical(url: "string ical url",
             scale: "int to scale cost by"
             = 1,
             reg: "name filter in regex"
             = ".*",
             sieve: "a python function that returns true or false"
             = lambda x: True,
             a_time: "days ahead for a_time delta"
             = 2,
             default_dur: "min default duration of event"
             = 60,
             default_due: "what datetime time to set if event is all day"
             = datetime.time(hour=23, minute=59, tzinfo=LOCAL_TIMEZONE),
             paradox: "Are zero length events allowed"
             = True,
             heading: "str headig. for safety use an index into HEADING"
             = "Default"):
    """Default add ical to heading method"""
    try:
        events = get_events(url,
                            start=(datetime.datetime.now(LOCAL_TIMEZONE) -
                                   datetime.timedelta(hours=MIN_LOOK)),
                            end=(datetime.datetime.now(LOCAL_TIMEZONE) +
                                   datetime.timedelta(days=MAX_LOOK)))
        ret = []
        for x in events:
            if (re.search(reg, x.summary) and sieve(x.summary)):
                args = {}
                tmp = (x.end - x.start)
                is_temporal = (tmp.seconds > 60) if not paradox else True
                args["des"] = x.summary
                args["due"] = x.end.astimezone(LOCAL_TIMEZONE)\
                        if (not x.all_day) and (is_temporal)\
                    else datetime.datetime.combine(x.end, default_due,
                                                   LOCAL_TIMEZONE)
                args["dur"] = ((tmp.days * 1440) + int((tmp.seconds / 60)))\
                    if (not x.all_day) and (is_temporal) and not paradox\
                    else default_dur
                if (args["dur"] == 0):
                    print(f'ERR: Zero duration event: {x.summary}')
                args["cost"] = scale * args["dur"]
                tmp = x.time_left()
                args["plat"] = ((tmp.days * 1440) + int((tmp.seconds / 60)))\
                        if (datetime.datetime.now(LOCAL_TIMEZONE) <
                            (args["due"] - datetime.timedelta(days=1))) else 0
                args["a_time"] = a_time
                args["heading"] = heading
                ret.append(way.Waypoint(**args))
    except Exception as e:
        print(e)
        print("ERR: Single add failed..... moving on")
        ret = []
        pass
    else:
        print(f'INFO: Added to {heading}')
    return ret


def gen_manifest():
    """Put your heading sources here...."""
    ret = []
    try:
        """Add your config code below!!! feel free to defin your own add
        functions / glue code. Just make sure that the gen_manifest function
        always returns a list of waypoint objects as defined in
        ./waypoint_def.py"""
        ## AN example
        ret.extend(add_ical(
            "http://www.nasa.gov/templateimages/redesign/calendar/iCal/nasa_calendar.ics",
            a_time=4, heading="SPACE"))

    except Exception as e:
        print(e)
        pass

    return ret
