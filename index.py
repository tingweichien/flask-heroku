##############################
#\                          /#
#\   Put the data here      /#
#\                          /#
##############################
# ************************** #
#     Please replace         #
#    Private_Index.json      #
# ************************** #
import json

#\ load data from json file
with open("Index.json") as f:
    INDEX = json.load(f)
    # print(f'{"x"*25}\n| [INFO]The Index data |\n{"x"*25}\n{json.dumps(INDEX, indent=4)}')

#\ load the private data from json file
with open("Private_Index.json") as p_f:
    INDEX_PRIVATE = json.load(p_f)


#\ APP Private Key
APP_Pri_Key = INDEX_PRIVATE["APP_Pri_Key"]


#\ -- OSM API --
bAPIon = INDEX['OSM']['bAPIon']
GMAPapikey = INDEX_PRIVATE['OSM']['GMAPapikey']


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



#\ -- DataBase --
#\ Database info
host = INDEX_PRIVATE["DataBase"]["DataBaseInfo"]["host"]
Database = INDEX_PRIVATE["DataBase"]["DataBaseInfo"]["Database"]
User = INDEX_PRIVATE["DataBase"]["DataBaseInfo"]["User"]
Port = INDEX_PRIVATE["DataBase"]["DataBaseInfo"]["Port"]
Password = INDEX_PRIVATE["DataBase"]["DataBaseInfo"]["Password"]
URI = INDEX_PRIVATE["DataBase"]["DataBaseInfo"]["URI"]

#\ Database table name
UserInfoTableName = INDEX["DataBase"]["DataBaseTable"]["UserInfoTableName"]