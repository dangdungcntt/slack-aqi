import re
import os
import json
import requests
import numpy as np
from dateutil import parser
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def get_color(value):
    if value <= 50:
        return '#0000ff'
    if value <= 100:
        return '#ffff00'
    if value <= 200:
        return '#ffa500'
    if value <= 300:
        return '#ff0000'
    return '#a52a2a'


def parse_data(json_text):
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

            np_matrix = np.array(matrix)

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


# api-endpoint
url = "http://api.waqi.info/feed/hanoi/?token=34ef24a0de1013ac74e978dc0ca7513e9c5e81a2"
forecastUrl = "https://aqicn.org/city/vietnam/hanoi/us-embassy"
slackHookUrl = os.getenv("SLACK_HOOK")
userAgent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
response = requests.get(url).json()
try:
    slackPayload = {
        "attachments": [
            {
                "author_name": "Dự báo AQI 7 ngày tới",
                "fields": [
                    {
                        "title": "Ngày",
                        "short": True
                    },
                    {
                        "title": "AQI",
                        "short": True
                    }
                ]
            }
        ]
    }
    aqi = response["data"]["aqi"]
    time = response["data"]["time"]["s"]

    slackPayload["text"] = f"Chỉ số AQI của Hà Nội lúc {time} là {aqi}."

    responseForecast = requests.get(forecastUrl, headers={"User-Agent": userAgent}).text
    matches = re.search("var f=\\[(.*)\\];try {var div =", responseForecast)
    result = parse_data(matches.group(1))

    for day in result:
        slackPayload["attachments"].append({
            "color": get_color(day['max']),
            "fields": [
                {
                    "value": day["date"],
                    "short": True
                },
                {
                    "value": f"{day['min']}~{day['max']}",
                    "short": True
                }
            ],
        })

    res = requests.post(slackHookUrl, json.dumps(slackPayload))
    print(res.text)
    print(slackPayload)

except KeyError:
    print("Error")
