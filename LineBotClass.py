##############################
#\                          /#
#\     Line BOt Event       /#
#\                          /#
##############################
#\ This is the main function to handle the line bot e=vent

from typing import List
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FollowEvent, FlexSendMessage, PostbackEvent, LocationSendMessage, flex_message
import configparser
from flask import request, abort
import index
from VarIndex import * #\ remeber to include this to use the cache function
import LineBotMsgHandler
import DragonflyData
import Database
import datetime
import LineBotMsgHandler
import random
from gSheetAPI import Sheet_id_dict
import urllib
import urllib.request, urllib.parse
import json
import yaml


#\ -- Global --
#\ Line bot basic info
config = configparser.ConfigParser()
config.read('./Key/config.ini')
gLine_bot_api = LineBotApi(config.get("line-bot", "channel_access_token"))
gHandler = WebhookHandler(config.get('line-bot', 'channel_secret'))




#\ ----------------------------------------------------------------------


#\ -- Main Function --
#\ handler. This is the example from the official doc
def LineBotHandler(app):
    #\ get X-Line-Signature header value
    #\ 如果該HTTP POST訊息是來自LINE平台，在HTTP請求標頭中一定會包括X-Line-Signature項目，
    #\ 該項目的內容值是即為數位簽章。例如：
    print("[INFO]LineBotHandler")
    signature = request.headers['X-Line-Signature']

    #\ get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(f"[INFO] body-->{body}")

    #\ handle webhook body
    try:
        gHandler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'



#\ handle the message
@gHandler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    print(f"[INFO] TextMessage\n[INFO] Event :{event}")

    #\ Check if there are user info store in the database, if True, then skip the login check
    print(f'[INFO] gIsJustText : {cache.get("gIsJustText")}\n[INFO] gEvent : {cache.get("gEvent")}\n[INFO] gLoginStatus: {cache.get("gLoginStatus")}')
    if cache.get("gLoginStatus") is False :
        #\ If the user info had been created
        if CheckUserInfo(event) is True:
            gLine_bot_api.link_rich_menu_to_user(event.source.user_id, cache.get("RichMenuID")["Main Richmenu"])

    #\ workaround for the linebot url verify error
    # if event.source.user_id != "U00a49f1618f9827d4b24f140c2e5f770":

    #\ Switch the case of MessageEvent
    #\ Read the text if it meants to trigger some event
    if cache.get("gIsJustText") == True :
        cache.set("gEventText", event.message.text.lower().replace(" ", ""))

        #\ categorize the text to trigger event
        CheckEvent(cache.get("gEventText"))


    #\ Categorize the event and the corresponding action
    #\---------------------------------------------------
    if cache.get("gEvent") == eLineBotEvent.LOGIN.value:
        #\ Check if there are user info store in the database, if True, then skip the login check
        #\ If the user info had been created
        if cache.get("gLoginStatus") is True :
            gLine_bot_api.reply_message(event.reply_token, TextSendMessage(text="Already Login"))
            gLine_bot_api.link_rich_menu_to_user(event.source.user_id, cache.get("RichMenuID")["Main Richmenu"])
            cache.set("gIsJustText", True)

        #\ The user info havn't been created, then start the login process
        else :
            LoginProgress(event)


    elif cache.get("gEvent") == eLineBotEvent.MENU.value:
        if pleaseLogin(event) is True :
            #\
            #\ Add the event here
            #\
            #\ reset the is-just-text flag
            cache.set("gIsJustText", True)


    elif cache.get("gEvent") == eLineBotEvent.IDREQUEST.value:
        if pleaseLogin(event) is True :

            #\ main function callback
            IDRequestfinish = IDRequestCallback(event)

            #\ reset the is-just-text flag
            if IDRequestfinish is True:
                cache.set("gIsJustText", True)


    elif cache.get("gEvent") == eLineBotEvent.RECORD.value:
        if pleaseLogin(event) is True :
            #\
            #\ Add the event here
            #\
            #\ reset the is-just-text flag
            cache.set("gIsJustText", True)


    elif cache.get("gEvent") == eLineBotEvent.SETTING.value:
        if pleaseLogin(event) is True :
            #\
            #\ Add the event here
            #\
            #\ reset the is-just-text flag
            cache.set("gIsJustText", True)


    elif cache.get("gEvent") == eLineBotEvent.SEARCH.value:
        if pleaseLogin(event) is True :
            search_flex_message = FlexSendMessage(alt_text="Please type IDRequest or Advance Search",
                                                  contents=LineBotMsgHandler.Search_event_text
                                                  )
            gLine_bot_api.reply_message(event.reply_token,
                                        search_flex_message
                                        )
            #\ reset the is-just-text flag
            cache.set("gIsJustText", True)


    elif cache.get("gEvent") == eLineBotEvent.TODAYDATA.value:
        if pleaseLogin(event) is True :

            #\ Get today's data
            index.Hourly_Summary_default_data_filter[1] = index.Species_rare_rank_first_60.copy()
            GetTodayDataSend2LINEBot(event.source.user_id,
                                     event.reply_token,
                                     True,
                                     index.Hourly_Summary_default_data_filter
                                     )

            #\ reset the is-just-text flag
            cache.set("gIsJustText", True)

    else :
        print("[EVENT] Echo")
        cache.set("gEvent", eLineBotEvent.NONE.value)
        gLine_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))






