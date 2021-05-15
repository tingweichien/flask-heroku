#\ put the variable or constant value here

from enum import IntEnum


#\ Login info
gLoginData = {"Account":"",
            "Password":""}


#\ Line bot Event
class eLineBotEvent(IntEnum):
    LOGIN   = 1
    MENU    = 2




#\ global event
gEventText = ""
gEvent = None
gEventCnt = 0
#\ message text
gIsJustText = True
gLoginDataConfirm = False