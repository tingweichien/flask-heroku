#\ ======================================
#\ |  Handle the specific message here  |
#\ ======================================
#\ reference
#\  1. https://developers.line.biz/flex-simulator/
#\  2. https://medium.com/@marstseng/line-flex-message-b83b33483f9d


from linebot.models import RichMenu, RichMenuSize, RichMenuArea, RichMenuBounds, PostbackAction, MessageAction, URIAction
from linebot import LineBotApi
import configparser
import index
from DataClass import DetailedTableInfo


#\ FLEX-MESSAGE
##########################################################################################################################

#\ Login Flex-message for login check text
#\ ---------------------------------------
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
        "align": "start",
        "margin": "none",
        "wrap": True,
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
                "text": "temp",
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
                "text": "temp",
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
        "style": "secondary",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "EXIT",
          "text": "LOGIN_EXIT"
        }
      },
      {
        "type": "button",
        "style": "secondary",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "NO",
          "text": "LOGIN_FAIL"
        }
      },
      {
        "type": "button",
        "style": "primary",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "OK",
          "text": "LOGIN_CONFIRM"
        }
      }
    ]
  }
}


#\ for testing
"""
#\ account
LoginCheckText["body"]["contents"][1]["contents"][0]["contents"][1]["text"] = "@@@@@@@@@@@@@@@@"
# \ password
LoginCheckText["body"]["contents"][1]["contents"][1]["contents"][1]["text"] = "################"
print(LoginCheckText)
"""



#\ Data Flex-message for search event
#\ ---------------------------------------
Search_event_text={
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "size": "micro",
      "header": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "ID Search",
            "color": "#ffffff",
            "align": "start",
            "size": "md",
            "gravity": "center"
          }
        ],
        "backgroundColor": "#27ACB2",
        "paddingTop": "19px",
        "paddingAll": "12px",
        "paddingBottom": "16px"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "Search the data by input ID ",
                "color": "#8C8C8C",
                "size": "sm",
                "wrap": True
              }
            ],
            "flex": 3
          },
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "GO",
              "text": "IDREQUEST"
            }
          }
        ],
        "spacing": "md",
        "paddingAll": "12px"
      },
      "styles": {
        "footer": {
          "separator": False
        }
      }
    },
    {
      "type": "bubble",
      "size": "micro",
      "header": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "Advance Search",
            "color": "#ffffff",
            "align": "start",
            "size": "md",
            "gravity": "center"
          }
        ],
        "backgroundColor": "#FF6B6E",
        "paddingTop": "19px",
        "paddingAll": "12px",
        "paddingBottom": "16px"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "Search with specific date and species",
                "color": "#8C8C8C",
                "size": "sm",
                "wrap": True
              }
            ],
            "flex": 1
          },
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "GO",
              "text": "hello"
            }
          }
        ],
        "spacing": "md",
        "paddingAll": "12px"
      },
      "styles": {
        "footer": {
          "separator": False
        }
      }
    }
  ]
}




#\ Request data message
RequestDataMsgText = {
  "type": "bubble",
  "size": "mega",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "ID",
        "weight": "bold",
        "size": "xxl",
        "margin": "md"
      },
      {
        "type": "text",
        "text": "Time",
        "size": "sm",
        "wrap": True,
        "align": "start"
      },
      {
        "type": "separator",
        "margin": "xxl"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "xxl",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "紀錄者",
                "size": "md",
                "color": "#555555",
                "flex": 0,
                "weight": "bold"
              },
              {
                "type": "text",
                "text": "User",
                "size": "sm",
                "color": "#111111",
                "align": "end"
              }
            ]
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "地點",
                "size": "md",
                "color": "#555555",
                "flex": 0,
                "weight": "bold"
              },
              {
                "type": "text",
                "text": "City District Place",
                "size": "sm",
                "color": "#111111",
                "align": "end",
                "wrap": True
              }
            ]
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "經緯度",
                "size": "md",
                "color": "#555555",
                "flex": 0,
                "weight": "bold"
              },
              {
                "type": "text",
                "text": "(LAT, LNG)",
                "size": "sm",
                "color": "#111111",
                "align": "end",
                "wrap": True
              }
            ]
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "contents": [
              {
                "type": "text",
                "text": "蜓種",
                "size": "md",
                "color": "#555555",
                "weight": "bold"
              },
              {
                "type": "text",
                "text": "Species",
                "size": "sm",
                "color": "#111111",
                "align": "start",
                "wrap": True
              }
            ]
          }
        ]
      },
      {
        "type": "separator",
        "margin": "xxl"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "md",
        "contents": [
          {
            "type": "text",
            "text": "描述",
            "size": "md",
            "flex": 0,
            "weight": "bold"
          },
          {
            "type": "text",
            "text": "Description",
            "size": "sm",
            "wrap": True
          }
        ]
      }
    ]
  },
  "styles": {
    "footer": {
      "separator": True
    }
  }
}

