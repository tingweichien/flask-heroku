##############################
#\                          /#
#\     Line BOt Event       /#
#\                          /#
##############################

from typing import List
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FollowEvent, FlexSendMessage, PostbackEvent, LocationSendMessage, flex_message
import configparser
from flask import request, abort
import index
from index import *
from VarIndex import *
import LineBotMsgHandler
import DragonflyData
import Database
import datetime
import random
from gSheetAPI import Sheet_id_dict
import urllib
import urllib.request, urllib.parse
import yaml
import DataClass
import logging

#\ -- Global --
config = configparser.ConfigParser()
config.read('./Key/config.ini')
gLine_bot_api = LineBotApi(config.get("line-bot", "channel_access_token"))
gHandler = WebhookHandler(config.get('line-bot', 'channel_secret'))

def LineBotHandler(app):
    logging.debug("LineBotHandler")
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    logging.info(f"Body-->{body}")

    try:
        gHandler.handle(body, signature)
    except InvalidSignatureError:
        logging.warning("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@gHandler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    if cache.get("gLoginStatus") == False:
        if CheckUserInfo(event) == True:
            gLine_bot_api.link_rich_menu_to_user(event.source.user_id, cache.get("RichMenuID")["Main Richmenu"])

    if cache.get("gIsJustText") == True:
        cache.set("gEventText", event.message.text.lower().replace(" ", ""))
        CheckEvent(cache.get("gEventText"))

    if cache.get("gEvent") == eLineBotEvent.LOGIN.value:
        if cache.get("gLoginStatus") == True:
            gLine_bot_api.reply_message(event.reply_token, TextSendMessage(text="Already Login"))
            gLine_bot_api.link_rich_menu_to_user(event.source.user_id, cache.get("RichMenuID")["Main Richmenu"])
            cache.set("gIsJustText", True)
        else :
            LoginProgress(event)

    elif cache.get("gEvent") == eLineBotEvent.MENU.value:
        if pleaseLogin(event) == True:
            cache.set("gIsJustText", True)

    elif cache.get("gEvent") == eLineBotEvent.IDREQUEST.value:
        if pleaseLogin(event) == True:
            IDRequestfinish = IDRequestCallback(event)
            if IDRequestfinish == True:
                cache.set("gIsJustText", True)

    elif cache.get("gEvent") == eLineBotEvent.RECORD.value:
        if pleaseLogin(event) == True:
            cache.set("gIsJustText", True)

    elif cache.get("gEvent") == eLineBotEvent.SETTING.value:
        if pleaseLogin(event) == True:
            cache.set("gIsJustText", True)

    elif cache.get("gEvent") == eLineBotEvent.SEARCH.value:
        if pleaseLogin(event) == True:
            search_flex_message = FlexSendMessage(alt_text="Please type IDRequest or Advance Search", contents=LineBotMsgHandler.Search_event_text)
            gLine_bot_api.reply_message(event.reply_token, search_flex_message)
            cache.set("gIsJustText", True)

    elif cache.get("gEvent") == eLineBotEvent.TODAYDATA.value:
        if pleaseLogin(event) == True:
            GetTodayDataSend2LINEBot(event.source.user_id, event.reply_token, True, index.Hourly_Summary_default_data_filter)
            cache.set("gIsJustText", True)
    else :
        cache.set("gEvent", eLineBotEvent.NONE.value)
        gLine_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))

def CheckEvent(event_text:str):
    if event_text == "login":
        cache.set("gEvent", eLineBotEvent.LOGIN.value)
        cache.set("gIsJustText", False)
    elif event_text == "menu" :
        cache.set("gEvent", eLineBotEvent.MENU.value)
        cache.set("gIsJustText", False)
    elif event_text == "idrequest" :
        cache.set("gEvent", eLineBotEvent.IDREQUEST.value)
        cache.set("gIsJustText", False)
    elif event_text == "record" :
        cache.set("gEvent", eLineBotEvent.RECORD.value)
        cache.set("gIsJustText", False)
    elif event_text == "setting" :
        cache.set("gEvent", eLineBotEvent.SETTING.value)
        cache.set("gIsJustText", False)
    elif event_text == "search" :
        cache.set("gEvent", eLineBotEvent.SEARCH.value)
        cache.set("gIsJustText", False)
    elif event_text == "todaydata" :
        cache.set("gEvent", eLineBotEvent.TODAYDATA.value)
        cache.set("gIsJustText", False)
    else:
        cache.set("gEvent", eLineBotEvent.NONE.value)

