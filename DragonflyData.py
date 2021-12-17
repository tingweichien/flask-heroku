from typing import List
import proxyscrape
import requests
from bs4 import BeautifulSoup
import DataClass
import index
from fake_useragent import UserAgent, FakeUserAgentError
import re
from datetime import datetime




#\--->Now use random fake user agent
# https://ithelp.ithome.com.tw/articles/10209356
#\ if there is error orrcur then do not use this
try:
    UA = UserAgent()
    headers = {
            'User-Agent' : UA.random,
    }
except FakeUserAgentError:
    headers = {}


#\ Proxy auto crawling
#\ by proxyscrape 0.3.0
#\ https://pypi.org/project/proxyscrape/
def get_proxy()->list:
    collector = proxyscrape.create_collector('default', 'https')  # Create a collector for http resources
    proxy = collector.get_proxy({'country': 'united states'})  # Retrieve a united states proxy
    print(f"proxy: {proxy}")
    return proxy



#\ Login
def Login_Web(Input_account:str, Input_password:str)->list:
    """
    params:
        account,
        password
    return:
        session,
        Login_Response,
        Login_state
    """

    #\ seesion
    session = requests.Session()

    #\ Login account and password
    data = {
        'account' : Input_account,
        'password' : Input_password,
    }

    re_try = 0
    #\ retry for certain times if failed
    while re_try < index.re_try_limit:
        try:
            #\ auto get the proxy
            # try:
            #     list_len = len(index.proxy_list)
            #     loginStatus = requests.get(index.Login_url, proxies=index.proxy_list[re_try % list_len])
            #     Login_type = "proxy"
            # except:
            loginStatus = requests.get(index.Login_url)
            Login_type = "No proxy"

            print(f"[info] login type: {Login_type}, login status: {loginStatus}")


        except:
            #\ print the retry
            re_try += 1
            print(f"[info] retry: {re_try}")


        else:
            #\ 執行登入
            Login_Response = session.post(index.Login_url, headers=headers, data=data)

            #\ 確認是否成功登入
            # print(f"[INFO] Login response text : \n {Login_Response.text}")
            soup_login_ckeck = BeautifulSoup(Login_Response.text, 'html.parser')
            script = soup_login_ckeck.find("script") # find the alert
            try :
                alert = re.findall(r'(?<=alert\(\").+(?=\")', script.contents[0]) #\r\n    alert("登入失敗，請重新登入");\r\n

            except :
                alert = ""

            if (len(alert) > 0):
                Login_state = False # to show the error that the password or account might be wrong
            else:
                Login_state = True
            return [session, Login_Response, Login_state]

    #\ retry failed
    print("[waning] Login failed")
    return [None, None, None]