#\ handle the RequestDataMsgText
def RequestDataMsgText_handler(DrgonflyData:DetailedTableInfo)->str :
  RequestDataMsgText["body"]["contents"][0]["text"] = DrgonflyData.IdNumber
  RequestDataMsgText["body"]["contents"][1]["text"] = f"{DrgonflyData.Dates}, {DrgonflyData.Times}"
  RequestDataMsgText["body"]["contents"][3]["contents"][0]["contents"][1]["text"] = DrgonflyData.User
  RequestDataMsgText["body"]["contents"][3]["contents"][1]["contents"][1]["text"] = f"{DrgonflyData.City} {DrgonflyData.District} {DrgonflyData.Place}"
  RequestDataMsgText["body"]["contents"][3]["contents"][2]["contents"][1]["text"] = f"({round(float(DrgonflyData.Latitude), index.PositionPrecision)}, {round(float(DrgonflyData.Longitude), index.PositionPrecision)})"
  RequestDataMsgText["body"]["contents"][3]["contents"][4]["contents"][1]["text"] = DrgonflyData.Species
  RequestDataMsgText["body"]["contents"][5]["contents"][1]["text"] = DrgonflyData.Description
  return RequestDataMsgText

# print(RequestDataMsgText_handler("123", "123","123","123","123","123","123","123","123","123","123"))


#\ RICH-MENU
##########################################################################################################################
#\ Update the richmenu name and ID here
#\**************************************************************
#\    Login Richmenu : richmenu-e0edbad344efd7d9615a8f0823f64725
#\    Main Richmenu  : richmenu-fc0743c412e9282afa55d612c52547a5
#\    Main2 Richmenu : richmenu-fe7a083cdec686df7f1a9259eff6aef5
#\***************************************************************

#\ Init the line bot api
#\ ---------------------------------------
#\required
"""
config = configparser.ConfigParser()
config.read('config.ini')
gLine_bot_api = LineBotApi(config.get("line-bot", "channel_access_token"))
"""


#\ Richmenu general setting
#\ ---------------------------------------
#\ Attention:
#\    1. Create the richmenu
#\    2. Upload the richmenu image
#\    3. Check the current richmenu list
#\    4. Set the the richmenu as default if needed
#\    5. Delete the richmenu if you just want to update the specific menu or just want to drop it

#\ Get the rich menu list
def Get_RichMenu(line_bot_api):
  rich_menu_list = line_bot_api.get_rich_menu_list()
  return_rich_menu_list = dict()
  for rich_menu in rich_menu_list:
    print(f"[INFO] Rich menu '{rich_menu.name}', ID: {rich_menu.rich_menu_id}, selected : {rich_menu.selected}")
    return_rich_menu_list[rich_menu.name] = rich_menu.rich_menu_id

  return return_rich_menu_list

# print(Get_RichMenu(gLine_bot_api))


#\ Set default richmenu
# gLine_bot_api.set_default_rich_menu(rich_menu_list[0].rich_menu_id)


#\ Delete richmenu
# rich_menu_list = gLine_bot_api.get_rich_menu_list()
#for i in [0,1]:
# gLine_bot_api.delete_rich_menu(Get_RichMenu(gLine_bot_api)["Main Richmenu"])
# gLine_bot_api.delete_rich_menu(Get_RichMenu(gLine_bot_api)["Main2 Richmenu"])




#\ Upload function
#\ ---------------------------------------
def UploadRichMenu(line_bot_api ,file_path:str, rich_menu_id:str, content_type:str):
  """
  content_type = "image/jpeg" or "image/png、
  """
  with open(file_path, 'rb') as f:
    line_bot_api.set_rich_menu_image(rich_menu_id, content_type, f)




#\ Default Richmenu handling
def DefaultRichMenu(linebot_api, LoginState):
  rich_menu_dict = Get_RichMenu(linebot_api)
  if LoginState is True:
    linebot_api.set_default_rich_menu(rich_menu_dict["Main Richmenu"])
    print("[INFO] Set the Richmenu to Main Richmenu")
  else:
    linebot_api.set_default_rich_menu(rich_menu_dict["Login Richmenu"])
    print("[INFO] Set the Richmenu to Login Richmenu")


