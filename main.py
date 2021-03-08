"""The toplevel of the program and where the system starts. Other than being
the driver this code manages connections to endpoints and sanitizes input before
passing to the switchboard"""



# dis start code and event handlers

# handlesrs will convert to lower and then pass to switchboard with the
# folowing
# Switch_Board(M: message obj, T: text of message, I: Intent/What event did it
# come from. Enums for I can be found in kenums.py, U: the username)
