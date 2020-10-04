from flask import Flask, render_template

# __name__ represent the current module
app = Flask(__name__)

# Decorator 函式的裝飾:以函式為基礎,提供附加功能
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/test") # 代表我們要處理的路徑
def text():
    return "This is test"

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")



if __name__ == "__main__":
    #啟動伺服器
    app.run(debug=True)