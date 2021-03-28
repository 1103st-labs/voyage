"""Used to find whose account to send the message and what program to run if
any"""

import voyage_enums
import time
import pickle
import voyage_programs.h_manager as h
import voyage_programs.m_manager as m
import voyage_core as vc
import voyage_enums as ve


class User():
    """Used to represent the users account"""
    data = {}  # holds a users data...
    active_intents = {member: None for name, member in
                      voyage_enums.Intent.__members__.items()}
    # ^ mount points for programs

    def __init__(self, username: "the username of the account allocated"):
        """makes the user...."""
        self.data["USER"] = username
        self.data["VMAP"] = vc.VMap(user=self)


class Switch_Board():
    """The switchboard proper, there should be one of these per system. The
    primary account manager and save state manager."""
    users = {}
    programs = {"h": h.h_manager, "m": m.make_manifest}
    schedule = {}  # of the from {time.time() obj: func}
    e_count = 0

    def __init__(self, name):
        """sets the name for the switchboard"""
        self.name = name

    async def run_program(self, m: "The dis mesg obj",
                    t: "sanitized text message",
                    i: "The intent of the msg, see enum",
                    u: "the users username from the message"):
        """Runs through the array of users and checks to see if they have a
        program running in the stated intent. If they do the message is passed
        to it, otherwise the program is started and added to there account at
        that intent"""
        if (u in self.users):  # if they have an account
            if (self.users[u].active_intents[i] is not None):
                # if they have an active program at intent
                self.users[u].active_intents[i].msg_q.put(m)
            else:  # start a new program
                tmp_program = t[0]
                if (tmp_program in self.programs.keys()):
                    self.users[u].active_intents[i] = \
                            self.programs[tmp_program](m, t, i, self.users[u])
                    await self.users[u].active_intents[i].main_loop(m)
                else:
                    # NOTE THIS IS A HACK THAT SHOULD BE FIXED
                    raise ve.NoSaveErr("Not a valid program.")
                    pass

        else:  # add new user
            self.add_user(u)
            await self.run_program(m, t, i, u)  # TODO add recursion depth ck

    def add_user(self, u: "the string name of the user"):
        """adds a user to the known accounts"""
        # TODO send back help text
        self.users[u] = (User(u))

    def save_state(self, name: "optional path to save to" = None):
        """saves the state of the Switch_Board obj as a pickle"""
        name = name if (name is not None) else self.name
        with open(name, "wb+") as f:
            pickle.dump(self, f)

    def backup(self):
        """Creates a unique backup of the current state"""
        self.save_state(self.name + "_backup_" +
                        time.asctime(time.gmtime()).replace(" ", "_"))

