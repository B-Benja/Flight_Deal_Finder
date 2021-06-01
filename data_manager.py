import gspread
from oauth2client.service_account import ServiceAccountCredentials

# add credentials to the account
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
CREDS = ServiceAccountCredentials.from_json_keyfile_name('YOUR KEY.json', SCOPE)
# authorize the clientsheet
client = gspread.authorize(CREDS)
# get the instance of the Spreadsheet
sheet = client.open('FlightDeals')
# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)
sheet_user = sheet.get_worksheet(1)

class DataManager:

    def __init__(self):
        self.destination_nfo = {}

    def get_data(self):
        self.destination_nfo = sheet_instance.get_all_records()
        return self.destination_nfo

    def update_iatacode(self, sheet_data):
        print(sheet_data)
        for x in range(len(sheet_data)):
            sheet_instance.update_acell(f"B{x+2}", sheet_data[x]["IATA Code"])

    def add_new_user(self):
        ### User input to sign up for flight club

        print("""Welcome to our Flight Club.\n
        We find the best flight deals and mail you the lowest prices.""")
        first_name = input("What ist your first name? ")
        last_name = input("What is your last name? ")
        email = input("What is your email? ")
        email_confirm = input("Please confirm (retype) your email. ")

        if email == email_confirm:
            user_entry = [first_name, last_name, email]
            empty_row_user_sheet = len(sheet_user.get_all_records()) + 2
            sheet_user.insert_row(user_entry, empty_row_user_sheet)
            print("You are in the club!")

    def get_email(self):
        self.user_data = sheet_user.get_all_records()
        return self.user_data