def CheckUserInfo(event):
    DB_Data = Database.ReadFromDB(Database.CreateDBConection(), Database.Read_userinfo_query(event.source.user_id), True)
    if DB_Data is not None:
        cache.set("gLoginStatus", True)
        return True
    else :
        return False

def pleaseLogin(event):
    if cache.get("gLoginStatus") != True:
        gLine_bot_api.reply_message(event.reply_token, TextSendMessage(text="Please Login first to use this function"))
        return False
    else:
        return True

def AskInputID(event):
    gLine_bot_api.reply_message(event.reply_token, TextSendMessage(text="Please Enter the request ID"))

def IDRequestCallback(event):
    tmpCnt = cache.get("gEventCnt")
    tmpCnt += 1
    cache.set("gEventCnt", tmpCnt)
    if tmpCnt == 1:
        AskInputID(event)
        return False
    elif tmpCnt == 2:
        DragonflyData_session, _ = CreateWebSession(event)
        try :
            IDNumber = int(event.message.text)
        except:
            gLine_bot_api.reply_message(event.reply_token, "Input ID number is not integer !!!!!!!!!!!")
            cache.set("gEventCnt", 0)
            return False

        [ID_find_result, overflow, Max_ID_Num] = DragonflyData.DataCrawler(DragonflyData_session, IDNumber, None, index.Hourly_Summary_default_data_filter)

        if overflow:
            gLine_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"The ID is overflow, please use the ID smaller {Max_ID_Num}"))
        else:
            if ID_find_result.Description is not None:
                ID_find_result.Description = f"\n{' '*10}".join(list(ID_find_result.Description.split("\n")))
            
            RequestDataText = FlexSendMessage(alt_text=f"[IdNumber]: {ID_find_result.IdNumber}\n"+\
                                                        f"[Dates]: {ID_find_result.Dates}, {ID_find_result.Times}\n"+\
                                                        f"[City]: {ID_find_result.City} {ID_find_result.District}\n"+\
                                                        f"[Place]: {ID_find_result.Place}\n"+\
                                                        f"[Altitude]: {ID_find_result.Altitude}\n" +\
                                                        f"[User]: {ID_find_result.User}\n"+\
                                                        f"[Latitude]: {ID_find_result.Latitude}\n"+\
                                                        f"[Longitude]: {ID_find_result.Longitude}\n"\
                                                        f"[Speceis]: {', '.join(ID_find_result.SpeciesList)}\n"+\
                                                        f"[Description]: {ID_find_result.Description}\n",
                                                contents=LineBotMsgHandler.RequestDataMsgText_handler(LineBotMsgHandler.RequestDataMsgText, ID_find_result)
                                            )
            gLine_bot_api.reply_message(event.reply_token, RequestDataText)
        cache.set("gEventCnt", 0)
        return True

def CreateWebSession(event=None, CloseDBConn=True):
    if event is not None:
        read_query = Database.Read_userinfo_query(event.source.user_id)
        fetchone = True
    else:
        read_query = Database.Read_all_query(index.UserInfoTableName)
        fetchone = False

    conn = Database.CreateDBConection()
    if conn is None:
        return None, None

    DB_Data = Database.ReadFromDB(conn, read_query, fetchone, CloseDBConn)
    if DB_Data is None:
        logging.warning("No DB Data return")

    if event is not None and fetchone == True:
        ACC, PW = DB_Data[4], DB_Data[5]
    else:
        idx = random.randint(0, len(DB_Data)-1)
        ACC, PW = DB_Data[idx][4], DB_Data[idx][5]

    [session, _, Login_state] = DragonflyData.Login_Web(ACC, PW)
    if Login_state == False:
        return None, None
    else:
        return session, conn