###################################################################
def DataCrawler(session, Input_ID:int=None, InputMaxID:int=None, Species_filter:list=[])->list:
    """
    params:
        session : from the return object of the requests.Session()
        Input_ID : The ID you want to crawl, if not then it will auto set to the latest ID number
        InputMaxID : This is to avoid redundent of request to get the MaxID again when calling this function in the loop.
    """


    #\ 執行進入"蜓種觀察資料查詢作業"
    # All_Observation_Data_response = session.post(index.All_Observation_Data_url, headers=headers)


    #\ 下一頁
    #\ http://dragonfly.idv.tw/dragonfly/rec_list_view.php?pageNum_rs_dragonfly_record=3
    '''
    page = 1
    response_next_page = session.post(All_Observation_Data_url + Next_page_url + str(page), headers=headers)
    #print(response_next_page.text)
    '''


    #\ 執行點入簡述
    # request url = http://dragonfly.idv.tw/dragonfly/view_data.php?id=65431
    # id = 65431
    # response_Brief_discriptions = session.post(index.general_url + index.Brief_discriptions_url + str(Input_ID), headers=headers)
    # response_Brief_discriptions_text = BeautifulSoup(response_Brief_discriptions.text, 'html.parser')
    # Max_All_Observation_Data_response_Data = response_Brief_discriptions_text.find_all('td')

    """print the colume in sequence
    for i in range(len(Max_All_Observation_Data_response_Data)):
        print(f"({i})\t"+Max_All_Observation_Data_response_Data[i].text)
    """
    # for idx in range(len(Max_All_Observation_Data_response_Data)):
    #     #\ Find the Species list
    #     if Max_All_Observation_Data_response_Data[idx].text == index.dragonfly_simple_info_species_col_name:
    #         SpeciesList = Max_All_Observation_Data_response_Data[idx+1].text.split(' ')
    #         SpeciesList = list(filter(None, SpeciesList))#\ filter out the empty list
    #         # print(f"[INFO] Species for ID : {Input_ID} -> {SpeciesList}")

    #     #\ Find the city and district
    #     if Max_All_Observation_Data_response_Data[idx].text == index.dragonfly_simple_info_city_col_name:
    #         CityDistrict = Max_All_Observation_Data_response_Data[idx+1].text.split(' - ')[0]
    #         City = CityDistrict[:3]
    #         District = CityDistrict[3:]
    #         # print(f"[INFO] City for ID : {Input_ID} -> {City}\n[INFO] District for ID : {Input_ID} -> {District}")





    #\ 執行詳述
    # request url = http://dragonfly.idv.tw/dragonfly/read_data.php?id=65431
    '''
    id = 64774
    response_Detailed_discriptions = session.post(general_url + Detailed_discriptions_url + str(id), headers=headers)
    soup = BeautifulSoup(response_Detailed_discriptions.text, 'html.parser')
    Longitude = soup.find(id = 'R_LNG').get('value')
    print('經度 : ' + Longitude)
    Lateral = soup.find(id = 'R_LAT').get('value')
    print('緯度 : ' + Lateral)
    '''


    #\ 嘗試非自己可以看的詳細內容
    '''
    id = 65430
    response_Detailed_discriptions2 = session.post(general_url + Detailed_discriptions_url + str(id), headers=headers)
    soup2 = BeautifulSoup(response_Detailed_discriptions2.text, 'html.parser')
    Longitude = soup2.find(id = 'R_LNG').get('value')
    print('經度 : ' + Longitude)
    Lateral = soup2.find(id = 'R_LAT').get('value')
    print('緯度 : ' + Lateral)
    '''


    '''
    target_url = 'http://dragonfly.idv.tw/dragonfly/member_center.php'
    response = session.get(target_url, headers=headers)
    print(response.text);
    '''



    #\ 解析資料
    """
    Data_List = []
    tmp_List = []
    soup = BeautifulSoup(All_Observation_Data_response.text, 'html.parser')
    for All_Observation_Data_response_Data_Set in soup.find_all(id='theRow'):
        for All_Observation_Data_response_Data in All_Observation_Data_response_Data_Set.find_all('td'):
            # check if the wanted data crawl to the last and avoid the unwanted data
            if All_Observation_Data_response_Data.text == '簡述':
                Data_List.append(simplifyTableInfo(tmp_List[0], tmp_List[1], tmp_List[2], tmp_List[3], tmp_List[4], tmp_List[5], tmp_List[6], tmp_List[7]))
                tmp_List.clear()
                break
            tmp_List.append(All_Observation_Data_response_Data.text)

    for obj in Data_List:
        print(obj, sep =' ')


    #\ 執行GUI input
    #\確認是否成功登入
    soup_login_ckeck = BeautifulSoup(Login_Response.text, 'html.parser')
    script = soup_login_ckeck.find("script").extract() # find the alert
    alert = re.findall(r'(?<=alert\(\").+(?=\")', script.text) #\r\n    alert("登入失敗，請重新登入");\r\n
    if (len(alert) > 0):
        return [ErrorID["Login_error"], ErrorID["Login_error"]] # to show the error that the password or account might be wrong
    """

    #\先確ID認是否超處範圍
    #\ Design to let the function not getting max number again when in the loop.
    overflow = False
    if InputMaxID is None:
        # soup_ID_check = BeautifulSoup(All_Observation_Data_response.text, 'html.parser')
        # All_Observation_Data_response_Data_Set = soup_ID_check.find(id='theRow')
        # Max_All_Observation_Data_response_Data = All_Observation_Data_response_Data_Set.find_all('td')
        # Max_ID_Num = Max_All_Observation_Data_response_Data[0].text
        Max_ID_Num = GetMaxID(session)
    else:
        Max_ID_Num = InputMaxID

    #\ This is the patch for parsing the data from the latest
    #\ If the input ID is not specified(None) then set the ID to the latest
    if Input_ID is None :
        Input_ID = Max_ID_Num

    #\check if the ID is out of the range
    if (Input_ID is not None) and (Input_ID > Max_ID_Num) or (Input_ID < 0):
        overflow = True
        ID_find_result = []
    else:
        #\ 執行
        response_Detailed_discriptions2 = session.post(index.general_url + index.Detailed_discriptions_url + str(Input_ID), headers=headers)
        soup2 = BeautifulSoup(response_Detailed_discriptions2.text, 'html.parser')

        #\ find the description
        # print("\n\n->"+str(soup2.find("textarea", {'id':'R_MEMO'}).text))
        # print(str(soup2.find(id='R_MEMO').text))
        if soup2.find(id='R_MEMO').text is not None and len(soup2.find(id='R_MEMO').text.replace(" ", "")) is not 0:
            Description = soup2.find(id='R_MEMO').text
            print(f"[INFO] Description: {Description}")
            Description = Description.replace(" ", "")
            print(f"[INFO] After removing the space in the Description: {Description}")
        else:
            Description = "None"

        #\ Find the city and district
        response_Brief_discriptions = session.post(index.general_url + index.Brief_discriptions_url + str(Input_ID), headers=headers)
        response_Brief_discriptions_text = BeautifulSoup(response_Brief_discriptions.text, 'html.parser')
        Max_All_Observation_Data_response_Data = response_Brief_discriptions_text.find_all('td')

        """print the colume in sequence
        for i in range(len(Max_All_Observation_Data_response_Data)):
            print(f"({i})\t"+Max_All_Observation_Data_response_Data[i].text)
        """
        for idx in range(len(Max_All_Observation_Data_response_Data)):
            #\ Find the Species list
            if Max_All_Observation_Data_response_Data[idx].text == index.dragonfly_simple_info_species_col_name:
                SpeciesList = Max_All_Observation_Data_response_Data[idx+1].text.split(' ')
                SpeciesList = list(filter(None, SpeciesList))#\ filter out the empty list
                # print(f"[INFO] Species for ID : {Input_ID} -> {SpeciesList}")

            #\ Find the city and district
            if Max_All_Observation_Data_response_Data[idx].text == index.dragonfly_simple_info_city_col_name:
                CityDistrict = Max_All_Observation_Data_response_Data[idx+1].text.split(' - ')[0]
                City = CityDistrict[:3]
                District = CityDistrict[3:]
                # print(f"[INFO] City for ID : {Input_ID} -> {City}\n[INFO] District for ID : {Input_ID} -> {District}")

        #\ Set the rarity for the species
        rarity = CheckSpeciesRarityRates(SpeciesList, Species_filter)

        #\ Save the info to data class
        ID_find_result = DataClass.DetailedTableInfo(str(Input_ID),
                                                    soup2.find(id='日期').get('value'),
                                                    soup2.find(id='時間').get('value'),
                                                    City,
                                                    District,
                                                    soup2.find(id='地點').get('value'),
                                                    soup2.find(id='R_ELEVATION').get('value'),
                                                    soup2.find(id='紀錄者').get('value'),
                                                    soup2.find(id='R_LAT').get('value'),
                                                    soup2.find(id='R_LNG').get('value'),
                                                    "",
                                                    "",
                                                    SpeciesList,
                                                    Description,
                                                    "",
                                                    rarity
                                                    )

    # print(f"[INFO] Return Object: {ID_find_result}")
    return [ID_find_result, overflow, int(Max_ID_Num)]


