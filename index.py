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


#\ -- Line Bot --
#\ Line Bot join group Text
JoinEventText = INDEX['LineBot']['JoinEventText']


#\ Login info
LoginEventText = INDEX['LineBot']['LoginEventText']


#\ retry for login
re_try_limit = INDEX["DragonflyData"]["re_try_limit"]


#\ URL
general_url = INDEX["DragonflyData"]["general_url"]
Login_url = INDEX["DragonflyData"]["Login_url"]
All_Observation_Data_url = INDEX["DragonflyData"]["All_Observation_Data_url"]
Next_page_url = INDEX["DragonflyData"]["Next_page_url"]
Brief_discriptions_url = INDEX["DragonflyData"]["Brief_discriptions_url"]
Detailed_discriptions_url = INDEX["DragonflyData"]["Detailed_discriptions_url"]
map_info_url = INDEX["DragonflyData"]["map_info_url"]
species_all_record_data_first_url = INDEX["DragonflyData"]["species_all_record_data_first_url"]
species_all_record_data_page_url = INDEX["DragonflyData"]["species_all_record_data_page_url"]
species_all_record_data_species_url = INDEX["DragonflyData"]["species_all_record_data_species_url"]
total_num_species_url = INDEX["DragonflyData"]["total_num_species_url"]