@gHandler.add(FollowEvent)
def handle_follow_message(event):
    for idx in range(len(index.JoinEventText)):
        gLine_bot_api.reply_message(event.reply_token, TextSendMessage(text=index.JoinEventText[idx]))
    InitCache(cache)
    OEMSetDefaultRichmenu(gLine_bot_api, event)

def LineBotLogin2Web(login_account:str, login_password:str)->str:
    [Dragonfly_session, Login_Response, Login_state] = DragonflyData.Login_Web(login_account, login_password)
    if (Login_state == False):
        return "Account or Password might be incorrect!!!!"
    elif Login_Response is None and Login_state is None:
        return " No connection to server, check the internet connection!!!"
    else:
        cache.set("gLoginStatus", True)
        cache.set("Dragonfly_session", Dragonfly_session)
        return "Login state success~"

def LoginProgress(event):
    if cache.get("gEventCnt") is None:
        tmpCnt = 0
    else :
        tmpCnt = cache.get("gEventCnt")
    tmpCnt += 1
    cache.set("gEventCnt", tmpCnt)

    if cache.get("gEventCnt") == 4:
        if event.message.text == "LOGIN_CONFIRM":
            gLine_bot_api.reply_message(event.reply_token, TextSendMessage(text="Start to Login~"))
            LoginStateMessage = LineBotLogin2Web(cache.get("gAccount"), cache.get("gPassword"))
            gLine_bot_api.push_message(event.source.user_id, TextSendMessage(text=LoginStateMessage))

            if cache.get("gLoginStatus") == True:
                if index.CreateDataBase:
                    Database.ExecuteDB(Database.CreateDBConection(), Database.UserInfo_create_table_query)

                request_userinfo = gLine_bot_api.get_profile(event.source.user_id)
                InsertData = (
                    request_userinfo.display_name,
                    event.source.user_id,
                    datetime.datetime.now().strftime("%Y-%m-%d"),
                    cache.get("gAccount"),
                    cache.get("gPassword")
                )
                Database.InsertDB(Database.CreateDBConection(), Database.Insert_userinfo_query(), InsertData)
                gLine_bot_api.link_rich_menu_to_user(event.source.user_id, cache.get("RichMenuID")["Main Richmenu"])

        elif event.message.text == "LOGIN_FAIL":
            cache.set("gEventCnt", 1)
        elif event.message.text == "LOGIN_EXIT":
            cache.set("gEventCnt", 0)

    elif cache.get("gEventCnt") == 1:
        gLine_bot_api.reply_message(event.reply_token, TextSendMessage(text=index.LoginEventText[0]))
    elif cache.get("gEventCnt") == 2:
        gLine_bot_api.reply_message(event.reply_token, TextSendMessage(text=index.LoginEventText[1]))
        cache.set("gAccount", event.message.text)
    elif cache.get("gEventCnt") == 3:
        cache.set("gPassword", event.message.text)
        LineBotMsgHandler.LoginCheckText["body"]["contents"][1]["contents"][0]["contents"][1]["text"] = cache.get("gAccount")
        LineBotMsgHandler.LoginCheckText["body"]["contents"][1]["contents"][1]["contents"][1]["text"] = cache.get("gPassword")
        flex_message = FlexSendMessage(alt_text=f'Hi, Check again for the login info:\nAccount: {cache.get("gAccount")}\nPassword: {cache.get("gPassword")}',
                                        contents=LineBotMsgHandler.LoginCheckText)
        gLine_bot_api.reply_message(event.reply_token, flex_message)
    else:
        cache.set("gIsJustText", True)
        cache.set("gEventCnt", 0)
        cache.set("gEvent", eLineBotEvent.NONE.value)

def OEMSetDefaultRichmenu(linebot_api, event):
    LoginState = CheckUserInfo(event)
    LineBotMsgHandler.DefaultRichMenu(linebot_api, LoginState)

def CheckCurrentAndLatestID(conn, current_crawling_id_db:int, Latest_ID:int, user_id:str):
    if current_crawling_id_db is not None:
        Database.InsertDB(conn, Database.Update_userinfo_query(index.UserInfo_current_crawling_id), (current_crawling_id_db, user_id))
        return current_crawling_id_db
    elif current_crawling_id_db is None and Latest_ID is not None:
        Database.InsertDB(conn, Database.Update_userinfo_query(index.UserInfo_current_crawling_id), (Latest_ID, user_id))
        return None
    return None

