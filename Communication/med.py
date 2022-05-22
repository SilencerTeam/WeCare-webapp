import streamlit as stream
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
import json
import requests
import datetime
import pandas as pd

import json
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account





def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def df_to_csv():
    
    fd = open("med_record.json",'r')
    txt = fd.read()
    fd.close()
    rec = json.loads(txt)
    zer = 0
    if '0' in rec:
        del rec['0']
    df = pd.DataFrame(rec).transpose()
    df1 = df.astype(str)
    nan_value = float("NaN")
    df1.replace("", nan_value, inplace=True)
    df1.dropna(inplace=True)

    df1.to_csv('file1.csv') # dataframe to CSV file 

def write_sheet(rec):
    new_rec = []
    for i in rec.keys():
        nm = rec[i]['Name']  #0
        med = rec[i]['Medicine']  #1
        tm = rec[i]['time']  #2
        em = rec[i]['Email']  #3
        mob = rec[i]['Mobile']  #4
        if med != "" or em != "":
            new_rec.append([nm, med, tm, em, mob])



    new_dict = dict()
    for i in range(len(new_rec)):
        new_dict.setdefault(str(i), []).append(new_rec[i])



    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'keys.json'
    creds = None
    creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    SAMPLE_SPREADSHEET_ID = '1CSsXvnbkM3iNCaw9IRIlM_jAR0E84n4LDdnXzn9b364'


    service = build('sheets', 'v4', credentials=creds)
    el = len(rec) + 1
    col = 'D' + str(el)
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range="file1!A1:D1").execute()
    values = result.get('values', [])
    aoa = new_rec
    request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="sheet1!A1", valueInputOption="USER_ENTERED", body={"values" :aoa}).execute()
    # print(col)




def app():

    fd = open("med_record.json",'r')
    sl = fd.read()
    fd.close()
    info = json.loads(sl)

    stream.markdown("<h1 style='text-align: center; color: white;'>PERSONAL INFORMATION</h1>", unsafe_allow_html=True)
    lottie_med = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_tutvdkg0.json")
    st_lottie(lottie_med)

    with stream.form(key = 'forml'):
        pid = len(info) + 1
        name = stream.text_input("Enter your name")
        email = stream.text_input("Enter EMAIL ID")
        medicine = stream.text_input("Write the name of medicines prescribed by the doctor")
        time  = stream.time_input("Specify the timing of taking the medicine", datetime.time(00, 00)) 
        mob = stream.text_input("Write your contact no.")
        submit_button = stream.form_submit_button(label = 'Confirm')

    if submit_button:
        stream.success("Info added")

    info[pid] = {'Name' : name, 'Medicine' : medicine, 'time': str(time), 'Email' : email, 'Mobile' : mob}

    js = json.dumps(info)
    fd = open("med_record.json",'w')
    fd.write(js)
    fd.close()

    # df_to_csv()
    fd = open("med_record.json",'r')
    txt = fd.read()
    fd.close()
    rec = json.loads(txt)
    write_sheet(rec)


        
app()