#\ this is the entry of the program
import os
import requests
from flask import Flask, render_template, request, url_for, redirect, session
from flask_session import Session
from datetime import timedelta
import LineBotClass
import index
from VarIndex import cache
import gSheetAPI
import json
import logging

################################################################################
#\ -- Global and Init --

app = Flask(__name__)

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

app.secret_key = index.APP_Pri_Key
app.permanent_session_lifetime = timedelta(seconds=5)

cache.init_app(app=app, config={"CACHE_TYPE": "filesystem", "CACHE_DIR":"/tmp"})

#\ Set cache data
LineBotClass.InitCache(cache)

#\ --- 平台開關設定 (透過 Render 環境變數讀取) ---
USE_LINE = os.environ.get('USE_LINE', 'True').lower() == 'true'
USE_TELEGRAM = os.environ.get('USE_TELEGRAM', 'False').lower() == 'true'
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')

################################################################################
#\ -- App menu css setting --
MenuBarSetting = [
    {"url":"Home", "class":"btn", "name":"Home"},
    {"url":"About", "class":"btn", "name":"About"},
    {"url":"Weather", "class":"btn", "name":"Weather"},
    {"url":"OSMmap", "class":"btn", "name":"OSMmap"},
    {"url":"Leaflet", "class":"btn", "name":"Leaflet"}
]
Pre_Menu = 0

#\ -- APP ROUTER --
@app.route("/")
def Home():
    global Pre_Menu
    L_MenuBarSetting = MenuBarSetting
    L_MenuBarSetting[Pre_Menu]["class"] = "btn"
    L_MenuBarSetting[0]["class"] = "btn-active"
    Pre_Menu = 0
    return render_template("Home.html", _MenuBarSetting=L_MenuBarSetting)

@app.route("/About", methods=["GET", "POST"])
def About():
    global Pre_Menu
    L_MenuBarSetting = MenuBarSetting
    L_MenuBarSetting[Pre_Menu]["class"] = "btn"
    L_MenuBarSetting[1]["class"] = "btn-active"
    Pre_Menu = 1

    if request.method == "POST":
        user = request.form['nm']
        session['user'] = user
        return redirect(url_for("user"))
    else:
        if 'user' in session:
            return redirect(url_for("user"))
        return render_template("About.html", _MenuBarSetting=L_MenuBarSetting)

@app.route("/Weather")
def Weather():
    global Pre_Menu
    L_MenuBarSetting = MenuBarSetting
    L_MenuBarSetting[Pre_Menu]["class"] = "btn"
    L_MenuBarSetting[2]["class"] = "btn-active"
    Pre_Menu = 2
    return render_template("Weather.html", _MenuBarSetting=L_MenuBarSetting)

@app.route("/OSMmap")
def OSMmap():
    global Pre_Menu
    L_MenuBarSetting = MenuBarSetting
    L_MenuBarSetting[Pre_Menu]["class"] = "btn"
    L_MenuBarSetting[3]["class"] = "btn-active"
    Pre_Menu = 3
    return render_template("OSMmap.html", apikey = index.GMAPapikey, api_on = index.bAPIon, _MenuBarSetting=L_MenuBarSetting)

@app.route("/Leaflet", methods=['GET','POST'])
def Leaflet():
    global Pre_Menu
    L_MenuBarSetting = MenuBarSetting
    L_MenuBarSetting[Pre_Menu]["class"] = "btn"
    L_MenuBarSetting[4]["class"] = "btn-active"
    Pre_Menu = 4

    MapData = []
    MapDataStatus = 0
    if request.method == "POST":
        [MapDataStatus, MapData] = gSheetAPI.GetDragonflyDataGoogleSheets(request.form['Family']+request.form['Species'], None)
    
    return render_template("Leaflet.html",
                            _index=index,
                            _MenuBarSetting=L_MenuBarSetting,
                            _MapDataStatus=json.dumps(MapDataStatus),
                            _MapData=json.dumps(MapData)
                            )

@app.route("/urlREST/<name>")
def urlREST(name):
    return "<h1>Hello {} !! This is urlREST example</h1>".format(name)

@app.route("/Query/")
def Query():
    name = request.args.get("name")
    text = request.args.get("text")
    return "<h1>Hello {} !! you speak {} !!! This is Query example</h1>".format(name, text)

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return f"<h1>{user}</h1>"
    else:
        return redirect(url_for("About"))

#\ -- Line Bot --
@app.route("/LineBotEcho", methods=['POST'])
def LineBotEcho():
    if not USE_LINE:
        return "LINE is disabled", 200

    if cache.get("gIsJustText") is None:
        LineBotClass.InitCache(cache)

    body_text = request.get_data(as_text=True)
    body = json.loads(body_text)

    if len(body.get("events", [])) == 0:
        return "ok", 200

    LineBotClass.LineBotHandler(app)
    return "ok"

@app.route("/callback/notify", methods=['GET'])
def callback_nofity():
    return "LINE Notify function is currently disabled.", 200

#\ -- Telegram Bot --
@app.route('/TelegramWebhook', methods=['POST'])
def TelegramWebhook():
    if not USE_TELEGRAM:
        return "Telegram is disabled", 200

    update = request.get_json()
    if "message" in update and "text" in update["message"]:
        chat_id = update["message"]["chat"]["id"]
        user_text = update["message"]["text"]

        reply_text = f"你傳送了: {user_text}\n(Telegram Bot 正常運作中！)"
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": chat_id, "text": reply_text}
        requests.post(url, json=payload)

    return "OK", 200

################################################################################
#\ -- Start the server --
if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)