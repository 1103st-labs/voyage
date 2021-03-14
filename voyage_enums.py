"""Contains all of the defined enums of the project"""
from enum import Enum, auto


class Default_Mode_Data(Enum):
    ICAL = {"URL": "www.nasa.gov/templateimages/redesign/calendar/iCal/nasa_calendar.ics",
            "Filter": ".*",
            "TimeRule": "due = call_event.end.timestamp(); cost = (call_event.end.timestamp() - call_event.start.timestamp()); activation = (due - 86400);"
           }


class Intent(Enum):
    """used to define what intent a message object was sent with"""
    HEADING_VIEW = auto()
    MANIFEST = auto()


class Update_Mode(Enum):
    """ used to define what update mode to use"""
    ICAL = auto()


class Task_State(Enum):
    """ used to define what state a waypoint is"""
    ACTIVE = auto()
    SLEEPING = auto()
    DONE = auto()
    FAILED = auto()
    LIMBO = auto()
