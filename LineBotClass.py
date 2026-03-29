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

config = configparser.ConfigParser()
config.read('./Key/config.ini')

# 核心修復：將 LINE API 的連線超時時間從預設的 5 秒提高到 20 秒，避免 Render 免費節點網路波動導致 Timeout
gLine_bot_api = LineBotApi(config.get("line-bot", "channel_access_token"), timeout=20)
gHandler = WebhookHandler(config.get('line-bot', 'channel_secret'))

def LineBotHandler(app):
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        gHandler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    except Exception as e:
        # 核心修復：攔截所有 LINE SDK 拋出的網路或連線錯誤，防止伺服器 500 崩潰
        logging.error(f"[LineBotHandler Error] {e}")
    return 'OK'

@gHandler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    if cache.get("gLoginStatus") == False:
        if CheckUserInfo(event) == True:
            try:
                gLine_bot_api.link_rich_menu_to_user(event.source.user_id, cache.get("RichMenuID")["Main Richmenu"])
            except Exception as e:
                logging.error(f"Link RichMenu Error: {e}")

    if cache.get("gIsJustText") == True:
        cache.set("gEventText", event.message.text.lower().replace(" ", ""))
        CheckEvent(cache.get("gEventText"))

    if cache.get("gEvent") == eLineBotEvent.LOGIN.value:
        if cache.get("gLoginStatus") == True:
            try:
                gLine_bot_api.reply_message(event.reply_token, TextSendMessage(text="Already Login"))
                gLine_bot_api.link_rich_menu_to_user(event.source.user_id, cache.get("RichMenuID")["Main Richmenu"])
            except Exception as e:
                logging.error(f"Login reply error: {e}")
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
            try:
                search_flex_message = FlexSendMessage(alt_text="Please type IDRequest or Advance Search", contents=LineBotMsgHandler.Search_event_text)
                gLine_bot_api.reply_message(event.reply_token, search_flex_message)
            except Exception as e:
                logging.error(f"Search reply error: {e}")
            cache.set("gIsJustText", True)

    elif cache.get("gEvent") == eLineBotEvent.TODAYDATA.value:
        if pleaseLogin(event) == True:
            GetTodayDataSend2LINEBot(event.source.user_id, event.reply_token, False, index.Hourly_Summary_default_data_filter)
            cache.set("gIsJustText", True)
    else :
        cache.set("gEvent", eLineBotEvent.NONE.value)
        try:
            gLine_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))
        except Exception as e:
            logging.error(f"Echo reply error: {e}")

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
        try:
            gLine_bot_api.reply_message(event.reply_token, TextSendMessage(text="登入時效已過或尚未登入，請重新登入以使用此功能。"))
        except Exception as e:
            logging.error(f"pleaseLogin reply_message error: {e}")
            
        try:
            rich_menu_id = cache.get("RichMenuID").get("Login Richmenu")
            if rich_menu_id:
                gLine_bot_api.link_rich_menu_to_user(event.source.user_id, rich_menu_id)
        except Exception as e:
            logging.error(f"Failed to change RichMenu to Login: {e}")
        return False
    else:
        return True

def AskInputID(event):
    try:
        gLine_bot_api.reply_message(event.reply_token, TextSendMessage(text="Please Enter the request ID"))
    except Exception as e:
        logging.error(f"AskInputID error: {e}")

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
            try:
                gLine_bot_api.reply_message(event.reply_token, TextSendMessage(text="Input ID number is not integer !!!!!!!!!!!"))
            except Exception as e:
                pass
            cache.set("gEventCnt", 0)
            return False

        [ID_find_result, overflow, Max_ID_Num] = DragonflyData.DataCrawler(DragonflyData_session, IDNumber, None, index.Hourly_Summary_default_data_filter)

        try:
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
        except Exception as e:
            logging.error(f"IDRequestCallback reply error: {e}")
            
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
    try:
        for idx in range(len(index.JoinEventText)):
            gLine_bot_api.reply_message(event.reply_token, TextSendMessage(text=index.JoinEventText[idx]))
    except Exception as e:
        logging.error(f"FollowEvent error: {e}")
        
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

    try:
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
    except Exception as e:
        logging.error(f"LoginProgress error: {e}")

def OEMSetDefaultRichmenu(linebot_api, event):
    LoginState = CheckUserInfo(event)
    LineBotMsgHandler.DefaultRichMenu(linebot_api, LoginState)

