##############################
#\                          /#
#\   Put the data here      /#
#\                          /#
##############################


import json

#\ load data from json file
with open("Index.json") as f:
    INDEX = json.load(f)
    # print(f'{"x"*25}\n| [INFO]The Index data |\n{"x"*25}\n{json.dumps(INDEX, indent=4)}')


#\ -- OSM API --
bAPIon = INDEX['OSM']['bAPIon']
GMAPapikey = INDEX['OSM']['GMAPapikey']

#\ -- Server url--
ServerURL = INDEX["Server"]


#\ -- Line Bot --
#\ Line Bot join group Text
JoinEventText = INDEX['LineBot']['JoinEventText']


#\ Login info
LoginEventText = INDEX['LineBot']['LoginEventText']


#\ retry for login
re_try_limit = INDEX["DragonflyData"]["re_try_limit"]


#\ URL
general_url = INDEX["DragonflyData"]["URL"]["general_url"]
Login_url = general_url + INDEX["DragonflyData"]["URL"]["Login_url"]
All_Observation_Data_url = general_url + INDEX["DragonflyData"]["URL"]["All_Observation_Data_url"]
Next_page_url = general_url + INDEX["DragonflyData"]["URL"]["Next_page_url"]
Brief_discriptions_url = INDEX["DragonflyData"]["URL"]["Brief_discriptions_url"]
Detailed_discriptions_url = INDEX["DragonflyData"]["URL"]["Detailed_discriptions_url"]
map_info_url = INDEX["DragonflyData"]["URL"]["map_info_url"]
species_all_record_data_first_url = INDEX["DragonflyData"]["URL"]["species_all_record_data_first_url"]
species_all_record_data_page_url = INDEX["DragonflyData"]["URL"]["species_all_record_data_page_url"]
species_all_record_data_species_url = INDEX["DragonflyData"]["URL"]["species_all_record_data_species_url"]
total_num_species_url = INDEX["DragonflyData"]["URL"]["total_num_species_url"]


#\ Alarm
HourFrom = INDEX["WakeUpAlarm"]["HourFrom"]
HourEnd = INDEX["WakeUpAlarm"]["HourEnd"]
HourRange = f"{HourFrom}-{HourEnd}"
IntervalPerHour = INDEX["WakeUpAlarm"]["IntervalPerHour"]
IntervalPerMin = INDEX["WakeUpAlarm"]["IntervalPerMin"]
HOUR = {"hour" : HourRange+"/"+IntervalPerHour} if IntervalPerHour != "" else {"minute" : "*/"+IntervalPerMin}

