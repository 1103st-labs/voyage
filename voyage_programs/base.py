"""This is the beys e class for progams in  this system."""


class base():
    """All your base are belong to us"""
    def __init__(self, m: "the inital message object",
                 t: "The inital comand text",
                 i: "the inital intent",
                 user: "the user that this is asigned to"):
        """You should use this for prosessing the first part ot you comand.
        dont forget to call suuper before anything else to get everything set
        up!"""
        self.msg_q += m
        self.user = user
        self.intent = i

    def program():
        """This is where your program goesfert initiliaseation."""
        pass
