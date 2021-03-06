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

#### 1. somehow can show the image when deploying on the heroku

- I found that I should make sure that the file typt for my picture should in lowercase, despite the fact that it's not sensitive on the localhost. However, after I modified the problem, it still can't shown on the heroku server.

- So, I turn into another solution, which is change the file type to .png , then everything went well !!!

#### 2. The css template do not change after I modified it

- The solution is just to simply refresh the page by ```crtl + shift + R```

- reference:
  - [Why won't my Flask app connect to my CSS files?](https://stackoverflow.com/questions/45567877/why-wont-my-flask-app-connect-to-my-css-files/45588180)

#### 3. make sure when you using the ```url_for``` function there should be a corresponding function

- I get the error on the ```layout.html``` template, due to that I only create the ```.html``` file but not adding  the correspondingfunction in ```app.py```


#### 4. While running, the console log showing favicon.ico 404 not found

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

## Reference

- [Python網頁設計：Flask使用筆記(二)- 搭配HTML和CSS](https://medium.com/@yanweiliu/python%E7%B6%B2%E9%A0%81%E8%A8%AD%E8%A8%88-flask%E4%BD%BF%E7%94%A8%E7%AD%86%E8%A8%98-%E4%BA%8C-89549f4986de)

- [Python 學習筆記 : 用 Flask 架站 (一) 請求處理](http://yhhuang1966.blogspot.com/2019/08/python-flask.html)