def CheckCurrentAndLatestID(conn, current_crawling_id_db:int, Latest_ID:int, user_id:str):
    if current_crawling_id_db is not None:
        Database.InsertDB(conn, Database.Update_userinfo_query(index.UserInfo_current_crawling_id), (current_crawling_id_db, user_id))
        return current_crawling_id_db
    elif current_crawling_id_db is None and Latest_ID is not None:
        Database.InsertDB(conn, Database.Update_userinfo_query(index.UserInfo_current_crawling_id), (Latest_ID, user_id))
        return Latest_ID
    return None

def GetTodayDataSend2LINEBot(user_id:str="", reply_token:str="", AllDayData:bool=False,
                             filter:DataClass.FilterObject=None, conn=None, DragonflyData_session=None):
    if user_id == "":
        return

    if DragonflyData_session is None:
        DragonflyData_session, conn = CreateWebSession(CloseDBConn=False)
        
    if conn is None:
        return

    db_result = Database.ReadFromDB(conn, Database.Read_col_userinfo_query(index.UserInfo_current_crawling_id, user_id), True, False)
    
    current_crawling_id_db = None
    if db_result and db_result[0] is not None:
        current_crawling_id_db = int(db_result[0])
        
    Latest_ID = DragonflyData.GetMaxID(DragonflyData_session)
    
    if current_crawling_id_db is None:
        current_crawling_id_db = max(0, Latest_ID - 10)

    current_cawling_ID = CheckCurrentAndLatestID(conn, current_crawling_id_db, Latest_ID, user_id)

    if current_cawling_ID is None or current_cawling_ID >= int(Latest_ID):
        if reply_token != "":
            try:
                gLine_bot_api.reply_message(reply_token, TextSendMessage(text="目前沒有新的資料更新。"))
            except Exception as e:
                logging.error(f"GetTodayDataSend2LINEBot reply error: {e}")
        return None

    fetch_limit = 10
    has_more = False
    target_End_ID = int(Latest_ID)

    if (int(Latest_ID) - current_cawling_ID) > fetch_limit:
        target_End_ID = current_cawling_ID + fetch_limit
        has_more = True

    if reply_token != "":
        msg = "請稍候，正在為您抓取資料...\n(為避免被網站封鎖，已啟動擬真讀取模式)"
        if has_more:
            msg += f"\n\n※ 累積資料較多，本次將為您抓取 {fetch_limit} 筆 (進度: {target_End_ID}/{Latest_ID})。看完後請再次點擊 TodayData 繼續抓取。"
        try:
            gLine_bot_api.reply_message(reply_token, TextSendMessage(text=msg))
        except Exception as e:
            logging.error(f"GetTodayDataSend2LINEBot progress reply error: {e}")

    TimeIntevalDataList = DragonflyData.CrawlDataByIDRange(DragonflyData_session, current_cawling_ID, target_End_ID, filter)
    Database.InsertDB(conn, Database.Update_userinfo_query(index.UserInfo_current_crawling_id), (target_End_ID, user_id))

    if TimeIntevalDataList is None or len(TimeIntevalDataList) == 0:
        try:
            gLine_bot_api.push_message(user_id, TextSendMessage(text="本次抓取的資料區間中無符合條件的資料。"))
        except Exception as e:
            logging.error(f"GetTodayDataSend2LINEBot empty result push error: {e}")
        return None

    content_list = []
    for data in TimeIntevalDataList:
        bubble_content = LineBotMsgHandler.RequestDataMsgText_handler(LineBotMsgHandler.RequestDataMsgText, data)
        content_list.append(bubble_content)

    try:
        for content_idx in range(0, len(content_list), index.CarsoulBubbleLimit):
            end = content_idx + index.CarsoulBubbleLimit - 1
            content_limit_list = content_list[content_idx:] if end >= len(content_list) else content_list[content_idx:end]
            Msgtext = FlexSendMessage(alt_text="Observation Data", contents=LineBotMsgHandler.MultiRequestDataMsgText(content_limit_list))
            gLine_bot_api.push_message(user_id, Msgtext)
    except Exception as e:
        logging.error(f"GetTodayDataSend2LINEBot push_message error: {e}")

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
    try:
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
    except Exception as e:
        logging.error(f"PostbackEvent handle error: {e}")

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
    pass

def Check_LN_Key_exist(userid: str):
    pass

def LN_get_token(code:str, client_id:str=index.LN_Client_ID, client_secret:str=index.LN_Client_Secret, redirect_uri:str=index.LN_redirect_uri):
    return ""

def LN_send_message(access_token:str=None, text_message:str=None, picurl:str=None):
    pass