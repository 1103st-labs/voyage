"""This is the beys e class for progams in  this system."""
import queue
import asyncio
import time


class base():
    """All your base are belong to us"""
    def __init__(self, m: "the inital message object",
                 t: "The inital comand text",
                 i: "the inital intent",
                 user: "the user that this is asigned to"):
        """You should use this for prosessing the first part ot you comand.
        dont forget to call suuper before anything else to get everything set
        up!"""
        self.msg_q = queue.SimpleQueue()
        self.msg_q += m
        self.intent = i
        self.sleep_time = 10
        self.cron_time = 0 # Time in secods, 0 to disable
        self.last_time = time.time()
        self.setup(m)
        self.msg_q.get()
        while (True):
            if ((self.last_time + self.cron_time) < time.time()):
                self.cron()
            if (self.msg_q.empty):
                await asyncio.sleep(SLEEP_TIME)
            else:
                program(self.msg_q.get())

    def program(m: "dis message obj"):
        """This is where your program goesfert initiliaseation."""
        pass


    def setup(m: "dis obj"):
        """Allows for any first run code and to set program env stuff"""
        pass

    def cron(m: "dis obj"):
        """If you set schedule_time to a value this code will be run at that
        ibtervall regardless of que state"""
        pass