def GetTodayDataSend2LINEBot(user_id:str="", reply_token:str="", AllDayData:bool=True,
                             filter:DataClass.FilterObject=None, conn=None, DragonflyData_session=None):
    if user_id == "":
        return

    if reply_token != "":
        gLine_bot_api.reply_message(reply_token, TextSendMessage(text="Please be patient, it might take a while~~"))

    if DragonflyData_session is None:
        DragonflyData_session, conn = CreateWebSession(CloseDBConn=False)

    if AllDayData == True:
        TimeIntevalDataList = DragonflyData.CrawTodayData(DragonflyData_session, int(cache.get("DataBaseVariable")["LatestDataID"]), filter)
    else :
        if conn is None:
            return
        current_crawling_id_db = int(Database.ReadFromDB(conn, Database.Read_col_userinfo_query(index.UserInfo_current_crawling_id, user_id), True, False)[0])
        Latest_ID = DragonflyData.GetMaxID(DragonflyData_session)
        current_cawling_ID = CheckCurrentAndLatestID(conn, current_crawling_id_db, Latest_ID, user_id)
        if current_cawling_ID is None or current_cawling_ID == int(Latest_ID):
            return None
        TimeIntevalDataList = DragonflyData.CrawlDataByIDRange(DragonflyData_session, current_cawling_ID, int(Latest_ID), filter)
        Database.InsertDB(conn, Database.Update_userinfo_query(index.UserInfo_current_crawling_id), (Latest_ID, user_id))
        if len(TimeIntevalDataList) == 0:
            return None

    content_list = []
    for data in TimeIntevalDataList:
        bubble_content = LineBotMsgHandler.RequestDataMsgText_handler(LineBotMsgHandler.RequestDataMsgText, data)
        content_list.append(bubble_content)

    if len(content_list) == 0:
        gLine_bot_api.push_message(user_id, TextSendMessage(text="No data updated today"))
    else:
        for content_idx in range(0, len(content_list), index.CarsoulBubbleLimit):
            end = content_idx + index.CarsoulBubbleLimit - 1
            content_limit_list = content_list[content_idx:] if end >= len(content_list) else content_list[content_idx:end]
            Msgtext = FlexSendMessage(alt_text="No data", contents=LineBotMsgHandler.MultiRequestDataMsgText(content_limit_list))
            gLine_bot_api.push_message(user_id, Msgtext)

#\ --- 快取與資料庫防呆初始化機制 ---
def InitCache(_cache):
    _cache.set("gEventText", None)
    _cache.set("gEvent", eLineBotEvent.NONE.value)
    _cache.set("gEventCnt", 0)
    _cache.set("gIsJustText", True)
    _cache.set("gLoginDataConfirm", False)
    _cache.set("gLoginStatus", False)
    _cache.set("gUserID", None)
    _cache.set("gAccount", None)
    _cache.set("gPassword", None)
    _cache.set("Dragonfly_session", None)
    _cache.set("DBInfo", Database.InitDBInfo())
    
    try:
        _cache.set("RichMenuID", LineBotMsgHandler.Get_RichMenu(gLine_bot_api))
    except Exception as e:
        logging.warning(f"Unable to fetch RichMenu: {e}")
        _cache.set("RichMenuID", None)

    conn = Database.CreateDBConection()
    if conn:
        Database.ExecuteDB(conn, Database.UserInfo_create_table_query)
        Database.ExecuteDB(conn, Database.Variable_create_table_query)
        
        db_data = Database.ReadFromDB(conn, Database.Read_all_query(index.VariableTableName), False)
        
        # 驗證通過的核心修復：確保 3元素 tuple 可以被正確轉為 dictionary
        if db_data:
            var_dict = {row[1]: row[2] for row in db_data}
            _cache.set("DataBaseVariable", var_dict)
        else:
            Database.InsertDB(conn, Database.Insert_variable_query(index.VariableTableName), ("LatestDataID", "0"), False)
            _cache.set("DataBaseVariable", {"LatestDataID": "0"})
            
        Database.CloseDBConnection(conn)
    else:
        _cache.set("DataBaseVariable", {"LatestDataID": "0"})

    _cache.set("DAYAlarm", index.DAYAlarm)
    
    try:
        _cache.set("gGSheetList", Sheet_id_dict())
    except Exception as e:
        logging.warning(f"Unable to fetch GSheetList: {e}")
        _cache.set("gGSheetList", {})
        
    _cache.set("gLN_AccessToken", None)

