#\ put the line bot text here
#\ reference
#\  1. https://developers.line.biz/flex-simulator/
# \ 2. https://medium.com/@marstseng/line-flex-message-b83b33483f9d

from VarIndex import *

#\ Login Flex-message for login check text
# LoginCheckText = {
#         'type': 'bubble',
#         'direction': 'ltr',
#         'hero': {
#             'type': 'image',
#             'url': 'https://i.imgur.com/SpuIzyQ.jpeg',
#             'size': 'full',
#             'aspectRatio': '20:13',
#             'aspectMode': 'cover',
#             'action': { 'type': 'uri', 'uri': 'https://i.imgur.com/SpuIzyQ.jpeg', 'label': 'label' }
#         }
#     }
LoginCheckText={
  "type": "bubble",
  'direction': 'ltr',
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "Please check again for login account and password",
        "size": "lg",
        "offsetTop": "none",
        "offsetBottom": "none",
        "align": "start",
        "margin": "none",

        "weight": "bold"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "Account",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 2
              },
              {
                "type": "text",
                "text": "",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "Password",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 2
              },
              {
                "type": "text",
                "text": "",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "NO",
          "text": "LOGIN_FAIL"
        }
      },
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "OK",
          "text": "LOGIN_OK"
        }
      },
      {
        "type": "spacer",
        "size": "sm"
      }
    ],
    "flex": 0
  }
}


#\ for testing
#\ account
# LoginCheckText["body"]["contents"][1]["contents"][0]["contents"][1]["text"] = "@@@@@@@@@@@@@@@@"
#\ password
# LoginCheckText["body"]["contents"][1]["contents"][1]["contents"][1]["text"] = "################"
# print(LoginCheckText)