#\ Check the event from the received text
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

    print(f'[INFO] CheckEvent : {event_text}, (gIsJustText : {cache.get("gIsJustText")})')



#\ Check User Info from database to see if there are any records or not
def CheckUserInfo(event):
    DB_Data = Database.ReadFromDB(Database.CreateDBConection(),
                                    Database.Read_userinfo_query(event.source.user_id),
                                    True)
    print(f"[INFO] In the CkeckUserInfo() the Data return from the DB is {DB_Data}")
    if DB_Data is not None:
        cache.set("gLoginStatus", True)
        print("[INFO] The User has user info data store in the database")
        return True
    else :
        print("[INFO] The User has no user info data store in the database")
        return False



#\ When richmenu event been triggerred, check if the login state vaild
def pleaseLogin(event):
    if cache.get("gLoginStatus") is not True:
        gLine_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Please Login first to use this function")
                )
        return False
    else:
        return True



#\ Ask the input ID for request
def AskInputID(event):
    gLine_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="Please Enter the request ID")
        )


#\ request command callback, when type or push "request" button
def IDRequestCallback(event):

    tmpCnt = cache.get("gEventCnt")
    tmpCnt += 1
    cache.set("gEventCnt", tmpCnt)
    if tmpCnt == 1:

        #\ message to ask for the request ID
        AskInputID(event)
        return False

    elif tmpCnt == 2:
        #\ Get the dragonfly request session
        DragonflyData_session, _ = CreateWebSession(event)

        #\ execute the crawler function
        try :
            IDNumber = int(event.message.text)
        except:
            gLine_bot_api.reply_message(event.reply_token, "Input ID number is not integer !!!!!!!!!!!")
            print("[Warning] Input ID number is not integer")
            cache.set("gEventCnt", 0)
            return False

        [ID_find_result, overflow, Max_ID_Num] = DragonflyData.DataCrawler(DragonflyData_session, IDNumber)

        if overflow:
            print(f"[INFO] The ID is overflow, please use the ID smaller {Max_ID_Num}")
            gLine_bot_api.reply_message(event.reply_token,
                                TextSendMessage(text=f"The ID is overflow, please use the ID smaller {Max_ID_Num}")
                                )
        else:
            print(f"[INFO] Successfully craw the data")
            #\ handle the Description to align
            if ID_find_result.Description is not None:
                ID_find_result.Description = f"\n{' '*10}".join(list(ID_find_result.Description.split("\n")))
            # gLine_bot_api.push_message(event.source.user_id,
            #                             TextSendMessage(text=f"[IdNumber]: {ID_find_result.IdNumber}\n"+\
            #                                                 f"[Dates]: {ID_find_result.Dates}, {ID_find_result.Times}\n"+\
            #                                                 f"[City]: {ID_find_result.City} {ID_find_result.District}\n"+\
            #                                                 f"[Place]: {ID_find_result.Place}\n"+\
            #                                                 f"[Altitude]: {ID_find_result.Altitude}\n" +\
            #                                                 f"[User]: {ID_find_result.User}\n"+\
            #                                                 f"[Latitude]: {ID_find_result.Latitude}\n"+\
            #                                                 f"[Longitude]: {ID_find_result.Longitude}\n"\
            #                                                 f"[Speceis]: {', '.join(ID_find_result.SpeciesList)}\n"+\
            #                                                 f"[Description]: {ID_find_result.Description}\n",
            #                                             wrap = True
            #                                             )
            #                             )
            #\ Flex message template
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

            gLine_bot_api.reply_message(event.reply_token,
                                       RequestDataText
                                        )

            #\ loaction message
            gLine_bot_api.push_message(event.source.user_id,
                                        LocationSendMessage(title=f'# {ID_find_result.IdNumber}',
                                                            address=f'{ID_find_result.City} {ID_find_result.District} {ID_find_result.Place}',
                                                            latitude=float(ID_find_result.Latitude),
                                                            longitude=float(ID_find_result.Longitude)
                                                            )
                                        )


        #\ reset the counter
        cache.set("gEventCnt", 0)
        return True