#\ Richmenu for login
#\ ---------------------------------------
#\ Create menu
"""
RichMenu_Create_LoginMenu = RichMenu(size=RichMenuSize(width=2500, height=843),
                                    selected=True,
                                    name="Login Richmenu",
                                    chat_bar_text="LOGIN",
                                    areas=[RichMenuArea(bounds=RichMenuBounds(x=0, y=0, width=2500, height=843),
                                                        action=MessageAction(label="Login",
                                                                              text="Login")
                                                        )
                                           ]
                                    )


#\ ID
RichMenu_Login_ID = gLine_bot_api.create_rich_menu(rich_menu=RichMenu_Create_LoginMenu)
print(f"[INFO] RichMenu_Login_ID : {RichMenu_Login_ID}")

#\ Upload the menu
UploadRichMenu(gLine_bot_api, index.LoginRichMenuImgPath, RichMenu_Login_ID, "image/jpeg")
"""




#\ Richmenu for mainpage
#\ ---------------------------------------
#\ Create menu
"""
RichMenu_Create_MainMenu = RichMenu(size=RichMenuSize(width=2500, height=1686),
                                    selected=False,
                                    name="Main Richmenu",
                                    chat_bar_text="Menu",
                                    areas=[RichMenuArea(bounds=RichMenuBounds(x=0, y=0, width=833, height=843),
                                                        action=MessageAction(label="TodayData",
                                                                              text="TodayData")),
                                           RichMenuArea(bounds=RichMenuBounds(x=833, y=0, width=833, height=843),
                                                        action=MessageAction(label="Record",
                                                                              text="Record")),
                                           RichMenuArea(bounds=RichMenuBounds(x=1666, y=0, width=833, height=843),
                                                        action=URIAction(label="DragonflyWeb",
                                                                          uri="https://liff.line.me/1656015794-QgErjV75")),
                                           RichMenuArea(bounds=RichMenuBounds(x=0, y=843, width=833, height=843),
                                                        action=MessageAction(label="Search",
                                                                              text="Search")),
                                           RichMenuArea(bounds=RichMenuBounds(x=833, y=843, width=833, height=843),
                                                        action=PostbackAction(label="Others",
                                                                              data="Others")),
                                           RichMenuArea(bounds=RichMenuBounds(x=1666, y=843, width=833, height=843),
                                                        action=URIAction(label="DragonflyWeb",
                                                                          uri="http://dragonfly.idv.tw/dragonfly/member_center.php")),
                                           ]
                                    )


#\ ID
RichMenu_Main_ID = gLine_bot_api.create_rich_menu(rich_menu=RichMenu_Create_MainMenu)
print(f"[INFO] RichMenu_Login_ID : {RichMenu_Main_ID}")


#\ Upload the menu
UploadRichMenu(gLine_bot_api, index.MainRichMenuImgPath, Get_RichMenu(gLine_bot_api)["Main Richmenu"], "image/jpeg")
"""





#\ Richmenu of the second main page
#\ ---------------------------------------
#\ Create menu
"""
RichMenu_Create_MainMenu2 = RichMenu(size=RichMenuSize(width=2500, height=843),
                                    selected=False,
                                    name="Main2 Richmenu",
                                    chat_bar_text="Menu2",
                                    areas=[RichMenuArea(bounds=RichMenuBounds(x=0, y=0, width=833, height=843),
                                                        action=PostbackAction(label="GoBackMain",
                                                                              data="GoBackMain")),
                                           RichMenuArea(bounds=RichMenuBounds(x=833, y=0, width=833, height=843),
                                                        action=MessageAction(label="Menu2-1",
                                                                              text="Menu2-1")),
                                           RichMenuArea(bounds=RichMenuBounds(x=1666, y=0, width=833, height=843),
                                                        action=MessageAction(label="Menu2-2",
                                                                              text="Menu2-2")),
                                           ]
                                    )


#\ ID
RichMenu_Main2_ID = gLine_bot_api.create_rich_menu(rich_menu=RichMenu_Create_MainMenu2)
print(f"[INFO] RichMenu_Login_ID : {RichMenu_Main2_ID}")


#\ Upload the menu
UploadRichMenu(gLine_bot_api, index.Main2RichMenuImgPath, Get_RichMenu(gLine_bot_api)["Main2 Richmenu"], "image/jpeg")

"""




