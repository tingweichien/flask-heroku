# The flask tutorial

###### tags: `python`  `web`

## Introduce

WSGI 協定是 Python 網頁應用程式與伺服器溝通的介面, 來自客戶端的請求會被伺服器以 WSGI 協定封裝後傳送給應用程式, 而應用程式的回應也會用 WSGI 回傳給伺服器, 運作架構如下 :
![](https://i.imgur.com/7ZVtv2y.png)

實作 WSGI 協定的框架事實上具有兩個介面, 一個是面向 Web 伺服器的介面 (Server side), 另外一個是面向應用程式的介面, 架構圖如下 :
![](https://i.imgur.com/xsEPsgp.png)

Flask 內建的 Werkzeug 伺服器即實作了 WSGI 協定介面, 同時它本身也是一個實作 HTTP 的 Web 伺服器, 可直接與客戶端溝通, 但其效能只能做為開發使用. 實際運營使用例如 Nginx 或 Apache 等伺服器, 它們也都支援 WSGI 介面.

## Using libraries

- flask
- gunicorn

## Using tools

- VScode
- heroku
- git

## Guide

### Use python in html (Jinja)

To use python code inside the html requires jinja library.
i.e.

```html
<!doctype html>
  <table border = 1>
    {% for key, value in result.items() %}

    <tr>
       <th> {{ key }} </th>
       <td> {{ value }} </td>
    </tr>

    {% endfor %}
  </table>
</html>
```

#### Usage

- ```{% XXXXX %}``` : statements
  - ```{% for i in range(10) %} time {% endfor %}``` --> this will print ten lines of **time**
- ```{{ XXXXX }}``` : variabes
  - ```<h1> the variabel will be {{var}} </h1>``` --> this will print the varible you set
- ```{# XXXXX #}``` : comments

- **Inheritance**
  - In parents template (layout.html)

    ```html
    <!doctype html>
      <head>
        <title>the title of the webpage</title>
        <% block head %>
        <% endblock %>
      </head>
      <body>
        <% block body %>
        <% endblock %>
      </body>
    </html>
    ```

  - In child templates (child.html)

    ```html
    <%extends "layout.html" %>
      <% block head %>
        something to show in the head
      <% endblock %>
      <% block body %>
        <li>XXXXXX</li>
        <img>XXXXX.png
      <% endblock %>
    ```

#### Reference

- [Jijna Template Designer Documentation](https://jinja.palletsprojects.com/en/2.11.x/templates/#variables)
- [Send data to Flask template (Jinja2)
](https://pythonbasics.org/flask-template-data/)

## Record

### [2020/10/06]

1. somehow can show the image when deploying on the heroku

   - I found that I should make sure that the file typt for my picture should in lowercase, despite the fact that it's not sensitive on the localhost. However, after I modified the problem, it still can't shown on the heroku server.

   - So, I turn into another solution, which is change the file type to .png , then everything went well !!!

2. The css template do not change after I modified it

   - The solution is just to simply refresh the page by ```crtl + shift + R```

   - reference:
     - [Why won't my Flask app connect to my CSS files?](https://stackoverflow.com/questions/45567877/why-wont-my-flask-app-connect-to-my-css-files/45588180)

3. make sure when you using the ```url_for``` function there should be a corresponding function

   - I get the error on the ```layout.html``` template, due to that I only create the ```.html``` file but not adding  the correspondingfunction in ```app.py```


4. While running, the console log showing favicon.ico 404 not found

   - that means there are no icon specified.
   - the icon can be in ```.png```or ```.ico```
   - the html to add

     ```html
       <link rel="shortcut icon" href="/path/to/icons/favicon.ico">
       <link rel="icon" type="image/png" href="/path/to/icons/favicon-192x192.png" sizes="192x192">
       <link rel="apple-touch-icon" sizes="180x180" href="/path/to/icons/apple-touch-icon-180x180.png">
     ```

   - reference:
       [What is the best practice for creating a favicon on a web site?](https://stackoverflow.com/questions/25952907/what-is-the-best-practice-for-creating-a-favicon-on-a-web-site)

##### Reference

   - [Python網頁設計：Flask使用筆記(二)- 搭配HTML和CSS](https://medium.com/@yanweiliu/python%E7%B6%B2%E9%A0%81%E8%A8%AD%E8%A8%88-flask%E4%BD%BF%E7%94%A8%E7%AD%86%E8%A8%98-%E4%BA%8C-89549f4986de)

   - [Python 學習筆記 : 用 Flask 架站 (一) 請求處理](http://yhhuang1966.blogspot.com/2019/08/python-flask.html)

### [2021/05/11]

1. Error after changing the name of the project
    - error

        ```shell
        D:\Code\python\web\flask_practice>git push -u heroku master
        error: src refspec master does not match any
        error: failed to push some refs to 'https://git.heroku.com/dragonfly-flask-web.git'
        ```

    - solve

        ```shell
        git push heroku HEAD:master
        ```

2. Heroku command

   1. Deploying from a branch besides main

      ```shell
      git push heroku testbranch:main
      ```

### [2021/05/20]

1. userId is user_id : ```event.source.user_id```
     - <https://xiaosean.github.io/chatbot/2018-04-19-LineChatbot_usage/>)

2. Flask cache for global variable : ```from flask_caching import Cache```
   Since the flask is multithread, the gloabl variable will not work, we use the **session** or **cache** to implement.
   - <https://flask-caching.readthedocs.io/en/latest/index.html>
   - <https://stackoverflow.com/questions/32815451/are-global-variables-thread-safe-in-flask-how-do-i-share-data-between-requests>

3. [Line bot Flex message template](https://medium.com/@marstseng/line-flex-message-b83b33483f9d) and [useful online desginer](https://developers.line.biz/flex-simulator/)

    ![Line bot Flex message](https://i.imgur.com/BQpqWkc.png)

4. other useful line bot design
    - <https://ithelp.ithome.com.tw/articles/10217767>
    - <https://ithelp.ithome.com.tw/articles/10229943>
    - <https://engineering.linecorp.com/zh-hant/blog/line-device-10/>
    - <https://ithelp.ithome.com.tw/articles/10219503>
    - <https://engineering.linecorp.com/zh-hant/blog/2020-flex-message-10-reason/>

5. LIFF (Line Front End Framework)
    - <https://ithelp.ithome.com.tw/articles/10222415>

6. font

    ```json
    {
      "type": "text",
      "text": "...",
      "contents": [
        {
          "type": "span",
          "text": "LINE",
          "size": "32px",
          "weight": "bold",
          "color": "#00ff00"
        },
        {
          "type": "span",
          "text": " Developers",
          "size": "24px"
        }
      ]
    }
    ```

    ![font](https://i.imgur.com/ny1bXZS.png)

### [2021/05/23]

1. Add Heroku Postgres
2. reference
   - https://ithelp.ithome.com.tw/articles/10219773
   - https://docs.postgresql.tw/the-sql-language/data-manipulation/6.1.-xin-zeng-zi-liao
   - https://docs.postgresql.tw/the-sql-language/data-types/date-time
   - https://www.postgresqltutorial.com/postgresql-upsert/

3. Insert if non-exist

   - https://stackoverflow.com/questions/4069718/postgres-insert-if-does-not-exist-already

4. Heroku change the timezone

  ```shell
  heroku config:add TZ="Asia/Taipei"
  ```

5. Check the free dyno hours

  ```shell
  heroku ps -a dragonfly-flask-web
  ```

### [2021/05/24]

1. When using the connection under the local using ```os.popen```, but when deploy to the Heroku, using ```os.system``` instead to
  get the database URI or infomation

- error log
  ![error log](https://i.imgur.com/1TBIJ7U.png)

- solving
  ![solving](https://i.imgur.com/9A8LOBz.png)



### [2021/05/25]

1. Split the string with something and store to list

  ```python
  txt = "apple#banana####cherry##orange"

  x = list(filter(None, txt.split("#")))
  ```

  result

  ```shell
  ['apple', 'banana', 'cherry', 'orange']
  ```

2. Turn the list to string

  ```python
  s_list = ["a", "b", "2", "asd", "rew123"]
  s = "".join(s_list)
  s2 = ", ".join(s_list)
  ```

  result

  ```shell
  s = 'ab2asdrew123'
  s2 = 'a, b, 2, asd, rew123'
  ```

### [2021/05/21]

1. Alarm to do action in schedule

   - <https://ithelp.ithome.com.tw/articles/10218874>
    ![Cron](https://i.imgur.com/HOqV9IZ.png)


### [2021/06/08]

1. Successfully add the clock to the heroku. The key point is as following
   - Run the clock.py on it's own by adding ```clock: python clock.py``` in the Procifile
   - Don't add any file or code or import about the clock.py to the main python file (app.py)
   - After deploying to the Heroku, turn on this dyno on Configure Dynos
    ![Dynos Configuration](https://i.imgur.com/nDHvqnZ.png)
   - Reference : <https://ithelp.ithome.com.tw/articles/10219082>
    ![CLI for clock](https://i.imgur.com/8WEX7XN.png)

2. Gunicorn(Green unicorn)

     - option

        ```shell
        reload ： 程式碼更新時將重啟工作，預設為False。此設定用於開發，每當應用程式發生更改時， 都會導致工作重新啟動。
        preload ： 在工作程序被複制(派生)之前載入應用程式程式碼，預設為False。通過預載入應用程  式，你可以節省RAM資源，並且加快伺服器啟動時間。 可以打印出具體的錯誤資訊
        ```

      - ref : <https://www.796t.com/article.php?id=208479>

### [2021/06/15]

1. Google sheet api
2. Reference :
   - <https://www.maxlist.xyz/2018/09/25/python_googlesheet_crud/>
   - <https://hackmd.io/@Yun-Cheng/GoogleSheets>

3. [javascript: dynamic drop down menu values](https://stackoverflow.com/questions/20483470/javascript-dynamic-drop-down-menu-values/20485740)
    ![dynamic drop down menu values](https://i.imgur.com/rCoee4e.png)



### [2021/06/20]

1. The steps to add the folder or file into the authorization

     - Go to the GCP and remeber the email of you're project
      ![picture 1](https://i.imgur.com/ZPEoL6r.png)

     - Go to the folder you want to use in this projecta and sharing it with this email.
      ![picture 2](https://i.imgur.com/MxrVOCl.png)

    - Use the code below, we can see the folder and file share to this.

      ```python
      # \ -- Authorize --
      import pygsheets

      gc = pygsheets.authorize(service_file=index.GSheetApiKeyPath)

      def folder_id_dict(client):
      folders = {}
      meta_list = client.drive.list()
      print(meta_list)
      for file_meta in meta_list:
          if file_meta['mimeType'] == 'application/vnd.google-apps.spreadsheet':
              folders[file_meta['name']] = file_meta['id']
      return folders

      #your use:
      names = folder_id_dict(gc)
      print(names)
      ```

    - Reference : [How do you create a new sheet in a specific folder/directory using PyGSheets v2?](https://stackoverflow.com/questions/55914179/how-do-you-create-a-new-sheet-in-a-specific-folder-directory-using-pygsheets-v2)

## [2021/06/23]

1. Add the constraint for zooming the map with **ctrl** by following [Leaflet.GestureHandling](https://github.com/elmarquis/Leaflet.GestureHandling)


## [2021/10/16]

1. The database GUI for the PostgreSQL database : **pgAdmin**
   ![pgAdmin](https://i.imgur.com/TybeITK.png)
