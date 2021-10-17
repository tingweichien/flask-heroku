import urllib
import urllib.request, urllib.parse
import requests


#\ Send the message
def LN_send_message(access_token:str=None, text_message:str=None, picurl:str=None):
    """Send the message using LINE Notify

    Args:
        access_token (str, optional): [Access token for the LINE Notify]. Defaults to None.
        text_message (str, optional): [test message to sen]. Defaults to None.
        picurl (str, optional): [piecture url]. Defaults to None.
    """
    print("[LINE Notify] Send message")

    #\ Handle the access token and check the input data vaildation
    if access_token is None:
        print("[Warning][LINE Notify] access token is None")
        return
    else:
        url = 'https://notify-api.line.me/api/notify'
        headers = {
                "Authorization": "Bearer "+ access_token,
                "Content-Type" : "application/x-www-form-urlencoded"
       }

    #\ The LINE Notify required the text message no matter whether the picture url is specify or not
    if text_message is None:
        print("[Warning][LINE Notify] Not specify the mandatory text message to send")
        return

    DataToSend = dict()
    DataToSend = {'message': text_message}
    if picurl is not None:
        temp_data = {"stickerPackageId": 2, 'stickerId': 38,
                    'imageThumbnail':picurl, 'imageFullsize':picurl}
        DataToSend.update(temp_data)


    # data = {'message': text_message,
    #         "stickerPackageId": 2, 'stickerId': 38,
    #         'imageThumbnail':picurl, 'imageFullsize':picurl}

    payload = {'message': text_message }
    r = requests.post(url, headers = headers, params = payload)
    print(f"r.status_code: {r.status_code}")
    return r.status_code

LN_send_message("\\x6772616e745f747970653d617574686f72697a6174696f6e5f636f646526636f64653d52574466516a6f366663556e777950316c716f454a502672656469726563745f7572693d6874747073253341253246253246647261676f6e666c792d666c61736b2d7765622e6865726f6b756170702e636f6d25324663616c6c6261636b2532466e6f7469667926636c69656e745f69643d67765941693567713041774246754c6d5848554b463326636c69656e745f7365637265743d756d52386f454f315178417362544956784874534d43734e70674163416771346a6b52454b39707254424e",
                             "Test for the LINE Notify")