#\ create web session
def CreateWebSession(event=None, CloseDBConn=True):
    """
    params :
        event: to get the user info based on user id, if None, then fetchall
        CloseDBConn: default True to close DB connection after it.
    return:
        session
        conn
    """
    if event is not None:
        read_query = Database.Read_userinfo_query(event.source.user_id)
        fetchone = True
    else:
        read_query = Database.Read_all_query(index.UserInfoTableName)
        fetchone = False
    print(f"[INFO] in CrateWebSession read query : {read_query}")

    #\ read the data from DB
    conn = Database.CreateDBConection()
    if conn is None:
        print("[Warming] Fail to do CreateWebSession() due to the CreateDBConnection() fail")
        return None, None

    DB_Data = Database.ReadFromDB(conn,
                                    read_query,
                                    fetchone,
                                    CloseDBConn
                                    )
    # print(f"[INFO] DB_Data: {DB_Data}")

    #\ check the return from the database is vaild or not
    if DB_Data is None:
        print("[Warning] No DB Data return, skip the requwst ID function")

    #\ handle the account and password read from the database with fetchone and fetchall
    if event is not None and fetchone is True:
        ACC, PW = DB_Data[4], DB_Data[5]
    else:
        idx = random.randint(0, len(DB_Data)-1)
        ACC, PW = DB_Data[idx][4], DB_Data[idx][5]
    # print(f"[INFO] ACC :{ACC}, PW :{PW}")

    #\ return session
    [session, _, Login_state] = DragonflyData.Login_Web(ACC, PW)
    if Login_state is False:
        print("[Warning] In CreateWebSession() Login_state is False")
        return None, None
    else:
        print("[INFO] In CreateWebSession() successfully login")
        return session, conn




#\ for the first time follow the group
@gHandler.add(FollowEvent)
def handle_follow_message(event):
    # cache.set("gEvent", eLineBotEvent.LOGIN.value)
    # cache.set("gIsJustText", False)
    print("[INFO]: JoinEvent")
    for idx in range(len(index.JoinEventText)):
        gLine_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=index.JoinEventText[idx])
                        )

    #\ re intialize the cache
    InitCache(cache)

    #\Set the richmenu
    OEMSetDefaultRichmenu(gLine_bot_api, event)



#\ login to web
def LineBotLogin2Web(login_account:str, login_password:str)->str:
    print("[INFO] LineBotLogin2Web")

    #\ Get the login PW and ACCOUNT
    print(f'[INFO] Account: {login_account}, Password: {login_password}')

    #\ Main function to login
    [Dragonfly_session, Login_Response, Login_state] = DragonflyData.Login_Web(login_account, login_password)
    print(f"[INFO] Login_Response: {Login_Response}, Login_state: {Login_state}")

    #\ Check the login state
    if (Login_state == False):
        print("[Warning] Warning!!! Account or Password might be incorrect!!!!")  #incorrect account or password
        return "Account or Password might be incorrect!!!!"

    elif Login_Response == None and Login_state == None:
        print("[Warning] No connection to server, check the internet connection!!!")
        return " No connection to server, check the internet connection!!!"

    else: #\ Login_state == True and Login_Response not None
        print("[info] Login state success")

        #\ Function finish state
        cache.set("gLoginStatus", True)

        #\ Set the login session
        cache.set("Dragonfly_session", Dragonfly_session)

        return "Login state success~"





