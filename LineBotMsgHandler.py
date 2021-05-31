#\ ======================================
#\ |  Handle the specific message here  |
#\ ======================================
#\ reference
#\  1. https://developers.line.biz/flex-simulator/
#\  2. https://medium.com/@marstseng/line-flex-message-b83b33483f9d


from linebot.models import RichMenu, RichMenuSize, RichMenuArea, RichMenuBounds, PostbackAction, MessageAction
from linebot import LineBotApi
import configparser
import index


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



#\ Data Flex-message for login check text
#\ ---------------------------------------




#\ RICH-MENU
##########################################################################################################################
#\ Update the richmenu name and ID here
#\ Login Richmenu : richmenu-e0edbad344efd7d9615a8f0823f64725
#\ Main Richmenu : richmenu-949ea5b9377082c825caff1f14fa3fc1

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
# gLine_bot_api.delete_rich_menu(rich_menu_list[1].rich_menu_id)




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
  else:
    linebot_api.set_default_rich_menu(rich_menu_dict["Login Richmenu"])


#\ Richmenu for login
#\ ID : richmenu-e0edbad344efd7d9615a8f0823f64725
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
#\ ID : richmenu-949ea5b9377082c825caff1f14fa3fc1g
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
                                                        action=MessageAction(label="Setting",
                                                                              text="Setting")),
                                           RichMenuArea(bounds=RichMenuBounds(x=0, y=843, width=833, height=843),
                                                        action=MessageAction(label="Search",
                                                                              text="Search")),
                                           RichMenuArea(bounds=RichMenuBounds(x=833, y=843, width=833, height=843),
                                                        action=MessageAction(label="Others",
                                                                              text="Others")),
                                           RichMenuArea(bounds=RichMenuBounds(x=1666, y=843, width=833, height=843),
                                                        action=MessageAction(label="DragonflyWeb",
                                                                              text="DragonflyWeb")),
                                           ]
                                    )


#\ ID
RichMenu_Main_ID = gLine_bot_api.create_rich_menu(rich_menu=RichMenu_Create_MainMenu)
print(f"[INFO] RichMenu_Login_ID : {RichMenu_Main_ID}")

#\ Upload the menu
UploadRichMenu(gLine_bot_api, index.MainRichMenuImgPath, RichMenu_Main_ID, "image/jpeg")
"""












