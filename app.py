from flask import Flask

# __name__ represent the current module
app = Flask(__name__)

# Decorator 函式的裝飾:以函式為基礎,提供附加功能
@app.route("/")
def home():
    return "Hello Flask home"

@app.route("/test") # 代表我們要處理的路徑
def text():
    return "This is test"

if __name__ == "__main__":
    #啟動伺服器
    app.run()