#\ Login process
def LoginProgress(event):

    #\ handle the event count
    if cache.get("gEventCnt") == None:
        tmpCnt = 0
    else :
        tmpCnt = cache.get("gEventCnt")

    #\ Increase the event count
    tmpCnt += 1
    cache.set("gEventCnt", tmpCnt)
    print(f'[EVENT] Login gEventCnt: {cache.get("gEventCnt")}')


    #\\\\\\\ The login event \\\\\\\\
    #\ -- gEventCnt = 4 --
    #\ specified the login event 4 to determin redo login again or not
    if cache.get("gEventCnt") == 4:
        #\ Button loginc onfirm
        if event.message.text == "LOGIN_CONFIRM":
            print("[INFO] Login info user confirm")
            gLine_bot_api.reply_message(
                                        event.reply_token,
                                        TextSendMessage(text="Start to Login~")
                                        )

            #\ Start Login to web method
            LoginStateMessage = LineBotLogin2Web(cache.get("gAccount"), cache.get("gPassword"))
            print(f"[INFO] LoginStateMessage: {LoginStateMessage}")
            gLine_bot_api.push_message(event.source.user_id,
                                        TextSendMessage(text=LoginStateMessage)
                                        )

            #\ Login Success
            #\ Store the user info if success to skip login process
            if cache.get("gLoginStatus") is True:
                #\ Connect and Create the database if not exist
                if index.CreateDataBase:
                    Database.ExecuteDB(Database.CreateDBConection(), Database.UserInfo_create_table_query)

                #\ Request the user info
                #\      self.display_name = display_name
                #\      self.user_id = user_id
                #\      self.picture_url = picture_url
                #\      self.status_message = status_message
                #\      self.language = language
                request_userinfo = gLine_bot_api.get_profile(event.source.user_id)

                #\ Data to input
                InsertData = (
                    request_userinfo.display_name,
                    event.source.user_id,
                    datetime.datetime.now().strftime("%Y-%m-%d"),
                    cache.get("gAccount"),
                    cache.get("gPassword")
                )

                #\ Save the PW and ACCOUNT to the database
                Database.InsertDB(Database.CreateDBConection(),
                                    Database.Insert_userinfo_query(),
                                    InsertData
                                )

                #\ Set the default richmenu
                gLine_bot_api.link_rich_menu_to_user(event.source.user_id, cache.get("RichMenuID")["Main Richmenu"])


        #\ Button Login not confirm
        elif event.message.text == "LOGIN_FAIL":
            print("[INFO] Login info user decline")
            cache.set("gEventCnt", 1)

        #\ Button Exit the login process
        elif event.message.text == "LOGIN_EXIT":
            print("[INFO] Exit login")
            cache.set("gEventCnt", 0)


    #\ -- gEventCnt = 1 --
    if cache.get("gEventCnt") == 1:
        gLine_bot_api.reply_message(event.reply_token, TextSendMessage(text=index.LoginEventText[0]))

    #\ -- gEventCnt = 2 --
    elif cache.get("gEventCnt") == 2:
        gLine_bot_api.reply_message(event.reply_token, TextSendMessage(text=index.LoginEventText[1]))

        #\ assign the account
        # gLoginData["Account"] = event.message.text
        cache.set("gAccount", event.message.text)

    #\ -- gEventCnt = 3 --
    elif cache.get("gEventCnt") == 3:
        #\ assign the password
        # gLoginData["Password"] = event.message.text
        cache.set("gPassword", event.message.text)

        #\ Text to print on Flex message for re-checking the user login info
        LineBotMsgHandler.LoginCheckText["body"]["contents"][1]["contents"][0]["contents"][1]["text"] = cache.get("gAccount")
        LineBotMsgHandler.LoginCheckText["body"]["contents"][1]["contents"][1]["contents"][1]["text"] = cache.get("gPassword")

        #\ Check if the user confirm the login info
        flex_message = FlexSendMessage(alt_text=f'Hi, Check again for the login info:\nAccount: {cache.get("gAccount")}\nPassword: {cache.get("gPassword")}',
                                        contents=LineBotMsgHandler.LoginCheckText
                                        )
        gLine_bot_api.reply_message(
                        event.reply_token,
                        flex_message
                        )

    #\ -- gEventCnt = else --
    else:
        #\ reset the is-just-text flag and the event count and event
        print("[INFO] RESET event data~~~~~~~~~")
        cache.set("gIsJustText", True)
        cache.set("gEventCnt", 0)
        cache.set("gEvent", eLineBotEvent.NONE.value)



