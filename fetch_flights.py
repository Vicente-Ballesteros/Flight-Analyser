import requests
import pandas as pd

def fetch_flights(min_lat, max_lat, min_lon, max_lon):
    url = "https://opensky-network.org/api/states/all"
    params = {
        "lamin": min_lat,
        "lamax": max_lat,
        "lomin": min_lon,
        "lomax": max_lon,
    }

    response = requests.get(url, params=params)
    data = response.json()

    columns = [
        "icao24", "callsign", "origin_country",
        "time_position", "last_contact",
        "longitude", "latitude", "baro_altitude",
        "on_ground", "velocity", "heading",
        "vertical_rate", "sensors", "geo_altitude",
        "squawk", "spi", "position_source"
    ]

    flights = pd.DataFrame(data["states"], columns=columns)
    flights = flights[["callsign", "origin_country", "latitude",
                        "longitude", "baro_altitude", "velocity",
                        "heading", "vertical_rate", "on_ground"]]
    flights["callsign"] = flights["callsign"].str.strip()
    flights = flights[flights["on_ground"] == False]

    return flights

if __name__ == "__main__":
    flights = fetch_flights(49.9, 58.7, -8.2, 1.8)
    print(f"Found {len(flights)} flights over the UK\n")
    print(flights.head(10).to_string(index=False))