#\ Get max ID number
def GetMaxID(session)->int:
    """
    params:
        session for login
    return :
        Max id number,
        All_Observation_Data_response
    """
    All_Observation_Data_response = session.post(index.All_Observation_Data_url, headers=headers)
    soup_ID_check = BeautifulSoup(All_Observation_Data_response.text, 'html.parser')
    All_Observation_Data_response_Data_Set = soup_ID_check.find(id='theRow')
    Max_All_Observation_Data_response_Data = All_Observation_Data_response_Data_Set.find_all('td')
    return int(Max_All_Observation_Data_response_Data[0].text)


#\ ------------------------------------------------------------------------------
#\ for testing
# [session, Login_Response, Login_state] = Login_Web("-----", "-------")
# DataCrawler(session, "77257")



#\ Craw data as request date range
def CrawDataByDate(session, start_time:datetime, end_time:datetime, species_filter:list):
    condition = True
    initID = None
    counter = 0
    result_list = [] # this will be the 2D list
    Max_ID_Num = None
    while condition:
        [ID_find_result, overflow, Max_ID_Num] = DataCrawler(session, initID, Max_ID_Num, species_filter)
        print(f"ID: {initID}")

        #\ return if overflow
        if overflow:
            print("[Warning] In the CrawDataByDate() ID overflow")
            return

        #\ break out while loop condition
        if CheckIDDate(start_time, end_time, datetime.strptime(ID_find_result.Dates, "%Y-%m-%d")):
            counter += 1
            initID = Max_ID_Num - counter

            #\ Accumulate the data if this came from the same day, same place, same city, same district, same recorder
            """
            if CheckDataSameOrNot(result_list, ID_find_result) is False:
                #\ Append the result if not repeat
                result_list.append([ID_find_result])
            """

            result_list.append([ID_find_result])
        else:
            condition = False

    return result_list