#\ Set default richmenu
def OEMSetDefaultRichmenu(linebot_api, event):
    LoginState = CheckUserInfo(event)
    LineBotMsgHandler.DefaultRichMenu(linebot_api, LoginState)


#\ Callback for today's Data
def GetTodayDataSend2LINEBot(user_id:str=None, reply_token:str=None, AllDayData:bool=True, filter:List=index.DefaultFilterObject, conn=None, DragonflyData_session=None):
    """Callback for today's Data or data in certain time period(control by AllDayData) and apply the filter if needed
    Args:
        user_id (str, optional) : [description]. Defaults to None.
        reply_token (str, optional) : This is for rely function, you can choose whether you want to use or not. Defaults to None.
        AllDayData (bool, optional) : Whether to get all the data in this day or do the seperate. If this set to false, then the data return will
                                     be based on the current_crawling_id. The current_crawling_id will be updated after that and so does the daily update.
                                     Defaults to True.
        filter (list of list, optional): Filter to filter out the data you want. Defaults to index.DefaultFilterObject.
    """
    #\ Check the input args
    if user_id is None:
        print("[Error] In GetTodayDataSend2LINEBot() No user id been specify")
        return

    if reply_token is not None:
        gLine_bot_api.reply_message(reply_token,
                                    TextSendMessage(text="Please be patient, it might take a while~~")
                                    )

    #\ Check the web session
    if DragonflyData_session is None:
        DragonflyData_session, conn = CreateWebSession(CloseDBConn=False)

    #\ --- Get all the data today ---
    #\ ------------------------------------------------------------------------
    if AllDayData is True:
        TimeIntevalDataList = DragonflyData.CrawTodayData(DragonflyData_session,
                                                          int(cache.get("DataBaseVariable")["LatestDataID"]),
                                                          filter
                                                          )

    #\ --- Get the specific time interval data based on current_crawling_id ---
    #\ ------------------------------------------------------------------------
    else :
        #\ Get the data for certain time interval
        current_crawling_id_tmp = Database.ReadFromDB(conn,
                                                      Database.Read_col_userinfo_query("current_crawling_id", user_id),
                                                      True,
                                                      False
                                                      )[0]

        #\ Get the latest ID
        Latest_ID = DragonflyData.GetMaxID(DragonflyData_session)

        #\ Check if the current crawling data is None or not
        if current_crawling_id_tmp is not None:
            current_cawling_ID = current_crawling_id_tmp

        elif current_crawling_id_tmp is None and Latest_ID is not None:
            current_cawling_ID = Latest_ID
            #\ Update the current crawling data
            Database.InsertDB(  conn,
                                Database.Update_userinfo_query(index.UserInfo_current_crawling_id),
                                (Latest_ID, user_id)
                             )

            #\ Save the CCID(Current Crawling ID) to datbase
            print("[INFO] Update the current crawling ID to the database since there is no current crawling ID")
            Database.InsertDB(conn,
                              Database.Update_userinfo_query(index.UserInfo_current_crawling_id),
                              (current_cawling_ID, user_id)
                              )
            #\ Since the current latest ID is equal to the current crawling ID so there will be no data to upate, return this function
            return None

        else:
            print("[Warning] In GetTodayDataSend2LINEBot() both current_crawling_id_tmp and Latest_ID read from the database are None,\
                    please check the database query execution")
            return None


        #\ Get the data
        TimeIntevalDataList = DragonflyData.CrawlDataByIDRange(DragonflyData_session,
                                                            int(current_cawling_ID),
                                                            int(Latest_ID),
                                                            filter
                                                            )


        #\ Update the current ID and save the CCID(Current Crawling ID) to datbase
        Database.InsertDB(conn,
                        Database.Update_userinfo_query(index.UserInfo_current_crawling_id),
                        (Latest_ID, user_id)
                        )
        print(f"[INFO] Update the current crawling ID to the database: {Latest_ID}")


        #\ return in the returned data list is None
        if len(TimeIntevalDataList) is 0:
            print("[INFO] In GetTodayDataSend2LINEBot() No data need to update")
            return None

    #\ ------------------------------------------------------------------------


    #\ Handling the data for the bubble in the carsoul message
    content_list = []
    for data in TimeIntevalDataList:
        bubble_content = LineBotMsgHandler.RequestDataMsgText_handler(LineBotMsgHandler.RequestDataMsgText, data)
        content_list.append(bubble_content)


    #\ Handling the carsoul text message with limitation number by LINE API
    # print(f"[INFO] in GetTodayDataSend2LINEBot() content list\n{content_list}")
    if len(content_list) is 0:
        print("[INFO] In GetTodayDataSend2LINEBot() No data need to update")
        gLine_bot_api.push_message(user_id,
                        TextSendMessage(text="No data updated today")
                        )
    else:
        for content_idx in range(0, len(content_list), index.CarsoulBubbleLimit):
            end = content_idx + index.CarsoulBubbleLimit - 1
            #\ handle overflow
            if end >= len(content_list):
                content_limit_list = content_list[content_idx:]
            else:
                content_limit_list = content_list[content_idx:end]

            Msgtext = FlexSendMessage(alt_text="No data",
                                    contents=LineBotMsgHandler.MultiRequestDataMsgText(content_limit_list)
                                    )

            gLine_bot_api.push_message(user_id,
                                    Msgtext
                                    )



