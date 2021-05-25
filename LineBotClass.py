##############################
#\                          /#
#\     Line BOt Event       /#
#\                          /#
##############################
#\ This is the main function to handle the line bot e=vent

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FollowEvent, FlexSendMessage, PostbackEvent, LocationSendMessage
import configparser
from flask import request, abort
import index
from VarIndex import * #\ remeber to include this to use the cache function
import LineBotText
import DragonflyData
import Database
import datetime



#\ -- Global --
#\ Line bot basic info
config = configparser.ConfigParser()
config.read('config.ini')
gLine_bot_api = LineBotApi(config.get("line-bot", "channel_access_token"))
gHandler = WebhookHandler(config.get('line-bot', 'channel_secret'))




#\ ----------------------------------------------------------------------


#\ -- Main Function --
#\ handler. This is the example from the official doc
def LineBotHandler(app, session):
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
    if cache.get("gLoginStatus") is False:
        CheckUserInfo(event)

    #\ workaround for the linebot url verify error
    # if event.source.user_id != "U00a49f1618f9827d4b24f140c2e5f770":

    #\ Switch the case of MessageEvent
    #\ Read the text if it meants to trigger some event
    print(f'[INFO] gIsJustText : {cache.get("gIsJustText")}\n[INFO] gEvent : {cache.get("gEvent")}')
    if cache.get("gIsJustText") == True :
        cache.set("gEventText", event.message.text.lower().replace(" ", ""))

        #\ categorize the text to trigger event
        CheckEvent(cache.get("gEventText"))


    #\ Categorize the event and the corresponding action
    #\---------------------------------------------------
    if cache.get("gEvent") == eLineBotEvent.LOGIN.value:
        LoginProgress(event)


    elif cache.get("gEvent") == eLineBotEvent.MENU.value:
        if pleaseLogin(event) is True:
            #\
            #\ Add the event here
            #\
            #\ reset the is-just-text flag
            cache.set("gIsJustText", True)


    elif cache.get("gEvent") == eLineBotEvent.REQUEST.value:
        if pleaseLogin(event) is True:

            #\ main function callback
            RequestCallback(event)

            #\ reset the is-just-text flag
            cache.set("gIsJustText", True)


    elif cache.get("gEvent") == eLineBotEvent.RECORD.value:
        if pleaseLogin(event) is True:
            #\
            #\ Add the event here
            #\
            #\ reset the is-just-text flag
            cache.set("gIsJustText", True)


    elif cache.get("gEvent") == eLineBotEvent.SETTING.value:
        if pleaseLogin(event) is True:
            #\
            #\ Add the event here
            #\
            #\ reset the is-just-text flag
            cache.set("gIsJustText", True)


    elif cache.get("gEvent") == eLineBotEvent.SEARCH.value:
        if pleaseLogin(event) is True:
            #\
            #\ Add the event here
            #\
            #\ reset the is-just-text flag
            cache.set("gIsJustText", True)


    elif cache.get("gEvent") == eLineBotEvent.OTHERS.value:
        if pleaseLogin(event) is True:
            #\
            #\ Add the event here
            #\
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

    elif event_text == "request" :
        cache.set("gEvent", eLineBotEvent.REQUEST.value)
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

    elif event_text == "others" :
        cache.set("gEvent", eLineBotEvent.OTHERS.value)
        cache.set("gIsJustText", False)

    else:
        cache.set("gEvent", eLineBotEvent.NONE.value)

    print(f'[INFO] CheckEvent : {event_text}, (gIsJustText : {cache.get("gIsJustText")})')



