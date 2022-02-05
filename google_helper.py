# google stuff
import os
from dotenv import load_dotenv

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


load_dotenv()


def google_connect_and_authenticate():
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    TOKEN_JSON = "token.json"
    CREDENTIALS_JSON = "credentials.json"
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_JSON):
        creds = Credentials.from_authorized_user_file(TOKEN_JSON, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_JSON, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(TOKEN_JSON, "w") as token:
            token.write(creds.to_json())

    return creds


def thing(creds):
    SPREADSHEET_ID = os.getenv("GSHEET_WEEB")
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="A1:B10").execute()
    values = result.get("values", [])

    print(values)


# testing only
if __name__ == "__main__":

    creds = google_connect_and_authenticate()
    thing(creds)