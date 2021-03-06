#\ this is the entry of the program

from flask import Flask, render_template, request, url_for, redirect, session
from datetime import timedelta
from index import *

# __name__ represent the current module
app = Flask(__name__)

#\ secret key for seeeion
app.secret_key ="tim960622"
app.permanent_session_lifetime = timedelta(seconds=5)

#\ APP ROUTER
#\ Decorator 函式的裝飾:以函式為基礎,提供附加功能
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/test") # 代表我們要處理的路徑
def text():
    return "This is test"


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
    return render_template("OSMmap.html", apikey = GMAPapikey, api_on = bAPIon)





#\ to HTTP method
@ app.route("/urlREST/<name>")
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


#\ start the server
if __name__ == "__main__":
    # auto reload page
    app.config['TEMPLATES_AUTO_RELOAD'] = True


    #啟動伺服器
    app.run(debug=True)