#\ Check User Info from database to see if there are any records or not
def CheckUserInfo(event):
    DB_Data = Database.ReadFromDB(Database.CreateDBConection(),
                                    Database.Read_userinfo_query(index.UserInfoTableName, event.source.user_id),
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
    gLine_bot_api.push_message(
        event.source.user_id,
        TextSendMessage(text="Please Enter the request ID")
        )


#\ request command callback
def RequestCallback(event):

    #\ message to ask for the request ID
    AskInputID(event)

    #\ read the data from DB
    DB_Data = Database.ReadFromDB(Database.CreateDBConection(),
                                    Database.Read_userinfo_query(index.UserInfoTableName, event.source.user_id),
                                    True)
    print(f"[INFO] DB_Data: {DB_Data}")

    #\ check the return from the database is vaild or not
    if DB_Data is None:
        print("[Warning] No DB Data return, skip the requwst ID function")

    #\ login
    DragonflyData_session = Login2Web(DB_Data[4], DB_Data[5])

    #\ execute the crawler function
    [ID_find_result, overflow, Max_ID_Num] = DragonflyData.DataCrawler(DragonflyData_session, event.message.text)

    if overflow:
        print(f"[INFO] The ID is overflow, please use the ID smaller {Max_ID_Num}")
        gLine_bot_api.push_message(event.source.user_id,
                            TextSendMessage(text=f"The ID is overflow, please use the ID smaller {Max_ID_Num}")
                            )
    else:
        print(f"[INFO] Successfully craw the data")
        #\ handle the Description to align
        ID_find_result.Description = f"\n{' '*10}".join(list(ID_find_result.Description.split("\n")))
        gLine_bot_api.push_message(event.source.user_id,
                                    TextSendMessage(text=f"[IdNumber]: {ID_find_result.IdNumber}\n"+\
                                                        f"[Dates]: {ID_find_result.Dates}, {ID_find_result.Times}\n"+\
                                                        f"[City]: {ID_find_result.City} {ID_find_result.District}\n"+\
                                                        f"[Place]: {ID_find_result.Place}\n"+\
                                                        f"[Altitude]: {ID_find_result.Altitude}\n" +\
                                                        f"[User]: {ID_find_result.User}\n"+\
                                                        f"[Latitude]: {ID_find_result.Latitude}\n"+\
                                                        f"[Longitude]: {ID_find_result.Longitude}\n"\
                                                        f"[Speceis]: {', '.join(ID_find_result.SpeciesList)}\n"+\
                                                        f"[Description]: {ID_find_result.Description}\n"
                                                    )
                                    )
        #\ loaction message
        gLine_bot_api.push_message(event.source.user_id,
                                    LocationSendMessage(
                                                        title=f'# {ID_find_result.IdNumber}',
                                                        address=f'{ID_find_result.City} {ID_find_result.District} {ID_find_result.Place}',
                                                        latitude=float(ID_find_result.Latitude),
                                                        longitude=float(ID_find_result.Longitude)
                                                        )
        )




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



#\ login to web
def Login2Web(login_account:str, login_password:str)->str:
    print("[INFO] Login2Web")

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





#\Login process
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
        #\ loginconfirm
        if event.message.text == "LOGIN_CONFIRM":
            print("[INFO] Login info user confirm")
            gLine_bot_api.reply_message(
                                        event.reply_token,
                                        TextSendMessage(text="Start to Login~")
                                        )

            #\ Start Login to web method
            LoginStateMessage = Login2Web(cache.get("gAccount"), cache.get("gPassword"))
            print(f"[INFO] LoginStateMessage: {LoginStateMessage}")
            gLine_bot_api.push_message(event.source.user_id,
                                        TextSendMessage(text=LoginStateMessage)
                                        )

            #\ Store the user info if success to skip login process
            if cache.get("gLoginStatus") is True:
                #\ Connect and Create the database if not exist
                # Database.ExecuteDB(Database.CreateDBConection(), Database.UserInfo_create_table_query)

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
                                    Database.Insert_userinfo_query(index.UserInfoTableName),
                                    InsertData
                                )

        #\ Login not confirm
        elif event.message.text == "LOGIN_FAIL":
            print("[INFO] Login info user decline")
            cache.set("gEventCnt", 1)

        #\ Exit the login process
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
        LineBotText.LoginCheckText["body"]["contents"][1]["contents"][0]["contents"][1]["text"] = cache.get("gAccount")
        LineBotText.LoginCheckText["body"]["contents"][1]["contents"][1]["contents"][1]["text"] = cache.get("gPassword")

        #\ Check if the user confirm the login info
        flex_message = FlexSendMessage(alt_text=f'Hi, Check again for the login info:\nAccount: {cache.get("gAccount")}\nPassword: {cache.get("gPassword")}',
                                        contents=LineBotText.LoginCheckText
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





# #\ handle post back event
# @gHandler.add(PostbackEvent)
# def handle_postback_event(event):
#     global gLoginDataConfirm, gIsJustText, gEventCnt, gEvent
#     print("[EVENT] PostbackEvent")
#     if event.postback.data == "login_ok":
#         gLine_bot_api.reply_message(
#                 event.reply_token,
#                 TextSendMessage(text="Start to Login~")
#                 )
#         Login2Web()
#         #\ reset the is-just-text flag and the event count and event
#         gIsJustText = True
#         gEventCnt = 0
#         gEvent = None
#     elif event.postback.data == "login_fail":
#         gEventCnt = 0



