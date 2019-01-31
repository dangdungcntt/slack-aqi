import os
import aqi
import dotenv
import aqi_api
import slack_api

dotenv.load_dotenv()


def run(city, token, forecast_url, slack_hook_url):
    feed_data = aqi_api.feed(city, token)
    try:
        aqi_number = feed_data["data"]["aqi"]
        time_str = feed_data["data"]["time"]["s"]
        time_array = time_str.split(' ')
        time_array.reverse()
        time_str = ' '.join(time_array)

        slack_payload = {
            "text": f"Chỉ số AQI của Hà Nội lúc {time_str} là {aqi_number} ({aqi.get_instruction(aqi_number)})",
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

        result = aqi_api.get_forecast(forecast_url)

        for day in result:
            slack_payload["attachments"].append({
                "color": aqi.get_color(day['max']),
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

        res = slack_api.send_message(slack_hook_url, slack_payload)
        print(slack_payload)
        print(res)

        return [slack_payload, res]

    except KeyError:
        print("Error")


run(
    os.getenv("AQI_CITY"),
    os.getenv("AQI_TOKEN"),
    os.getenv("AQI_FORECAST_URL"),
    os.getenv("SLACK_HOOK")
)
