"""Used to find whose account to send the message and what program to run if
any"""

import voyage_enums
import time
import pickle
import voyage_programs


class User():
    """Used to represent the users account"""
    data = {}  # holds a users data...
    active_intents = {name: None for name, member in
                      voyage_enums.Intents._members_.items()}
    # ^ mount points for programs

    def __init__(self, username: "the username of the account allocated"):
        """makes the user...."""
        self.data["user"] = username


class Switch_Board():
    """The switchboard proper, there should be one of these per system. The
    primary account manager and save state manager."""
    users = {}  # of the form {"username with tag": user-account}
    programs = voyage_programs.__dict__
    schedule = {}  # of the from {time.time() obj: func}

    def run_program(self, m: "The dis mesg obj",
                    t: "sanitized text message",
                    i: "The intent of the msg, see enum",
                    u: "the users username from the message"):
        """Runns through the array of users and checks to see if they have a
        program running in the stated intent. if they do the message is passed
        to it, otherwise the program is started and added to there account at
        that intent"""
        if (u in self.users):  # if they have an account
            if (self.users[u].active_intents[i] is not None):
                # if they have an active program at intent
                self.users[u].active_intents[i].msg_q.append(m)
                next(self.users[u].active_intents[i].program)
            else:  # start a new program
                tmp_program = t.split(' ')[0]
                if (tmp_program in self.program.keys()):
                    self.users[u].active_intents[i] = \
                            self.programs[tmp_program](m, t, i, self.users[u])
                else:
                    # TODO send back error about not a program
                    pass

        else:  # add new user
            self.adduser(u)
            self.run_program(self, m, t, i, u)  # TODO add recursion depth ck

    def add_user(self, u: "the string name of the user"):
        """adds a user to the known accounts"""
        # TODO send back help text
        self.users.append(User(u))

    def save_state(self, name: "optional path to save to" = self.save_name):
        """saves the state of the Switch_Board obj as a pickle"""
        with open(name, "wb+") as f:
            pickle.dump(self, f)

    def backup(self):
        """Creates a unique backup of the current state"""
        self.save_state(self.name + "_backup_" +
                        time.asctime(time.gmtime()).replace(" ", "_"))

    def schedule_funct(self, func: "the function to schedule",
                       time: "the time.time object to use"
                       = None,
                       delta: "how many minutes into the future"
                       = None):
        """Adds a funtion to be called at time+delta minutes into the future or
        at time"""
        # TODO add seched funct and handeler in main
        pass
