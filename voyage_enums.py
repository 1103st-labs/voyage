"""Contains all of the defined enums of the project"""
from enum import Enum

Intent = Enum("Intent", "DM")
# used to define what intent a message object was sent with

Task_State = Enum("Task_State", "ACTIVE", "SLEEPING", "DONE",
                  "FAILED", "LIMBO")
# used to define what state a waypoint is
