from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, JoinEvent
import configparser
from flask import request, abort
import index
from VarIndex import *


#\ Global
#\ Line bot basic info
config = configparser.ConfigParser()
config.read('config.ini')
gLine_bot_api = LineBotApi(config.get("line-bot", "channel_access_token"))
gHandler = WebhookHandler(config.get('line-bot', 'channel_secret'))


#\ global event
gEventText = ""
gEvent = None
gEventCnt = 0

#\ message text
gIsJustText = True




#\ handler. This is the example from the official doc
def LineBotHandler(app):
    #\ get X-Line-Signature header value
    #\ 如果該HTTP POST訊息是來自LINE平台，在HTTP請求標頭中一定會包括X-Line-Signature項目，
    #\ 該項目的內容值是即為數位簽章。例如：
    signature = request.headers['X-Line-Signature']

    #\ get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(f"[INFO]{body}")

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
    global gIsJustText, gEventText, gEventCnt, gEvent
    print("[INFO]: TextMessage")
    print(f"[INFO]: {event}")

    #\ workaround for the linebot url verify error
    if event.source.user_id != "U00a49f1618f9827d4b24f140c2e5f770":

        #\ switch the case of MessageEvent

        #\ read the text if it meants to trigger some event
        if gIsJustText == True :
            gEventText = event.message.text.lower()

            #\ categorize the text to trigger event
            if gEventText == "login":
                gEvent = eLineBotEvent.LOGIN.value
                gIsJustText = False
            elif gEventText == "menu" :
                gEvent = eLineBotEvent.MENU.value
                gIsJustText = False
            else:
                pass


        #\ categorize the event and the corresponding action
        if gEvent == eLineBotEvent.LOGIN.value:
            gEventCnt += 1
            if gEventCnt == 1:
                gLine_bot_api.reply_message(event.reply_token, TextSendMessage(text=index.LoginEventText[0]))
            elif gEventCnt == 2:
                gLine_bot_api.reply_message(event.reply_token, TextSendMessage(text=index.LoginEventText[1]))
                LoginData["Account"] = event.message.text
            else:
                LoginData["Password"] = event.message.text
                Login2Web(event)
                #\ reset the is-just-text flag and the event count and event
                gIsJustText = True
                gEventCnt = 0
                gEvent = None

        elif gEvent == eLineBotEvent.MENU.value:
            pass
            #\ reset the is-just-text flag
            gIsJustText = True
        else :
            gLine_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))



#\ for the first time joining the group
@gHandler.add(JoinEvent)
def handle_message(event):
    global gEvent, gIsJustText
    gEvent = eLineBotEvent.LOGIN.value
    gIsJustText = False
    print("[INFO]: TextMessage")
    print(f"[INFO]: {event}")
    for idx in range(len(index.JoinEventText)):
        gLine_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=index.JoinEventText[idx])
                        )


#\
def Login2Web(event):
    gLine_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=f'Hi, Check again for the login info:\nAccount: {LoginData["Account"]}\nPassword: {LoginData["Password"]}'))
