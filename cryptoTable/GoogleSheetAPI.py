from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os.path
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleSheetAPI():

    __sheet = None

    def __init__(self, scope=["https://www.googleapis.com/auth/spreadsheets"],
                 id="1NoL0uV1QwB8toVev2ZqkWrCqnooWcb7fogXp3AdYK1g"):
        self.scope = scope
        self.id = id

    def authenticate_connection(self):

        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.scope)
        # If there are  o (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.scope)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        return creds

    def buildTable(self, creds):

        try:
            service = build('sheets', 'v4', credentials=creds)

            self.__sheet = service.spreadsheets()

        except HttpError as err:
            print(err)

    #Function to read the list of cryptos from google sheets sheet
    def read_cryptos_from_sheet(self, sheetName,range_name="A2:A"):
        result = self.__sheet.values().get(spreadsheetId=self.id,range=f"{sheetName}!{range_name}").execute()
        cryptos = result.get("values")

        return cryptos

    #Function that writes crypto prices to Google sheets sheet
    def write_prices_to_sheets(self,maxRange,cryptoPrices,sheetName,minRange = 2):

        for row in range(minRange,maxRange):
             self.__sheet.values().update(spreadsheetId=self.id,range=f"{sheetName}!D{row}",valueInputOption="USER_ENTERED",body = {"values":[[f"{cryptoPrices[row-2]}"]]}).execute()

    # Function that writes revnue to Google sheets sheet
    def write_revenu_to_sheets(self,sheetName,revenu,row,col="B"):
        self.__sheet.values().update(spreadsheetId=self.id, range=f"{sheetName}!{col}{row}",
                                              valueInputOption="USER_ENTERED",
                                              body={"values": [[f"{revenu}"]]}).execute()