#\ this is the entry of the program

from flask import Flask, render_template, request, url_for, redirect, session
from flask_session import Session
from datetime import timedelta
import LineBotClass
import index
from VarIndex import cache
import gSheetAPI
import json


################################################################################
#\ -- Global and Init --

#\ __name__ represent the current module
app = Flask(__name__)

# Check Configuration section for more details
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

#\ secret key for session
app.secret_key = index.APP_Pri_Key
app.permanent_session_lifetime = timedelta(seconds=5)

#\ Cache for global variable
cache.init_app(app=app, config={"CACHE_TYPE": "filesystem", "CACHE_DIR":"/tmp"})

#\ Set cache data
#\ use cache.get("name") or cache.set("name", "value")
LineBotClass.InitCache(cache)



################################################################################
#\ -- App menu css setting --
#\ Remeber to update this when adding another router in the menu bar
MenuBarSetting = [
    {"url":"Home", "class":"btn", "name":"Home"},
    {"url":"About", "class":"btn", "name":"About"},
    {"url":"Weather", "class":"btn", "name":"Weather"},
    {"url":"OSMmap", "class":"btn", "name":"OSMmap"},
    {"url":"Leaflet", "class":"btn", "name":"Leaflet"}
]
Pre_Menu = 0


#\ -- APP ROUTER --
#\ Decorator 函式的裝飾:以函式為基礎,提供附加功能
@app.route("/")
def Home():
    #\ Active the menu bar
    global Pre_Menu
    L_MenuBarSetting = MenuBarSetting
    L_MenuBarSetting[Pre_Menu]["class"] = "btn"
    L_MenuBarSetting[0]["class"] = "btn-active"
    Pre_Menu = 0
    return render_template("Home.html", _MenuBarSetting=L_MenuBarSetting)


@app.route("/About", methods=["GET", "POST"])
def About():
    #\ Active the menu bar
    global Pre_Menu
    L_MenuBarSetting = MenuBarSetting
    L_MenuBarSetting[Pre_Menu]["class"] = "btn"
    L_MenuBarSetting[1]["class"] = "btn-active"
    Pre_Menu = 1

    if request.method == "POST":
        #session.permanent = True
        user = request.form['nm']
        session['user'] = user
        return redirect(url_for("user"))
    else:
        if 'user' in session:
            return redirect(url_for("user"))

        return render_template("About.html", _MenuBarSetting=L_MenuBarSetting)


@app.route("/Weather")
def Weather():
    #\ Active the menu bar
    global Pre_Menu
    L_MenuBarSetting = MenuBarSetting
    L_MenuBarSetting[Pre_Menu]["class"] = "btn"
    L_MenuBarSetting[2]["class"] = "btn-active"
    Pre_Menu = 2
    return render_template("Weather.html", _MenuBarSetting=L_MenuBarSetting)


@app.route("/OSMmap")
def OSMmap():
    #\ Active the menu bar
    global Pre_Menu
    L_MenuBarSetting = MenuBarSetting
    L_MenuBarSetting[Pre_Menu]["class"] = "btn"
    L_MenuBarSetting[3]["class"] = "btn-active"
    Pre_Menu = 3
    return render_template("OSMmap.html", apikey = index.GMAPapikey, api_on = index.bAPIon, _MenuBarSetting=L_MenuBarSetting)


@app.route("/Leaflet", methods=['GET','POST'])
def Leaflet():
    #\ Active the menu bar
    global Pre_Menu
    L_MenuBarSetting = MenuBarSetting
    L_MenuBarSetting[Pre_Menu]["class"] = "btn"
    L_MenuBarSetting[4]["class"] = "btn-active"
    Pre_Menu = 4

    #\ Handling the POST and GET method
    #\ POST
    MapData = []
    MapDataStatus = 0
    if request.method == "POST":
        print(f"request.form: {request.form}") #\ i.e. request.form: ImmutableMultiDict([('Orders', 'Damselfly'), ('Family', 'Calopterygidae'), ('Species', '01')])
        [MapDataStatus, MapData] = gSheetAPI.GetDragonflyDataGoogleSheets(request.form['Family']+request.form['Species'],
                                                         None
                                                         )
        # print(f"[INFO] MapData : {MapData}")
        print("[INFO] Leaflet router method : POST")
    else:
        print("[INFO] Leaflet router method : GET")

    return render_template("Leaflet.html",
                            _index=index,
                            _MenuBarSetting=L_MenuBarSetting,
                            _MapDataStatus=json.dumps(MapDataStatus),
                            _MapData=json.dumps(MapData)
                            )



#\ -- to HTTP method --
@app.route("/urlREST/<name>")
def urlREST(name):
    return "<h1>Hello {} !! This is urlREST example</h1>".format(name)


@app.route("/Query/")
def Query():
    name = request.args.get("name")
    text = request.args.get("text")
    return "<h1>Hello {} !! you speak {} !!! This is Query example</h1>".format(name, text)


# @app.route("/<usr>")
# def user(usr):
#     return f"<h1>{usr}<h1/>"
@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return f"<h1>{user}</h1>"
    else:
        return redirect(url_for("about"))



#\ -- Line Bot --
#\ echo
@app.route("/LineBotEcho", methods=['POST'])
def LineBotEcho():
    #\ Init the cache
    if cache.get("gIsJustText") is None:
        LineBotClass.InitCache(cache)

    #\ Check if the LINE Notify is available or not
    if cache.get("gLN_AccessToken") is None:
        body = json.loads(request.get_data(as_text=True))
        LineBotClass.Check_LN_Key_exist(body["events"][0]["source"]["userId"])

    #\ handler
    LineBotClass.LineBotHandler(app)
    return "ok"


#\ Line bot for Line Notify
@app.route("/callback/notify", methods=['GET'])
def callback_nofity():
    try:
        assert request.headers['referer'] == 'https://notify-bot.line.me/'
        code = request.args.get('code')
        state = request.args.get('state')

        # 接下來要繼續實作的函式
        access_token = LineBotClass.LN_get_token(code, index.LN_Client_ID, index.LN_Client_Secret, index.LN_redirect_uri)

        return "恭喜完成 LINE Notify 連動！請關閉此視窗。"

    except:
        return "Failed to execute the LINE Notify callback redirect URL"


#\ handle the message
# @LineBotClass.gHandler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     LineBotClass.gLine_bot_api.reply_message(
#                             event.reply_token,
#                             TextSendMessage(text=event.message.text)
#                             )y




################################################################################
#\ -- Start the server --
if __name__ == "__main__":
    #\ auto reload page
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    #\ 啟動伺服器
    app.run(debug=True)