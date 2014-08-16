#!/usr/bin/python

import time
import gdata.spreadsheet.service

email = 'neurotest327@gmail.com'
password = 'ertobald88'
weight = '180'
# Find this value in the url with 'key=XXX' and copy XXX below
spreadsheet_key = '0ApyB_MBXPSjIdGNXRU9ZZzFBLWdjNWtoRUxYTjFiQkE'
#'0ApyB_MBXPSjIdDh3VFNXNllVZVZyNXhUWWRXNjBqNmc'
#'0ApyB_MBXPSjIdGxWSnJJWGdtbGlyclRzNk91emtYb0E'
#'0ApyB_MBXPSjIdEQ4d28zaG0tM1BQbU5FRk1IbVN1Tmc'
#'0ApyB_MBXPSjIdHY3eG1Jcm52aVZGUi1tV1lWb2lwcUE'
#'0ApyB_MBXPSjIdHp4SkRVOVVIYlh5TGduYUxGaW5sTHc'
# All spreadsheets have worksheets. I think worksheet #1 by default always
# has a value of 'od6'
worksheet_id = 'od6'
spr_client = gdata.spreadsheet.service.SpreadsheetsService()
spr_client.email = email
spr_client.password = password
spr_client.source = 'NeuroSky'
spr_client.ProgrammaticLogin()

# Prepare the dictionary to write
#dict = {}
#dict['date'] = time.strftime('%m/%d/%Y')
#dict['time'] = time.strftime('%H:%M:%S')
#dict['weight'] = weight
#print dict

def insertRow(input_data):
    entry = spr_client.InsertRow(input_data, spreadsheet_key, worksheet_id)
    if isinstance(entry, gdata.spreadsheet.SpreadsheetsList):
        print "Insert row succeeded."
    else:
        print "Insert row failed."
