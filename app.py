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
#\ -- APP ROUTER --
#\ Decorator 函式的裝飾:以函式為基礎,提供附加功能
@app.route("/")
def home():
    return render_template("home.html")



@app.route("/about", methods=["GET", "POST"])
def about():
    if request.method == "POST":
        #session.permanent = True
        user = request.form['nm']
        session['user'] = user
        return redirect(url_for("user"))
    else:
        if 'user' in session:
            return redirect(url_for("user"))

        return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/OSMmap")
def OSMmap():
    return render_template("OSMmap.html", apikey = index.GMAPapikey, api_on = index.bAPIon)


@app.route("/leaflet")
def leaflet():
    return render_template("leaflet.html", _index=index, _gSheetAPI=gSheetAPI)


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