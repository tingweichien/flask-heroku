# The flask tutorial

## Using libraries

- flask
- gunicorn

## Using tools

- VScode
- heroku
- git

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