#\ Check if the Data Date is valid or not
def CheckIDDate(start_time:datetime, end_time:datetime, check_time:datetime)->bool:
    if start_time <= check_time <= end_time:
        return True
    else:
        return False




#\ Check if the data can accumulate to one with same day, same place, same city, same district, same recorder
#\ if same then append the data.
def CheckDataSameOrNot(result_list:list, ID_find_result:list):
    for idx, lst in enumerate(result_list):
        if lst.User == ID_find_result.User and \
            lst.Dates == ID_find_result.Dates and \
            lst.City == ID_find_result.City and \
            lst.District == ID_find_result.District and \
            lst.Place == ID_find_result.Place:
                result_list[idx].append(ID_find_result)



#\ filter to filter out the data with specific condition
def DataFilter(Data:DataClass.DetailedTableInfo, user_filter:list=None, species_filter:list=None, KeepOrFilter:bool=None)->list:
    """
     @params:
          user to filter
          species to filter
          KeepOrFilter: indicate to do filter(False) or keep(True) the data if satisfied the condition
     @return:
        if KeepOrFilter True to keep the data
          True: Filter out
          False: Not Filter out to keep
        if KeepOrFilter False to filter the data
          True: keep
          False: not to keep to filter out
    """
    Filter_State = False

    #\ No input then return True, since nothing is going to filter
    if user_filter is None and species_filter is None:
        return True

    #\ user filter
    if user_filter is not None:
        if len(user_filter) > 0:
            Filter_State = Data.User in user_filter
    #\ species filter
    if species_filter is not None:
        if len(species_filter) > 0:
            Species_intersection_set = set(Data.SpeciesList) & set(species_filter)
            Filter_State = len(Species_intersection_set) > 0

    return [Filter_State if KeepOrFilter is True else not Filter_State, Species_intersection_set]




