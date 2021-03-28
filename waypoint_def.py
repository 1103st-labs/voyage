import hashlib
import datetime
from backports import zoneinfo


class Waypoint():
    """Represents an atomic todo"""
    def __init__(self,
                 des: "string description"
                 = "Default Des",
                 due: "A date time obj"
                 = datetime.datetime.now(datetime.timezone.utc),
                 dur: "int minute duration of the event"
                 = 0,
                 cost: "int energy cost of the event"
                 = 0,
                 plat: "int plat of the event"
                 = 0,
                 a_time: "int days before due that todo become active"
                 = 0,
                 heading: "string heading name"
                 = "Default"):
        self.des = des
        self.due = due
        self.dur = dur
        self.cost = cost
        self.plat = plat
        self.a_time = a_time
        self.heading = heading
        self.hash = self.gen_hash()

    def gen_hash(self):
        """Generates a Waypoint id"""
        vals = f'{self.des}{self.due}{self.heading}'
        vals = hashlib.sha1(vals.encode("utf-8"))
        return vals.hexdigest()

    def gen_sum(self):
        """generates a summary of the smaller details"""
        ret = ""
        tmp_day = f'{self.due.day}.{self.due.month}'
        tmp_time = f'{self.due.hour}:{self.due.minute}'
        ret += f'［ 🗓 {tmp_day}    ⏱  {tmp_time} ］\n'
        ret += f'［ ⛀ {self.cost}    ⛂ {self.plat} ］\n'
        ret += f'［ ⎆ {self.a_time}    ∆ {self.dur} ］\n'
        ret += self.hash
        if (len(ret) < 5):
            breakpoint()
        return ret
