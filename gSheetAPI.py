# \ This is the google sheet api feature
import pygsheets
import index
from typing import List
import logging

# \ -- Authorize --
client = None
try:
    # 加入防呆：如果金鑰失效或被 Google 拒絕，不要讓整個 App 崩潰
    client = pygsheets.authorize(service_file=index.GSheetApiKeyPath)
    logging.info("[INFO] Google Sheets API authorized successfully.")
except Exception as e:
    logging.error(f"[Google Auth Error] Failed to authorize Google Sheets API. Your JWT signature might be invalid or expired. Error: {e}")

def OpenGSheet(Species_table:str, gSheetIDList:list=None):
    global client
    if client is None:
        logging.error("[Google Auth Error] Client not initialized. Cannot open Google Sheet.")
        return None

    if gSheetIDList is None:
        gSheetIDList = Sheet_id_dict()

    try:
        SpeciesUrl = index.GeneralgSheetUrl(gSheetIDList[Species_table])
    except Exception as e:
        logging.error(f"[Google Sheets Error] Cannot find the sheet URL for {Species_table}: {e}")
        return None

    try:
        sheet = client.open_by_url(SpeciesUrl)
        wks_order = sheet.worksheets()[0]
        return wks_order
    except Exception as e:
        logging.error(f"[Google Sheets Error] Failed to open worksheet: {e}")
        return None

def SetDragonflyDataGoogleSheets(Species_table:str, gSheetIDList:list=None, NumRows:int=1, Data2Update:list=[]):
    wks_order = OpenGSheet(Species_table, gSheetIDList)
    if wks_order:
        try:
            wks_order.insert_rows(2, number=NumRows, value=Data2Update)
        except Exception as e:
            logging.error(f"[Google Sheets Error] Failed to insert rows: {e}")

def GetDragonflyDataGoogleSheets(Species_table:str, gSheetIDList:list=None)->list:
    wks_order = OpenGSheet(Species_table, gSheetIDList)
    if wks_order is None:
        return [False, []]

    try:
        ALL = wks_order.get_all_values(include_tailing_empty=False, include_tailing_empty_rows=False)
        gSheetResult = []
        ColumNum = len(ALL[0])-2
        for data in ALL:
            if len(data) == ColumNum:
                gSheetResult.append(data)
        return [True, gSheetResult]
    except Exception as e:
        logging.error(f"[Google Sheets Error] Failed to get all values: {e}")
        return [False, []]

def Sheet_id_dict()->dict:
    global client
    sheet = {}
    if client is None:
        logging.error("[Google Auth Error] Client not initialized. Cannot fetch sheet list.")
        return sheet

    try:
        meta_list = client.drive.list()
        for file_meta in meta_list:
            if file_meta['mimeType'] == 'application/vnd.google-apps.spreadsheet':
                sheet[file_meta['name']] = file_meta['id']
        return sheet
    except Exception as e:
        logging.error(f"[Google Drive Error] Failed to fetch drive list: {e}")
        return sheet