import re
import json
import numpy
import requests
from dateutil import parser
from datetime import datetime


def feed(city, token):
    url = f"http://api.waqi.info/feed/{city}/?token={token}"
    return requests.get(url).json()


def get_forecast(url):
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 " \
                 "Safari/537.36 "
    response_text = requests.get(url, headers={"User-Agent": user_agent}).text
    matches = re.search("var f=\\[(.*)\\];try {var div =", response_text)

    return parse_forecast_data(matches.group(1))


def parse_forecast_data(json_text):
    list_days = json.loads(json_text)["d"]
    map_days = {}

    for day in list_days:
        date = parser.parse(day["t"])

        if not 7 <= date.hour <= 21:
            continue

        key = date.strftime("%Y%m%d")

        if key in map_days:
            map_days[key].append(day)
        else:
            map_days[key] = [day]

    result = []

    for day in map_days:
        try:
            day_data = map_days[day]
            matrix = []

            for record in day_data:
                v = record["aqi"]["v"]
                if "pm25" in v:
                    matrix.append(v["pm25"])

            np_matrix = numpy.array(matrix)

            if len(np_matrix) == 0:
                continue

            min_value = min(np_matrix[::, 0])
            max_value = max(np_matrix[::, 1])

            date = datetime.strptime(day, "%Y%m%d")

            result.append({
                "date": date.strftime("%A %d"),
                "min": min_value,
                "max": max_value
            })

        except KeyError:
            continue

    return result
