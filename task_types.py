"""This contains the primary classes for task management"""
import time
import ..voyage_enums as ve

DAY = 86400 # How many seconds in a day

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
        if (tmp > time.gmtime(due)):
            self.state = ve.Task_State.FAILED

    def cal_value():
        """Calculates the reward for the waypoint"""
        gold = int(self.cost * self.heading.cost)
        platinum = int(self.due - time.time())
        return (gold, platinum)


class Heading():
    """Represents a catagory of tasks linked by a comon vector"""

    def __init__(self, name: "the name of the heading",
                 des: "describes where this vecotr points",
                 mode: "what mode is this heading in",
                 waypoints: "list of waypoints"
                 = [],
                 cost: "how much to scale waypoint values"
                 = 1):
        """makes a new heading..."""
        self.name = name
        self.des = des
        self.mode = mode
        self.waypoints = waypoints
        self.cost = cost
        self.make_date = time.time()

    def sync(self):
        """useed the mode specified in self.mode to update the waypoints"""
        # TODO diffrent syncs
        pass

class VMap():
    """Represents a per-user colection of headings"""
    manifest = None
    def __init__(self, headings: "the users headings",
                 gold: "the users gold",
                 platinum: "the users platnum",
                 user: "the user obj"):
        self.headings = headings
        self.gold = gold
        self.platinum = platinum
        self.user = user

    def update_headings(self):
        """updatess all known waypoints"""
        for x in self.headings:
            x.sync()
            for xx in x.Waypoint:
                xx.update_state()

    def get_mandatory(self):
        """returns all waypoints set to expire int the next 24 hours"""
        ret = {}
        for x in self.headings:
            for xx in x.waypoints:
                if ((xx.due - DAY ) < (time.time())):
                    ret[xx.due] = xx
        ret = [(i,ret[i]) for i in sorted(ret)]
        return ret

    def get_advised(self):
        """returns all waypoints that are active"""
        ret = {}
        for x in self.headings:
            for xx in x.waypoints:
                if (not ((xx.due - DAY) < (time.time()))
                    and ((time.time + DAY) > (xx.activation))):
                    ret[xx.due] = xx
        ret = [(i,ret[i]) for i in sorted(ret)]
        return ret

    def update_manifest(self):
        """generates a the days manifest for the user"""
        self.update_headings()
        mandatory = self.get_mandatory()
        advised = self.get_advised()
        ret = { "Mandatory": { "Waypoints": mandatory,
                               "Reward": [x[1].cal_value() for i in
                                          mandatory]},
                "Advised": { "Waypoints": advised,
                               "Reward": [x[1].cal_value() for i in
                                          advised]}
              }
        self.manifest = ret


    def change_waypoint_state(self, waypoint: "the waypoint in the manifest",
                              state: "A state from voyage_enums"):
        """Changes the state of an item  and applies the nessary
        change in balance"""
        if ((state == ve.Task_State.DONE)
            and (waypoint.state is not ve.Task_State.FAILED)):
            value = waypoint.cal_value()
            self.gold += value[0]
            self.platinum += value[1]
            waypoint.state = ve.Task_State.DONE
        elif (waypoint.state == ve.Task_State.DONE):
            value = waypoint.cal_value()
            self.gold -= value[0]
            self.platinum -= value[1]
            waypoint.state = state
        else:
            waypoint.state = state

