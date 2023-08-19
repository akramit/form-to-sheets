from flask import Flask, request

#from __future__ import print_function
import os.path

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID  of spreadsheet.
SPREADSHEET_ID = '1UpC3UmvHtiFLm2wEqPLj81MnarJNqqIpnNa8bD8ZVis'

@app.route('/')
def index():
    with open('index.html', 'r') as file:
        return file.read()

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    mobile = request.form.get('mobile')
    
    # Add the data to the Google Sheets
    data = [name, mobile]
    submit_to_spreadsheet(data)
    return "Data submitted successfully!"

def submit_to_spreadsheet(data):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)
        values = [
            [data[0],data[1]],
        ]
        body = {
            'values': values
        }
        # Call the Sheets API
        range_name = "A2:B25"
        value_input_option = "USER_ENTERED"
        sheet = service.spreadsheets()
        result = sheet.values().append(spreadsheetId=SPREADSHEET_ID,
                                        body=body, range=range_name,
                                        valueInputOption=value_input_option).execute()
    except HttpError as err:
        print("Error occurred")
        return err


if __name__ == '__main__':
    app.run(debug=True)
