import os
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from coinprices import getCoinsData

SCOPES = [os.environ['SCOPE1']]
SAMPLE_SPREADSHEET_ID = os.environ['SAMPLE_SPREADSHEET_ID']
SAMPLE_RANGE_NAME = os.environ['SAMPLE_RANGE_NAME']
JSON_TOKEN = json.loads(os.environ["JSON_TOKEN"])
JSON_CREDENTIALS = json.loads(os.environ['JSON_CREDENTIALS'])

def main():
  creds = None

  if JSON_TOKEN:
    creds = Credentials.from_authorized_user_info(JSON_TOKEN, SCOPES)

  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_config(JSON_CREDENTIALS, SCOPES)
      creds = flow.run_local_server(port=0)

    os.environ['JSON_TOKEN'] = creds.to_json() 

  try:
    service = build("sheets", "v4", credentials=creds)

    sheet = service.spreadsheets()

    values = getCoinsData()

    body = {"values": values}

    (
      sheet.values()
      .update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,valueInputOption="RAW",body=body)
      .execute()
    )

  except HttpError as err:
    print(err)


if __name__ == "__main__":
  main()