#\ Check the species rank rates
#\ return the "maximum" rank number in the list
def CheckSpeciesRarityRates(Species_intersection:list, species_filter:list)->str:
    #\ this specify the species is not in the filter, which you want to filter out and don't want to see
    rarity = -1

    if Species_intersection is not None and species_filter is not None:
        for species in Species_intersection:
            if species in species_filter:
                rarity = max([species_filter.index(species)])
        #print(f"[INFO] in CheckSpeciesRarityRates() the rarity is : {rarity}")

        if rarity >= species_filter.index(index.StartOfSR_Species) :
            return "SR" #\ Super Rare
        elif rarity >= species_filter.index(index.StartOfR_Species) :
            return "R" #\ Rare
        elif rarity > 0:
            return "N" #\ Normal
        else:
            return "None" #\ too usual to see.
    else:
        return "None"



#\ Crawl data until certain ID
#\  This function will be call in Todays data crwal function
#\  since the data been uploaded to the data web will not be the
#\  same as the it's record date. Therefore, we select the data
#\  based on the ID renew in the midnight everyday to tell which
#\  ID correspond to the start of the that day to indicate the time.
def CrawlDataByIDRange(session, Start_ID:int, End_ID:int, filter_object:list)->List[DataClass.DetailedTableInfo]:
    """[summary]

    Args:
        session ([type]): session
        Start_ID (int): Start_ID (last)
        End_ID (int): End_ID (initial)
        filter_object (list of lists):

    Returns:
        list:
    """
    [User_filter, Species_filter, KeepOrFilter] = filter_object
    Max_ID_Num = None
    counter = 0
    condition = True
    result_list = []
    while condition:
        [ID_find_result, overflow, Max_ID_Num] = DataCrawler(session, End_ID, Max_ID_Num, Species_filter)

        #\ Return if overflow
        if overflow:
            print("[Warning] In the CrawDataByDate() ID overflow")
            return

        #\ Go to the next ID
        counter += 1
        End_ID = Max_ID_Num - counter

        #\ Check the condition
        if End_ID >= Start_ID:
            #\ Filter out the unwanted info
            [Status, Species_intersection_set] = DataFilter(ID_find_result, User_filter, Species_filter, KeepOrFilter)
            if Status:
                result_list.append(ID_find_result)

        else :
            condition = False

    # print(f"[INFO] In CrawlDataByIDRange() the result list is {result_list}")
    return result_list



#\ Craw today's data
def CrawTodayData(session, TodayFirstID:int, filter_object:List):
    #CrawDataByDate(session, datetime.now(), datetime.now())
    return CrawlDataByIDRange(session, TodayFirstID, None, filter_object)



#\ Get the species recording number rank from the website
def GetSpeciesRecordingNumberRank(session)->list:
    """[summary]

    Args:
        session ([type]): [description]

    Returns:
        dict: {name:count ,name2:count2,....}
        list: [name, name1, name2, ......]
    """

    #\ Get the data from the website via beautiful soup
    species_number_rank_response = session.post(index.species_number_rank_url, headers=headers)
    soup_number_species_check = BeautifulSoup(species_number_rank_response.text, 'html.parser')
    Data_td_tag = soup_number_species_check.find_all('td')
    #Data_td_tag = Data_tr_tag.find_all('td')

    #\ Extract the text from the html tags <td>
    #\ The return list : Species_rank_list will be Species_rank_list[the_rank_number] = ["species_name", "total_recording_number"]
    #\   <tr>
    #\      <td align="center">1</td>
    #\      <td>薄翅蜻蜓</td>
    #\      <td align="right">11267</td>
    #\      <td align="right">5.96 %</td>
    #\  <tr>
    Species_rank_dict = dict()
    Species_rank_list_only_name = []
    #\ i = 2--> workaround to skip the unused column name and title
    for i in range(2, len(Data_td_tag), 4):
        td = Data_td_tag[i:i+3]
        Species_rank_dict[td[0].text] = td[1].text
        Species_rank_list_only_name.append(td[0].text)

    #\ The first is the most common one which own most records
    return [Species_rank_dict, Species_rank_list_only_name]




#\ Test
#\ Use this to test the function required session
# [session, Login_Response, Login_state] = Login_Web("USER", "PW")
# print(GetSpeciesRecordingNumberRank(session)[1][60:])
# print(GetSpeciesRecordingNumberRank(session)[1])
# print(GetSpeciesRecordingNumberRank(session))
