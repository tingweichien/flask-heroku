from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FollowEvent, FlexSendMessage, PostbackEvent
import configparser
from flask import request, abort
import index
from VarIndex import *
import LineBotText



#\ Global
#\ Line bot basic info
config = configparser.ConfigParser()
config.read('config.ini')
gLine_bot_api = LineBotApi(config.get("line-bot", "channel_access_token"))
gHandler = WebhookHandler(config.get('line-bot', 'channel_secret'))






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
        gSession = session
        gHandler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'



#\ handle the message
@gHandler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    global gSession
    print("[INFO] TextMessage")
    print(f"[INFO] Event :{event}")

    #\ workaround for the linebot url verify error
    # if event.source.user_id != "U00a49f1618f9827d4b24f140c2e5f770":

    #\ switch the case of MessageEvent
    #\ read the text if it meants to trigger some event
    print(f'[INFO] gIsJustText : {cache.get("gIsJustText")}')
    print(f'[INFO] gEvent : {cache.get("gEvent")}')
    if cache.get("gIsJustText") == True :
        cache.set("gEventText", event.message.text.lower())

        #\ categorize the text to trigger event
        CheckEvent(cache.get("gEventText"))


    print(f'[INFO] gEvent(after ChekEvent) : {cache.get("gEvent")}')
    #\ categorize the event and the corresponding action
    if cache.get("gEvent") == eLineBotEvent.LOGIN.value:
        LoginProgress(event)

    elif cache.get("gEvent") == eLineBotEvent.MENU.value:
        #\ reset the is-just-text flag
        cache.set("gIsJustText", True)

    else :
        print("[EVENT] Echo")
        gLine_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))




#\ check the event from the received text
def CheckEvent(event_text:str):
    global gSession
    if event_text == "login":
        cache.set("gEvent", eLineBotEvent.LOGIN.value)
        cache.set("gIsJustText", False)
    elif event_text == "menu" :
        cache.set("gEvent", eLineBotEvent.MENU.value)
        cache.set("gIsJustText", False)
    else:
        cache.set("gEvent", eLineBotEvent.NONE.value)

    print(f'[INFO] CheckEvent : {event_text}, (gIsJustText : {cache.get("gIsJustText")})')





#\ for the first time follow the group
@gHandler.add(FollowEvent)
def handle_follow_message(event):
    cache.set("gEvent", eLineBotEvent.LOGIN.value)
    cache.set("gIsJustText", False)
    print("[INFO]: JoinEvent")
    print(f"[INFO]: {event}")
    for idx in range(len(index.JoinEventText)):
        gLine_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=index.JoinEventText[idx])
                        )



#\ login to web
def Login2Web():
    pass



#\Login process
def LoginProgress(event):
    global gSession
    tmpCnt = cache.get("gEventCnt")
    tmpCnt += 1
    cache.set("gEventCnt", tmpCnt)
    print(f'[EVENT] Login gEventCnt: {cache.get("gEventCnt")}')

    #\ specified the login event 4 to determin redo login again or not
    if cache.get("gEventCnt") == 4:
        if event.message.text == "LOGIN_CONFIRM":
            print("[INFO] Login info user confirm")
            gLine_bot_api.reply_message(
                                        event.reply_token,
                                        TextSendMessage(text="Start to Login~")
                                        )
            Login2Web()
        elif event.message.text == "LOGIN_FAIL":
            print("[INFO] Login info user decline")
            cache.set("gEventCnt", 1)

    #\ the login event
    print(f'[EVENT] Login gEventCnt(after gEventCnt 4): {cache.get("gEventCnt")}')
    if cache.get("gEventCnt") == 1:
        gLine_bot_api.reply_message(event.reply_token, TextSendMessage(text=index.LoginEventText[0]))
    elif cache.get("gEventCnt") == 2:
        gLine_bot_api.reply_message(event.reply_token, TextSendMessage(text=index.LoginEventText[1]))

        #\ assign the account
        gLoginData["Account"] = event.message.text

    elif cache.get("gEventCnt") == 3:
        #\ assign the password
        gLoginData["Password"] = event.message.text

        #\ Text to print on Flex message for re-checking the user login info
        LineBotText.LoginCheckText["body"]["contents"][1]["contents"][0]["contents"][1]["text"] = gLoginData["Account"]
        LineBotText.LoginCheckText["body"]["contents"][1]["contents"][1]["contents"][1]["text"] = gLoginData["Password"]

        #\ Check if the user confirm the login info
        flex_message = FlexSendMessage(alt_text=f'Hi, Check again for the login info:\nAccount: {gLoginData["Account"]}\nPassword: {gLoginData["Password"]}',
                                        contents=LineBotText.LoginCheckText
                                        )
        gLine_bot_api.reply_message(
                        event.reply_token,
                        flex_message
                        )
    else:
        #\ reset the is-just-text flag and the event count and event
        print("[INFO] RESET~~~~~~~~~")
        cache.set("gIsJustText", True)
        cache.set("gEventCnt", 0)
        cache.set("gEvent", None)





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


