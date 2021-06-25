#\ this is the entry of the program

from flask import Flask, render_template, request, url_for, redirect, session
from flask_session import Session
from datetime import timedelta
import LineBotClass
import index
from VarIndex import cache
import gSheetAPI



#\ __name__ represent the current module
app = Flask(__name__)

# Check Configuration section for more details
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

#\ secret key for session
app.secret_key = index.APP_Pri_Key
app.permanent_session_lifetime = timedelta(seconds=5)

#\ cache for global variable
cache.init_app(app=app, config={"CACHE_TYPE": "filesystem", "CACHE_DIR":"/tmp"})

#\set cache data
LineBotClass.InitCache(cache)

#\ Init default richmenu
# gLine_bot_api.set_default_rich_menu(cache.get("RichMenuID")["Login Richmenu"])


################################################################################
#\ -- App menu css setting --
#\ Remeber to update this when adding another router
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


@app.route("/Leaflet")
def Leaflet():
    #\ Active the menu bar
    global Pre_Menu
    L_MenuBarSetting = MenuBarSetting
    L_MenuBarSetting[Pre_Menu]["class"] = "btn"
    L_MenuBarSetting[4]["class"] = "btn-active"
    Pre_Menu = 4
    return render_template("Leaflet.html", _index=index, _gSheetAPI=gSheetAPI, _MenuBarSetting=L_MenuBarSetting)


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
    #\ handler
    LineBotClass.LineBotHandler(app)
    return "ok"


#\ handle the message
# @LineBotClass.gHandler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     LineBotClass.gLine_bot_api.reply_message(
#                             event.reply_token,
#                             TextSendMessage(text=event.message.text)
#                             )y




################################################################################
#\ start the server
if __name__ == "__main__":
    #\ auto reload page
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    #\ 啟動伺服器
    app.run(debug=True)