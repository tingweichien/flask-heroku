#\ put the variable or constant value here

from enum import IntEnum
# from flask import session
from flask_caching import Cache

# Instantiate the cache
cache = Cache()


#\ Line bot Event
class eLineBotEvent(IntEnum):
    NONE    = 0
    LOGIN   = 1
    MENU    = 2
    REQUEST = 3
    RECORD  = 4
    SETTING = 5
    SEARCH  = 6
    OTHERS  = 7
