# ask the user to add her name to a google sheet
# check the requested cities (also in google sheet) against a price
# if price is available send an email

from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

DEPARTURE_CITY = "AMS"
KEY_IATA_CODE = "IATA Code"

# user input (name, email)
data_manager.add_new_user()


# for entries in google sheet, if iata code is empty, search for iata code based on city name
sheet_data = data_manager.get_data()
print(len(sheet_data))
for x in range(len(sheet_data)):
    if sheet_data[x][KEY_IATA_CODE] == "":
        sheet_data[x][KEY_IATA_CODE] = flight_search.get_iata(sheet_data[x]["City"])

# update entries in google sheet
data_manager.update_iatacode(sheet_data)

# get all emails from user data sheet
user_data = data_manager.get_email()
user_emails = [entry["Email"] for entry in user_data]

# search for price
for x in range(len(sheet_data)):
    flight = flight_search.get_price(fly_from=DEPARTURE_CITY, fly_to=sheet_data[x][KEY_IATA_CODE])
    # email info to user
    if flight is not None and flight.price < sheet_data[x]["Lowest Price"]:
        content = f"Subject: Low Price! {flight.price} - {flight.origin_city}-{flight.destination_city}\n\nOnly {flight.price} Euro to fly from {flight.origin_city} to {flight.destination_city}, from {flight.out_date} to {flight.return_date}.\n"
        if flight.stop_overs > 0:
            content += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."
        notification_manager.send_email(message=content, email_list=user_emails)




