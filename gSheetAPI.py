# \ This is the google sheet api feature
# \ reference : https://www.maxlist.xyz/2018/09/25/python_googlesheet_crud/
# \              https://www.learncodewithmike.com/2020/08/python-write-to-google-sheet.html

import pygsheets
import index
from typing import List
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

# \ -- Authorize --
client = pygsheets.authorize(service_file=index.GSheetApiKeyPath)

"""For example
sheet = gc.open_by_url(
    "https://docs.google.com/spreadsheets/d/1dZtaLtbP4PKsjcQ01mj25HDkEBzk-nF0094tUhce1YU/edit?usp=sharing")

# \--  Open the sheets --
wks_list = sheet.worksheets()
print(wks_list)

# \ -- Select the worksheet --
# \ Select by order
wks_order = sheet[0]

# \ Select by name
wks_name = sheet.worksheet_by_title("Table2")

# \ Update title
wks_order.title = "New Table2"


# \ -- Read the worksheets --
A1 = wks_order.cell("A1")
print(f"Al : {A1.value}")
A2 = wks_order.get_value("A2")
print(f"A2 : {A2}")
ALL = wks_name.get_all_values(include_tailing_empty=False,
                              include_tailing_empty_rows=False)
print(f"All: {ALL}")


# \ -- Update the google sheets --
wks_name.update_value('A1', 'test')

"""
def OpenGSheet(Species_table:str, gSheetIDList:list)->pygsheets.Worksheet:
    #\Get the sheet
    global client

    #\ Get the list
    if gSheetIDList is None:
        gSheetIDList = Sheet_id_dict()

    #\ get the url correspond to the input Species_table name
    #\ https://docs.google.com/spreadsheets/d/1dZtaLtbP4PKsjcQ01mj25HDkEBzk-nF0094tUhce1YU/edit?usp=sharing
    SpeciesUrl = None
    try:
        SpeciesUrl = index.GeneralgSheetUrl(gSheetIDList[Species_table])
        status = True
    except :
        # SpeciesUrl =  index.GeneralgSheetUrl(gSheetIDList["Calopterygidae01"])
        status = False


    #\ Open the sheets
    sheet = client.open_by_url(SpeciesUrl)
    wks_list = sheet.worksheets()

    #\ Select the worksheet
    #\ Select by order
    wks_order = wks_list[0]

    return wks_order

#\ Set the data to the gsheets
def SetDragonflyDataGoogleSheets(Species_table:str, gSheetIDList:list=None, NumRows:int=1, Data2Update:list=[]):
    """Set the data to the gsheets

    Args:
        Species_table (str): [description]
        gSheetIDList (list, optional): [description]. Defaults to None.
        NumRows (int, optional): [description]. Defaults to 1.
        Data2Update (list, optional): [description]. Defaults to [].
    """
    #\ Open the sheets
    wks_order = OpenGSheet(Species_table, gSheetIDList)
    #\ 2 is to skip the column name.
    wks_order.insert_rows(2, number=NumRows, value=Data2Update)



#\ Function to get the dragonfly data from the google sheets
def GetDragonflyDataGoogleSheets(Species_table:str, gSheetIDList:list=None)->list:
    """Function to get the dragonfly data from the google sheets
    Args:
        Species_table (str): title of the gsheet
        gSheetIDList (list, optional): gsheet list. Defaults to None, or you can put the cache.get("gGSheetList"). If None then funciton will get the sheet list itself.

    Returns:
        list: list of list, list of the data in the gsheet
        status: success or fail
    """

    #\ Open the sheets
    wks_order = OpenGSheet(Species_table, gSheetIDList)


    #\ Read the worksheets
    ALL = wks_order.get_all_values(include_tailing_empty=False,
                                include_tailing_empty_rows=False)

    #\ eliminate the null lat lon data
    gSheetResult = []
    ColumNum = len(ALL[0])-2 #\ minus 2 is because the weather and discription column are not using
    for data in ALL:
        if len(data) == ColumNum:
            gSheetResult.append(data)

    # print(f"All: {gSheetResult}")

    return gSheetResult



#\ Function to get the google sheet list of dictionay id
def Sheet_id_dict()->list:
    """Function to get the google sheet id list of dictionay
    Returns:
        list: google sheet list of dict [{name:id}, ....]
    """
    global client
    sheet = {}
    meta_list = client.drive.list()
    # print(meta_list)
    for file_meta in meta_list:
        if file_meta['mimeType'] == 'application/vnd.google-apps.spreadsheet':
            sheet[file_meta['name']] = file_meta['id']
    print(sheet)
    return sheet


########################################################
#\ Test case
# IDList = Sheet_id_dict()
# print(IDList)
# GetDragonflyDataGoogleSheets("Calopterygidae", IDList)
