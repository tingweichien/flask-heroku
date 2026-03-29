from typing import List
import proxyscrape
import requests
from bs4 import BeautifulSoup
import DataClass
import index
from fake_useragent import UserAgent, FakeUserAgentError
import re
from datetime import datetime
from opencc import OpenCC
import time
import random
import logging

# Make sure there is no simple chinese, if so, change to tradition chinese
Word_S2Tcc = OpenCC('s2t')

# 產生擬真的瀏覽器 Header，增加隱匿性
def get_realistic_headers():
    try:
        UA = UserAgent()
        user_agent = UA.random
    except FakeUserAgentError:
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    
    return {
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Referer': index.general_url, # 偽裝是從主網頁點擊過來的
        'Upgrade-Insecure-Requests': '1'
    }

def get_proxy()->list:
    collector = proxyscrape.create_collector('default', 'https')
    proxy = collector.get_proxy({'country': 'united states'})
    print(f"proxy: {proxy}")
    return proxy

def Login_Web(Input_account:str, Input_password:str)->list:
    session = requests.Session()
    data = {
        'account' : Input_account,
        'password' : Input_password,
    }
    headers = get_realistic_headers()
    re_try = 0

    while re_try < index.re_try_limit:
        try:
            # 模擬人類打開登入頁面
            loginStatus = requests.get(index.Login_url, headers=headers, timeout=10)
            time.sleep(random.uniform(1.0, 2.5)) # 停留一下再送出表單
            
            Login_type = "No proxy"
            print(f"[info] login type: {Login_type}, login status: {loginStatus}")
        except:
            re_try += 1
            print(f"[info] retry: {re_try}")
        else:
            Login_Response = session.post(index.Login_url, headers=headers, data=data, timeout=10)
            soup_login_ckeck = BeautifulSoup(Login_Response.text, 'html.parser')
            script = soup_login_ckeck.find("script") 
            try :
                alert = re.findall(r'(?<=alert\(\").+(?=\")', script.contents[0])
            except :
                alert = ""

            if (len(alert) > 0):
                Login_state = False 
            else:
                Login_state = True
            return [session, Login_Response, Login_state]

    print("[waning] Login failed")
    return [None, None, None]

def DataCrawler(session, Input_ID:int=None, InputMaxID:int=None, filter_object:DataClass.FilterObject=None)->list:
    overflow = False
    headers = get_realistic_headers()
    
    if InputMaxID == None:
        Max_ID_Num = GetMaxID(session)
    else:
        Max_ID_Num = InputMaxID

    if Input_ID == None :
        Input_ID = Max_ID_Num

    if (Input_ID != None) and (Input_ID > Max_ID_Num) or (Input_ID < 0):
        overflow = True
        ID_find_result = []
    else:
        try:
            # 抓取詳細資料
            response_Detailed_discriptions2 = session.post(index.general_url + index.Detailed_discriptions_url + str(Input_ID), headers=headers, timeout=15)
            soup2 = BeautifulSoup(response_Detailed_discriptions2.text, 'html.parser')
            
            if soup2.find(id='R_MEMO') and soup2.find(id='R_MEMO').text != None and len(soup2.find(id='R_MEMO').text.replace(" ", "")) != 0:
                Description = soup2.find(id='R_MEMO').text.replace(" ", "").replace("\n", "").replace("\t", "")
            else:
                Description = "None"

            # 模擬人類切換頁面，加入隨機延遲
            time.sleep(random.uniform(1.5, 3.5))

            # 抓取簡述資料
            response_Brief_discriptions = session.post(index.general_url + index.Brief_discriptions_url + str(Input_ID), headers=headers, timeout=15)
            response_Brief_discriptions_text = BeautifulSoup(response_Brief_discriptions.text, 'html.parser')
            Max_All_Observation_Data_response_Data = response_Brief_discriptions_text.find_all('td')

        except Exception as e:
            logging.warning(f"[DragonflyData Error] Connection error for ID {Input_ID}: {e}. Skipping this ID.")
            empty_result = DataClass.DetailedTableInfo(str(Input_ID), "1970-01-01", "00:00", "None", "None", "None", "None", "None", "None", "None", "", "", [], "Connection Error", "", "None")
            return [empty_result, overflow, int(Max_ID_Num)]

        SpeciesList = []
        City = "None"
        District = "None"
        for idx in range(len(Max_All_Observation_Data_response_Data)):
            if Max_All_Observation_Data_response_Data[idx].text == index.dragonfly_simple_info_species_col_name:
                SpeciesList = Max_All_Observation_Data_response_Data[idx+1].text.split(' ')
                SpeciesList = list(filter(None, SpeciesList))
            if Max_All_Observation_Data_response_Data[idx].text == index.dragonfly_simple_info_city_col_name:
                CityDistrict = Max_All_Observation_Data_response_Data[idx+1].text.split(' - ')[0]
                City = CityDistrict[:3]
                District = CityDistrict[3:]

        if filter_object != None:
            rarity = CheckSpeciesRarityRates(SpeciesList, filter_object.SpeciesFilter)
        else:
            rarity = "None"

        date_val = soup2.find(id='日期').get('value') if soup2.find(id='日期') else "1970-01-01"
        time_val = soup2.find(id='時間').get('value') if soup2.find(id='時間') else "00:00"
        place_val = Word_S2Tcc.convert(soup2.find(id='地點').get('value')) if soup2.find(id='地點') else "None"
        elevation_val = soup2.find(id='R_ELEVATION').get('value') if soup2.find(id='R_ELEVATION') else "0"
        recorder_val = soup2.find(id='紀錄者').get('value') if soup2.find(id='紀錄者') else "None"
        lat_val = soup2.find(id='R_LAT').get('value') if soup2.find(id='R_LAT') else "none"
        lng_val = soup2.find(id='R_LNG').get('value') if soup2.find(id='R_LNG') else "none"

        ID_find_result = DataClass.DetailedTableInfo(str(Input_ID), date_val, time_val, City, District, place_val, elevation_val, recorder_val, lat_val, lng_val, "", "", SpeciesList, Word_S2Tcc.convert(Description), "", rarity)

        if filter_object != None:
            [Status, Species_intersection] = filter_object.DataFilter(ID_find_result)
            if Status:
                ID_find_result.FilteredSpeciesList = Species_intersection

    return [ID_find_result, overflow, int(Max_ID_Num)]

