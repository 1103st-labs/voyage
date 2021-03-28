"""This contains the primary classes for task management"""
import time
import voyage_enums as ve
from icalevents.icalevents import events
import re

DAY = 86400  # How many seconds in a day


class Waypoint():
    """Represents an atomic task to be done"""

    def __init__(self, des: "What needs to be done",
                 due: "time.time obj",
                 heading: "the heading object to which this belongs",
                 activation: "time obj, start to be concidered",
                 cost: "Time cost to do the task in min"
                 = 60,
                 state: "what state is this task"
                 = ve.Task_State.SLEEPING):
        """makes a wapoint...."""
        self.des = des
        self.due = due
        self.heading = heading
        self.activation = activation
        self.state = state
        self.cost = cost
        self.make_date = time.time()
        self.update_state()

    def update_state(self):
        """Figures out if the task has expired"""
        tmp = time.gmtime()
        if (tmp > time.gmtime(self.activation)):
            self.state = ve.Task_State.ACTIVE
        if (tmp > time.gmtime(self.due)):
            self.state = ve.Task_State.FAILED

    def cal_value(self):
        """Calculates the reward for the waypoint"""
        gold = int(self.cost * self.heading.cost)
        platinum = int(self.due - time.time())
        return (gold, platinum)


class Heading():
    """Represents a catagory of tasks linked by a comon vector"""

    def __init__(self, name: "the name of the heading",
                 des: "describes where this vecotr points",
                 mode: "what mode is this heading in",
                 mode_data: "Whatever the mode needs"
                 = None,
                 waypoints: "list of waypoints"
                 = [],
                 cost: "how much to scale waypoint values"
                 = 1):
        """makes a new heading..."""
        self.name = name
        self.des = des
        self.mode = mode
        self.mode_data = mode_data
        self.waypoints = waypoints
        self.cost = cost
        self.make_date = time.time()

    def sync(self):
        """useed the mode specified in self.mode to update the waypoints"""
        if (True): # NOTE TEMP HACK
            tmp_events = events(self.mode_data["URL"])
            for x in tmp_events:
                if (re.search(self.mode_data["Filter"], x.summary)):
                    des = x.summary
                    due = 0
                    cost = 0
                    activation = 0
                    # NOTE Shoul this be the compile command?
                    # I Have switched this off to male this work
                    # TODO switch this back on AND Make it work
                   # exec(self.mode_data["TimeRule"],
                   #      {"__builtins__": __builtins__,
                   #       "ve": ve, 
                   #       "cal_event": x,
                   #        "description": des,
                   #        "due": due,
                   #        "cost": cost,
                   #        "activation": activation})
                    cal_event = x
                    import voyage_enums as ve
                    l = locals()
                    exec(self.mode_data["TimeRule"], globals(), l)
                    # TODO Check return types
                    self.waypoints.append(Waypoint(l["des"], l["due"],
                                                   self, l["activation"],
                                                   l["cost"]))


class VMap():
    """Represents a per-user colection of headings"""

    manifest = None

    def __init__(self, headings: "the users headings"
                 = [],
                 gold: "the users gold"
                 = 0,
                 platinum: "the users platnum"
                 = 0,
                 user: "the user obj"
                 = None):
        self.headings = headings
        self.gold = gold
        self.platinum = platinum
        self.user = user

    def update_headings(self):
        """updatess all known waypoints"""
        for x in self.headings:
            x.sync()
            for xx in x.waypoints:
                xx.update_state()

    def get_mandatory(self):
        """returns all waypoints set to expire int the next 24 hours"""
        ret = {}
        for x in self.headings:
            for xx in x.waypoints:
                if ((xx.due - DAY) < (time.time())):
                    ret[xx.due] = xx
        # v cleans out the done tasks
        ret = {x: ret[x] for x in ret if ret[x].state != ve.Task_State.DONE}
        ret = [(i, ret[i]) for i in sorted(ret)]
        return ret

    def get_advised(self):
        """returns all waypoints that are active"""
        ret = {}
        for x in self.headings:
            for xx in x.waypoints:
                if (not ((xx.due - DAY) < (time.time()))
                    and ((time.time() + DAY) > (xx.activation))):
                    ret[xx.due] = xx
        ret = {x: ret[x] for x in ret if ret[x].state != ve.Task_State.DONE}
        ret = [(i, ret[i]) for i in sorted(ret)]
        return ret

    def update_manifest(self):
        """generates a the days manifest for the user"""
        self.update_headings()
        mandatory = self.get_mandatory()
        advised = self.get_advised()
        ret = {"Mandatory": {"Waypoints": mandatory,
                               "Reward": [x[1].cal_value() for x in
                                          mandatory]},
                "Advised": {"Waypoints": advised,
                               "Reward": [x[1].cal_value() for x in
                                          advised]}
              }
        self.manifest = ret

    def change_waypoint_state(self, waypoint: "the waypoint in the manifest",
                              state: "A state from voyage_enums"):
        """Changes the state of an item  and applies the nessary
        change in balance"""
        if ((state == ve.Task_State.DONE) and
            (waypoint.state is not ve.Task_State.FAILED)):
            value = waypoint.cal_value()
            self.gold += value[0]
            # if there are mandatory tasks left do not give plat.
            undone = [x for x
                      in self.manifest["Mandatory"]["Waypoints"]
                      if x[1].state != ve.Task_State.DONE]
            if (len(undone) == 0):
                self.platinum += value[1]
            waypoint.state = ve.Task_State.DONE
        elif (waypoint.state == ve.Task_State.DONE):
            value = waypoint.cal_value()
            self.gold -= value[0]
            undone = [x for x
                      in self.manifest["Mandatory"]["Waypoints"]
                      if x[1].state != ve.Task_State.DONE]
            if (len(undone) == 0):
                self.platinum -= value[1]
            waypoint.state = state
        else:
            waypoint.state = state


# Unit Test
if __name__ == "__main__":
    print("Unit Test!")
    m = VMap()
    print(f'Made VMap {m}')
    h = Heading("Test Heading", "The testing of this unit", None)
    print(f'Made Heading {h}')
    w = Waypoint("test unit!", time.time() + DAY, h, time.time())
    print(f'Made waypoint {w}')
