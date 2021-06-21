##############################
#\                          /#
#\   Put the data here      /#
#\                          /#
##############################
# ************************** #
#                            #
#  Please replace data in    #
#    Private_Index.json      #
#                            #
# ************************** #

import json



#\ Load data from json file
with open("./Setting/Index.json", encoding="utf-8") as f:
    INDEX = json.load(f)
    # print(f'{"x"*25}\n| [INFO]The Index data |\n{"x"*25}\n{json.dumps(INDEX, indent=4)}')

#\ Load the private data from json file
with open("./Setting/Private_Index.json") as p_f:
    INDEX_PRIVATE = json.load(p_f)

#\ Load Species directory
with open("./Setting/SpeciesDirectory.json", encoding="utf-8") as SD_f:
    INDEX_SPECIES = json.load(SD_f)



#\ ---- Flask ----
#\ APP Private Key
APP_Pri_Key = INDEX_PRIVATE["APP_Pri_Key"]



#\ ---- OSM API ----
bAPIon = INDEX["OSM"]["bAPIon"]
GMAPapikey = INDEX_PRIVATE["OSM"]["GMAPapikey"]

#\ limit the map marker amount
MapMarksLimit = INDEX["OSM"]["MapMarksLimit"]

#\ default map view location
DefaultMapViewLocation = INDEX["OSM"]["DefaultMapViewLocation"]

#\ accuracy for the latitude and longitude
LatLonAccuracy = 10**INDEX["OSM"]["LatLonAccuracy"]


#\ ---- Google sheet API ----
GSheetApiKeyPath = INDEX["GCP"]["GSheetApiKeyPath"]



#\ -- Server url--
ServerURL = INDEX["Server"]



#\ ---- Line Bot ----
#\ Line Bot join group Text
JoinEventText = INDEX["LineBot"]["EventText"]["JoinEventText"]

#\ Login info
LoginEventText = INDEX["LineBot"]["EventText"]["LoginEventText"]

#\ Rich menu image path
LoginRichMenuImgPath = INDEX["LineBot"]["RichMenu"]["MenuImgPath"]["LoginRichMenuImgPath"]
MainRichMenuImgPath = INDEX["LineBot"]["RichMenu"]["MenuImgPath"]["MainRichMenuImgPath"]
Main2RichMenuImgPath = INDEX["LineBot"]["RichMenu"]["MenuImgPath"]["Main2RichMenuImgPath"]

#\ Carsoul Bubble Limit number due to line bot api limitation
CarsoulBubbleLimit = INDEX["LineBot"]["CarsoulBubbleLimit"]


#\ ---- Dragonfly ----
#\ Retry for login
re_try_limit = INDEX["DragonflyData"]["re_try_limit"]

#\ URL
general_url = INDEX["DragonflyData"]["URL"]["general_url"]
Login_url = general_url + INDEX["DragonflyData"]["URL"]["Login_url"]
All_Observation_Data_url = general_url + INDEX["DragonflyData"]["URL"]["All_Observation_Data_url"]
Next_page_url = INDEX["DragonflyData"]["URL"]["Next_page_url"]
Brief_discriptions_url = INDEX["DragonflyData"]["URL"]["Brief_discriptions_url"]
Detailed_discriptions_url = INDEX["DragonflyData"]["URL"]["Detailed_discriptions_url"]
map_info_url = INDEX["DragonflyData"]["URL"]["map_info_url"]
species_all_record_data_first_url = INDEX["DragonflyData"]["URL"]["species_all_record_data_first_url"]
species_all_record_data_page_url = INDEX["DragonflyData"]["URL"]["species_all_record_data_page_url"]
species_all_record_data_species_url = INDEX["DragonflyData"]["URL"]["species_all_record_data_species_url"]
total_num_species_url = INDEX["DragonflyData"]["URL"]["total_num_species_url"]

#\ Dragonfly simple info species column name
dragonfly_simple_info_species_col_name = INDEX["DragonflyData"]["Simple_info_table"]["dragonfly_simple_info_species_col_name"]
dragonfly_simple_info_city_col_name = INDEX["DragonflyData"]["Simple_info_table"]["dragonfly_simple_info_city_col_name"]
# print(dragonfly_simple_info_species_col_name)


#\ LAT LNG precision
PositionPrecision = INDEX["DragonflyData"]["PositionPrecision"]


#\ ---- DataBase ----
#\ Database info
host = INDEX_PRIVATE["DataBase"]["DataBaseInfo"]["host"]
Database = INDEX_PRIVATE["DataBase"]["DataBaseInfo"]["Database"]
User = INDEX_PRIVATE["DataBase"]["DataBaseInfo"]["User"]
Port = INDEX_PRIVATE["DataBase"]["DataBaseInfo"]["Port"]
Password = INDEX_PRIVATE["DataBase"]["DataBaseInfo"]["Password"]
URI = INDEX_PRIVATE["DataBase"]["DataBaseInfo"]["URI"]

#\ Database table name
UserInfoTableName = INDEX["DataBase"]["DataBaseTable"]["UserInfoTable"]["TableName"]
VariableTableName = INDEX["DataBase"]["DataBaseTable"]["VariableTable"]["TableName"]
VarLatestDataID = INDEX["DataBase"]["DataBaseTable"]["VariableTable"]["TableVar"]["LatestDataID"]



#\ Filter object [User_filter, Species_filter, KeepOrFilter]
DefaultFilterObject = [None, None, None]

#\ Alarm (This is for wake the free dyno Heroku up)
HourFrom = INDEX["Alarm"]["WakeUpAlarm"]["HourFrom"]
HourEnd = INDEX["Alarm"]["WakeUpAlarm"]["HourEnd"]
HourRange = f"{HourFrom}-{HourEnd}"
IntervalPerHour = INDEX["Alarm"]["WakeUpAlarm"]["IntervalPerHour"]
IntervalPerMin = INDEX["Alarm"]["WakeUpAlarm"]["IntervalPerMin"]
HOURAlarm = {"hour" : HourRange+"/"+IntervalPerHour} if IntervalPerHour != "" else {"minute" : "*/"+IntervalPerMin}

#\ Daily routine
DAYAlarm = {"hour": INDEX["Alarm"]["DailyUpdate"]["Hour"], "minute": INDEX["Alarm"]["DailyUpdate"]["Minute"], "second": INDEX["Alarm"]["DailyUpdate"]["Second"]}




#\ --Species directory--
# Dragonfly_Orders




#\ --Google sheet api--
#\ General google sheet url
GeneralgSheetUrl = lambda SpeciesID: INDEX["GoogleSheet"]["GeneralgSheetUrl_head"] + str(SpeciesID) + INDEX["GoogleSheet"]["GeneralgSheetUrl_end"]