#\ Init the cache data
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
    _cache.set("RichMenuID", LineBotMsgHandler.Get_RichMenu(gLine_bot_api))
    _cache.set("DataBaseVariable", dict((Database.ReadFromDB(Database.CreateDBConection(),
                                                            Database.Read_all_query(index.VariableTableName),
                                                            False)
                                        ))
               )
    _cache.set("DAYAlarm", index.DAYAlarm)
    _cache.set("gGSheetList", Sheet_id_dict())
    _cache.set("gLN_AccessToken", None)



#\ handle post back event
@gHandler.add(PostbackEvent)
def handle_postback_event(event):
    PostbackEvent = CheckPostEvent(event.postback.data.lower().replace(" ", ""))

    #\ Go to second main richmenu
    if PostbackEvent == eLineBotPostEvent.OTHERS.value:
        gLine_bot_api.link_rich_menu_to_user(event.source.user_id,cache.get("RichMenuID")["Main2 Richmenu"])
        print("[INFO] Switch to the Main2 Richmenu")

    elif PostbackEvent == eLineBotPostEvent.GOBACKMAIN.value:
        gLine_bot_api.link_rich_menu_to_user(event.source.user_id,cache.get("RichMenuID")["Main Richmenu"])
        print("[INFO] Go back to the Main Richmenu")

    elif PostbackEvent == eLineBotPostEvent.SHOWONMAP.value:
        [ID, Addr, Lat, Lng] = PostbackEvent.split("_")[1:]
        print("[INFO] In the POST back event, the ID: {ID}, Addr: {Addr}, Lat: {Lat}, Lng: {Lng}")
        if Lat and Lng is not None:
            gLine_bot_api.push_message(event.source.user_id,
                                        LocationSendMessage(title=f'# {ID}',
                                                            address=Addr,
                                                            latitude=float(Lat),
                                                            longitude=float(Lng)
                                                            )
                                        )
        print("[INFO] Show the address on the map")

    else :
        print("[INFO] No POST event been dpecified")


#\ Check the post event
def CheckPostEvent(event_text:str):
    if event_text == "others":
        return eLineBotPostEvent.OTHERS.value

    elif event_text == "gobackmain":
        return eLineBotPostEvent.GOBACKMAIN.value

    elif event_text.split("_")[0] == "ShoWOnMap":
        return eLineBotPostEvent.SHOWONMAP.value

    else:
        return eLineBotPostEvent.NONE.value



