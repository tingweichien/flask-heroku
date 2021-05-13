##############################
#\                          /#
#\   Put the data here      /#
#\                          /#
##############################


import json

#\ load data from json file
with open("Index.json") as f:
    INDEX = json.load(f)
    print(f'{"x"*25}\n| [INFO]The Index data |\n{"x"*25}\n{json.dumps(INDEX, indent=4)}')


#\ -- OSM API --
bAPIon = INDEX['OSM']['bAPIon']
GMAPapikey = INDEX['OSM']['GMAPapikey']


#\ -- Line Bot --
#\ Line Bot join group Text
JoinEventText = INDEX['LineBot']['JoinEventText']

#\ Login info
LoginEventText = INDEX['LineBot']['LoginEventText']
LoginData = dict()

