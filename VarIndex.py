#\ put the variable or constant value here

from enum import IntEnum


#\ Login info
LoginData = {"Account":"",
            "Password":""}


#\ Line bot Event
class eLineBotEvent(IntEnum):
    LOGIN   = 1
    MENU    = 2
