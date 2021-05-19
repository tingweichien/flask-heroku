import proxyscrape
from typing import List
import requests
from bs4 import BeautifulSoup
import DataClass
import index
from fake_useragent import UserAgent
import re


#\ seesion
session = requests.Session()



#\--->Now use random fake user agent
# https://ithelp.ithome.com.tw/articles/10209356
UA = UserAgent()
headers = {
        'User-Agent' : UA.random,
}


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

    #\ Login account and password
    data = {
        'account' : Input_account,
        'password' : Input_password,
    }

    Login_state = True
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
            soup_login_ckeck = BeautifulSoup(Login_Response.text, 'html.parser')
            script = soup_login_ckeck.find("script").extract() # find the alert
            alert = re.findall(r'(?<=alert\(\").+(?=\")', script.text) #\r\n    alert("登入失敗，請重新登入");\r\n
            if (len(alert) > 0):
                Login_state = False # to show the error that the password or account might be wrong
            return [session, Login_Response, Login_state]

    #\ retry failed
    print("[waning] Login failed")
    return [None, None, None]


###################################################################
def DataCrawler(Login_Response, Input_ID:str)->list:
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    }
    '''

    #\ Login account and password
    '''
    data = {
        'account' : Input_account,
        'password' : Input_password,
    }
    '''



    #\ 執行登入
    '''
    session = requests.Session()
    Login_Response = session.post(Login_url, headers=headers, data=data)
    '''


    #\ 執行進入"蜓種觀察資料查詢作業"
    All_Observation_Data_response = session.post(index.All_Observation_Data_url, headers=headers)


    #\ 下一頁
    '''
    page = 1
    response_next_page = session.post(All_Observation_Data_url + Next_page_url + str(page), headers=headers)
    #print(response_next_page.text)
    '''


    #\ 執行點入簡述
    # request url = http://dragonfly.idv.tw/dragonfly/view_data.php?id=65431
    '''
    id = 65431
    response_Brief_discriptions = session.post(general_url + Brief_discriptions_url + str(id), headers=headers)
    print(response_Brief_discriptions.text)
    '''



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
    overflow = False
    soup_ID_check = BeautifulSoup(All_Observation_Data_response.text, 'html.parser')
    All_Observation_Data_response_Data_Set = soup_ID_check.find(id='theRow')
    Max_All_Observation_Data_response_Data = All_Observation_Data_response_Data_Set.find_all('td')
    Max_ID_Num = Max_All_Observation_Data_response_Data[0].text
    #\check if the ID is out of the range
    if (int(Input_ID) > int(Max_All_Observation_Data_response_Data[0].text) or int(Input_ID) < 0):
        overflow = True
        ID_find_result = []
    else:
        #\ 執行
        response_Detailed_discriptions2 = session.post(index.general_url + index.Detailed_discriptions_url + Input_ID, headers=headers)
        soup2 = BeautifulSoup(response_Detailed_discriptions2.text, 'html.parser')
        Longitude = soup2.find(id = 'R_LNG').get('value')
        print('經度 : ' + Longitude)
        Lateral = soup2.find(id = 'R_LAT').get('value')
        print('緯度 : ' + Lateral)
        ID_find_result = DataClass.DetailedTableInfo(Input_ID,
                                            soup2.find(id='日期').get('value'),
                                            soup2.find(id='時間').get('value'),
                                            "",
                                            "",
                                            soup2.find(id='地點').get('value'),
                                            soup2.find(id='R_ELEVATION').get('value'),
                                            soup2.find(id='紀錄者').get('value'),
                                            soup2.find(id='R_LAT').get('value'),
                                            soup2.find(id='R_LNG').get('value'),
                                            "",
                                            "",
                                            soup2.find(id='R_MEMO').get('value'))

    return [ID_find_result, overflow, int(Max_ID_Num)]