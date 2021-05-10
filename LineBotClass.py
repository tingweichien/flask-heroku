from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import configparser
from flask import Flask, request, abort

#\ Global
gHandler = None

class LineBotClass():
    #\ -- CONSTRUCTOR --
    def __init__(self, app:Flask):
        #\ Line bot basic info
        global gHandler
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.Line_bot_api = LineBotApi(self.config.get("line-bot", "channel_access_token"))
        self.handler = WebhookHandler(self.config.get('line-bot', 'channel_secret'))
        gHandler = self.handler
        self.app = app

    #\ -- METHOD --

    #\ Echo what you send. This is the example from the official doc
    def echo(self):
        #\ get X-Line-Signature header value
        #\ 如果該HTTP POST訊息是來自LINE平台，在HTTP請求標頭中一定會包括X-Line-Signature項目，
        #\ 該項目的內容值是即為數位簽章。例如：
        signature = request.headers['X-Line-Signature']

        #\ get request body as text
        body = request.get_data(as_text=True)
        self.app.logger.info("Request body: " + body)

        #\ handle webhook body
        try:
            gHandler.handle(body, signature)
        except InvalidSignatureError:
            print("Invalid signature. Please check your channel access token/channel secret.")
            abort(400)

        return 'OK'


    #\ handle the message
    @gHandler.add(MessageEvent, message=TextMessage)
    def handle_message(self, event):
        self.Line_bot_api.reply_message(
                                        event.reply_token,
                                        TextSendMessage(text=event.message.text)
                                        )