@gHandler.add(PostbackEvent)
def handle_postback_event(event):
    PostBackEventRawString = event.postback.data.lower().replace(" ", "")
    PostbackEvent = CheckPostEvent(PostBackEventRawString)
    if PostbackEvent == eLineBotPostEvent.OTHERS.value:
        gLine_bot_api.link_rich_menu_to_user(event.source.user_id,cache.get("RichMenuID")["Main2 Richmenu"])
    elif PostbackEvent == eLineBotPostEvent.GOBACKMAIN.value:
        gLine_bot_api.link_rich_menu_to_user(event.source.user_id,cache.get("RichMenuID")["Main Richmenu"])
    elif PostbackEvent == eLineBotPostEvent.SHOWONMAP.value:
        [Id, Addr, Lat, Lng, species] = PostBackEventRawString.split("_")[1:]
        if Lat != "none" and Lng != "none":
            gLine_bot_api.push_message(event.source.user_id, LocationSendMessage(title=f'#{Id}-{species}', address=Addr, latitude=float(Lat), longitude=float(Lng)))
        else:
            gLine_bot_api.push_message(event.source.user_id, TextSendMessage(text="Sorry~\n The Latitude and the Longitude is None"))

def CheckPostEvent(event_text:str):
    if event_text == "others":
        return eLineBotPostEvent.OTHERS.value
    elif event_text == "gobackmain":
        return eLineBotPostEvent.GOBACKMAIN.value
    elif event_text.split("_")[0] == "showonmap":
        return eLineBotPostEvent.SHOWONMAP.value
    else:
        return eLineBotPostEvent.NONE.value

def create_auth_link(user_id, client_id=index.LN_Client_ID, redirect_uri=index.LN_redirect_uri):
    data = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': 'notify',
        'state': user_id
    }
    query_str = urllib.parse.urlencode(data)
    gLine_bot_api.push_message(user_id, TextSendMessage(text=f"Please click the following link to authorize the LINE Notify, select \"1-on-1 chat with LINE Notify\"\nhttps://notify-bot.line.me/oauth/authorize?{query_str}"))

def Check_LN_Key_exist(userid: str):
    Userinfo_access_token = Database.ReadFromDB(Database.CreateDBConection(), Database.Read_col_userinfo_query("access_token", userid), True)
    cache.set("gUserID", userid)
    if Userinfo_access_token[0] is None:
        create_auth_link(userid)
    else:
        cache.set("gLN_AccessToken", Userinfo_access_token[0])

def LN_get_token(code:str, client_id:str=index.LN_Client_ID, client_secret:str=index.LN_Client_Secret, redirect_uri:str=index.LN_redirect_uri):
    url = 'https://notify-bot.line.me/oauth/token'
    headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    }
    data = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=data, headers=headers)
    page = urllib.request.urlopen(req).read()
    res = yaml.safe_load(page)
    Database.InsertDB(Database.CreateDBConection(), Database.Update_userinfo_query("access_token"), (res['access_token'], cache.get("gUserID")))
    cache.set("gLN_AccessToken", res['access_token'])
    return res['access_token']

def LN_send_message(access_token:str=None, text_message:str=None, picurl:str=None):
    if access_token is None:
        return
    else:
        url = 'https://notify-api.line.me/api/notify'
        headers = {"Authorization": "Bearer "+ access_token}
    if text_message is None:
        return

    DataToSend = dict()
    DataToSend = {'message': text_message}
    if picurl is not None:
        temp_data = {"stickerPackageId": 2, 'stickerId': 38, 'imageThumbnail':picurl, 'imageFullsize':picurl}
        DataToSend.update(temp_data)

    data = urllib.parse.urlencode(DataToSend).encode()
    req = urllib.request.Request(url, data=data, headers=headers)
    page = urllib.request.urlopen(req).read()