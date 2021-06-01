from flight_data import FlightData
import requests
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

FLIGHT_KEY = "YOUR FLIGHT KEY"
FLIGHT_API = "https://tequila-api.kiwi.com"
FLIGHT_IATA = "/locations/query"
FLIGHT_SEARCH = "/v2/search"

FLIGHT_HEADER = {
    "apikey": FLIGHT_KEY,
}

tomorrow = date.today() + timedelta(days=1)
tomorrow = tomorrow.strftime("%d/%m/%Y")

six_month = date.today() + relativedelta(months=+6)
six_month = six_month.strftime("%d/%m/%Y")

parameters = {
    "date_from": tomorrow,
    "date_to": six_month,
    "fly_from": "AMS",
    "fly_to": "AMS",
    "nights_in_dst_from": 7,
    "nights_in_dst_to": 28,
    "flight_type": "round",
    "max_stopovers": 0,
    "one_for_city": 1,
}


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.

    def get_iata(self, city_name):
        parameters = {
            "term": city_name,
            "location_types": "city",
        }
        iata_data = requests.get(url=f"{FLIGHT_API}{FLIGHT_IATA}", params=parameters, headers=FLIGHT_HEADER)
        return iata_data.json()["locations"][0]["code"]

    def get_price(self, fly_from, fly_to):
        destination = {"fly_to": fly_to, "fly_from": fly_from}
        parameters.update(destination)
        price_data = requests.get(url=f"{FLIGHT_API}{FLIGHT_SEARCH}", params=parameters, headers=FLIGHT_HEADER)

        try:
            data = price_data.json()["data"][0]

        except IndexError:
            parameters["max_stopovers"] = 1
            price_data = requests.get(url=f"{FLIGHT_API}{FLIGHT_SEARCH}", params=parameters, headers=FLIGHT_HEADER)
            try:
                data = price_data.json()["data"][0]
            except IndexError:
                print("No flights found.")
                return None

            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0],
                stop_overs=1,
                via_city=data["route"][0]["cityTo"],
            )
            print(f"{flight_data.destination_city}: {flight_data.price} Euro with Stopover in {flight_data.via_city}")
            return flight_data

        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
            )

            print(f"{flight_data.destination_city}: {flight_data.price} Euro")
            return flight_data