def GetMaxID(session)->int:
    headers = get_realistic_headers()
    All_Observation_Data_response = session.post(index.All_Observation_Data_url, headers=headers, timeout=15)
    soup_ID_check = BeautifulSoup(All_Observation_Data_response.text, 'html.parser')
    All_Observation_Data_response_Data_Set = soup_ID_check.find(id='theRow')
    Max_All_Observation_Data_response_Data = All_Observation_Data_response_Data_Set.find_all('td')
    return int(Max_All_Observation_Data_response_Data[0].text)

def CrawDataByDate(session, start_time:datetime, end_time:datetime, filter_object:DataClass.FilterObject):
    condition = True
    initID = None
    counter = 0
    result_list = []
    Max_ID_Num = None
    while condition:
        [ID_find_result, overflow, Max_ID_Num] = DataCrawler(session, initID, Max_ID_Num, filter_object)
        print(f"ID: {initID}")

        if overflow:
            print("[Warning] In the CrawDataByDate() ID overflow")
            return

        if CheckIDDate(start_time, end_time, datetime.strptime(ID_find_result.Dates, "%Y-%m-%d")):
            counter += 1
            initID = Max_ID_Num - counter
            result_list.append([ID_find_result])
        else:
            condition = False
            
        time.sleep(random.uniform(2.0, 4.5))

    return result_list

def CheckIDDate(start_time:datetime, end_time:datetime, check_time:datetime)->bool:
    if start_time <= check_time <= end_time:
        return True
    else:
        return False

def CheckSpeciesRarityRates(Species_intersection:list, species_filter:list)->str:
    rarity = -1
    if Species_intersection != None and species_filter != None:
        for species in Species_intersection:
            if species in species_filter:
                rarity = max([species_filter.index(species)])

        if rarity >= species_filter.index(index.StartOfSR_Species) :
            return "SR" 
        elif rarity >= species_filter.index(index.StartOfR_Species) :
            return "R" 
        elif rarity > 0:
            return "N" 
        else:
            return "None"
    else:
        return "None"

def CrawlDataByIDRange(session, Start_ID:int=None, End_ID:int=None, filter_object:DataClass.FilterObject=None)->List[DataClass.DetailedTableInfo]:
    Max_ID_Num = None
    counter = 0
    condition = True
    result_list = []
    SetEndID2Latest = False

    if Start_ID == None or filter_object == None:
        print("[Warning] In CrawlDataByIDRange() the Start_ID is None or filter_object is None")
        return None

    if End_ID == None:
        SetEndID2Latest = True
    else:
        if Start_ID > End_ID:
            print("[Warning] In CrawlDataByIDRange() the Start_ID > End_ID")
            return None

    while condition:
        [ID_find_result, overflow, Max_ID_Num] = DataCrawler(session, End_ID, Max_ID_Num, filter_object)

        if overflow:
            print("[Warning] In the CrawlDataByIDRange() ID overflow")
            return None

        if ID_find_result.Dates != "1970-01-01":
            if len(ID_find_result.FilteredSpeciesList) != 0:
                result_list.append(ID_find_result)

        if SetEndID2Latest == True:
            counter += 1
            End_ID = Max_ID_Num - counter
        else:
            End_ID -= 1

        if End_ID < Start_ID:
            condition = False
            
        # 爬完一筆資料後，隨機休息 1.5 ~ 4 秒，模擬人類看資料
        if condition:
            time.sleep(random.uniform(1.5, 4.0))

    print(f"[INFO] In CrawlDataByIDRange() the result list is {result_list}")
    return result_list

def CrawTodayData(session, TodayFirstID:int, filter_object:DataClass.FilterObject):
    return CrawlDataByIDRange(session, TodayFirstID, None, filter_object)

def GetSpeciesRecordingNumberRank(session)->list:
    headers = get_realistic_headers()
    species_number_rank_response = session.post(index.species_number_rank_url, headers=headers, timeout=15)
    soup_number_species_check = BeautifulSoup(species_number_rank_response.text, 'html.parser')
    Data_td_tag = soup_number_species_check.find_all('td')

    Species_rank_dict = dict()
    Species_rank_list_only_name = []
    for i in range(2, len(Data_td_tag), 4):
        td = Data_td_tag[i:i+3]
        Species_rank_dict[td[0].text] = td[1].text
        Species_rank_list_only_name.append(td[0].text)

    return [Species_rank_dict, Species_rank_list_only_name]