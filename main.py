import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from dotenv import dotenv_values

from coinprices import getCoinsData

config = dotenv_values()

# If modifying these scopes, delete the file token.json.
SCOPES = [config.get('SCOPE1')]
# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = config.get('SAMPLE_SPREADSHEET_ID')
SAMPLE_RANGE_NAME = config.get('SAMPLE_RANGE_NAME')

def main():
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    # values = [["A"], ["B"]]
    values = getCoinsData()
    body = {"values": values}
    result_update = (
      sheet.values()
      .update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,valueInputOption="RAW",body=body)
      .execute()
    )

  except HttpError as err:
    print(err)


if __name__ == "__main__":
  main()