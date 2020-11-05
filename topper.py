from __future__ import print_function
import pickle
from settings import *
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1SN2rcS9cSwuMT-MjIRHfR9yZPKi2bShp9-WEBv5Ri3s'
CRED_FILE = os.path.join(GAME_FOLDER,'credentials.json')
TOK_FILE = os.path.join(GAME_FOLDER,'token.pickle')

def winner_up(name,level,score):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOK_FILE):
        with open(TOK_FILE, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CRED_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOK_FILE, 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()

    listofstuff = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range='A1:D1').execute()['values'][0]
    listofstuff[1] = int(listofstuff[1])
    listofstuff[2] = int(listofstuff[2])
    if level + score > listofstuff[1] + int(float(listofstuff[2]) / 3.0):
        values = [[name,str(level),str(score)]]
        body = {'values': values}
        result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,valueInputOption = 'USER_ENTERED', range='A1:D1', body=body).execute()
        retval = [name,str(level),str(score)]
    else:
        retval = [listofstuff[0],str(listofstuff[1]),str(listofstuff[2])]
    return retval


def winner():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOK_FILE):
        with open(TOK_FILE, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CRED_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOK_FILE, 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()

    listofstuff = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range='A1:D1').execute()['values'][0]
    listofstuff[1] = int(listofstuff[1])
    listofstuff[2] = int(listofstuff[2])
    retval = [listofstuff[0],str(listofstuff[1]),str(listofstuff[2])]
    return retval
