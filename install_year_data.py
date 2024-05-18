import requests
import json
import datetime
from tqdm import tqdm
import logging
from utiles import Logger
year = datetime.datetime.now().year
def get_api_link(year, month):
    return f"http://api.aladhan.com/v1/calendarByCity/{year}/{month}"

def create_timestamp(year, month, day, time_str):
    time_str = time_str.replace(" (EET)", "")
    time_str = time_str.replace(" (EEST)", "")
    hour, minute = map(int, time_str.split(":"))
    timestamp = datetime.datetime(year, month, day, hour, minute)
    return timestamp.timestamp()


params = {
    "city": "Alexandria",
    "country": "Egypt",
    "method": "5"
}

logging.info(f"[Downloading] {year} data for {params['city']}, {params['country']} using method {params['method']}")

downloaded_data = {}
for month in tqdm(range(1, 12 +1), desc=f"Downloading {year} data...", ncols=100):
    response = requests.get(get_api_link(year, month), params=params)
    data = response.json()["data"]
    downloaded_data[str(month)] = {}
    for day in range(len(data)):
        praying_times = data[day]["timings"]
        hijri_date = data[day]["date"]["hijri"]["date"]
        praying_times = {key:create_timestamp(year, month, day + 1, time_str) for key, time_str in praying_times.items() if key !="Sunset"}
        praying_times = dict(sorted(praying_times.items(), key=lambda item: item[1]))
        downloaded_data[str(month)][f"{day + 1}"] = {}
        downloaded_data[str(month)][f"{day + 1}"]["praying_times"] = praying_times
        downloaded_data[str(month)][f"{day + 1}"]["hijri_date"] = hijri_date


with open("year_data.json", 'w') as file:
    json.dump(downloaded_data, file)
