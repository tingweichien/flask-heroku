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

LN_send_message("wvAy1Lu0U3OK1CrYSO1Nz2ElTalrqcWY14QBSYAMqWr",
                             "Test for the LINE Notify")