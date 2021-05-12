##############################
#\                          /#
#\   Put the data here      /#
#\                          /#
##############################


import json

#\ load data from json file
with open("Index.json") as f:
    Index = json.load(f)
    print(f'{"x"*25}\nx [INFO]The Index data is x\n{"x"*25}\n{json.dumps(Index, indent=4)}')


#\ -- OSM API --
bAPIon = Index.OSM.bAPIon
GMAPapikey = Index.OSM.GMAPapikey


#\ -- Line Bot --
#\ Line Bot join group Text
JoinEventText = Index.LineBot.JoinEventText

#\ Login info
LoginEventText = Index.LineBot.LoginEventText
LoginData = dict()