#\ ------------------------------------------------------------------------------------------------
#\ --- Line Bot for Line Notify ---
#\ send this url to the user to get the access token
def create_auth_link(user_id, client_id=index.LN_Client_ID, redirect_uri=index.LN_redirect_uri):
    print("[LINE Notify] Request the user to authorize the LINE Notify")
    data = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': 'notify',
        'state': user_id
    }
    query_str = urllib.parse.urlencode(data)

    #\ return f'https://notify-bot.line.me/oauth/authorize?{query_str}'
    gLine_bot_api.push_message(user_id,
                                TextSendMessage(text=f"Please click the following link to authorize the LINE Notify, select \"1-on-1 chat with LINE Notify\"\nhttps://notify-bot.line.me/oauth/authorize?{query_str}")
                                )


#\ Check if the LINE Notify key already exit or not
def Check_LN_Key_exist(userid: str):
    #\ read the database
    Userinfo_access_token = Database.ReadFromDB(Database.CreateDBConection(),
                                                Database.Read_col_userinfo_query("access_token", userid),
                                                True
                                                )

    #\ Set the User ID to cache
    cache.set("gUserID", userid)

    print(f"[Info] In Check_LN_Key_exist() the access token is {Userinfo_access_token}")
    if Userinfo_access_token[0] is None:
        print("[Info] Updating the LINE Notify access token")
        #\ Send the link to the user to authorize and get the access token
        #\ After the user click authorize, it'll redirect to the callback_nofity() in app.py
        #\ the code can be got, then can start to ask the LINE Notify for the access token
        create_auth_link(userid)
    else:
        cache.set("gLN_AccessToken", Userinfo_access_token)




#\ Get the token
def LN_get_token(code:str, client_id:str=index.LN_Client_ID, client_secret:str=index.LN_Client_Secret, redirect_uri:str=index.LN_redirect_uri):
    """Get the token from the user to access the LIne Notify message

    Args:
        code (str): The code that get after user click authorize
        client_id (str, optional): Put the user ID here and it'll return the corresponding access token back. Defaults to index.LN_Client_ID.
        client_secret (str, optional): . Defaults to index.LN_Client_Secret.
        redirect_uri (str, optional): . Defaults to index.LN_redirect_uri.

    Returns:
        str: access token
    """
    print("[LINE Notify] Get Token")
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

    #res = json.loads(page.decode('utf-8'))
    #\ Use the yaml loads to fix the unicode output by json.loads
    res = yaml.safe_load(page)


    #\ Save the token to the database
    Database.InsertDB(Database.CreateDBConection(),
                      Database.Update_userinfo_query("access_token"),
                      (res['access_token'], cache.get("gUserID")))
    #\ Set to the cache
    cache.set("gLN_AccessToken", res['access_token'])
    print(f"[LINE Notify] Access Token : {res['access_token']}")
    return res['access_token']


###########################################################################################
#\ Use this to send the message via LINE Notify, but the message will not show in your APP.
#\ Send the message
def LN_send_message(access_token:str=None, text_message:str=None, picurl:str=None):
    """Send the message using LINE Notify

    Args:
        access_token (str, optional): [Access token for the LINE Notify]. Defaults to None.
        text_message (str, optional): [test message to sen]. Defaults to None.
        picurl (str, optional): [piecture url]. Defaults to None.
    """
    print("[LINE Notify] Send message")

    #\ Handle the access token and check the input data vaildation
    if access_token is None:
        print("[Warning][LINE Notify] access token is None")
        return
    else:
        url = 'https://notify-api.line.me/api/notify'
        headers = {"Authorization": "Bearer "+ access_token}

    #\ The LINE Notify required the text message no matter whether the picture url is specify or not
    if text_message is None:
        print("[Warning][LINE Notify] Not specify the mandatory text message to send")
        return

    DataToSend = dict()
    DataToSend = {'message': text_message}
    if picurl is not None:
        temp_data = {"stickerPackageId": 2, 'stickerId': 38,
                    'imageThumbnail':picurl, 'imageFullsize':picurl}
        DataToSend.update(temp_data)


    # data = {'message': text_message,
    #         "stickerPackageId": 2, 'stickerId': 38,
    #         'imageThumbnail':picurl, 'imageFullsize':picurl}

    data = urllib.parse.urlencode(DataToSend).encode()
    req = urllib.request.Request(url, data=data, headers=headers)
    page = urllib.request.urlopen(req).read()
    ###########################################################################################