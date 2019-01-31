import json
import requests


def send_message(hook, payload):
    return requests.post(hook, json.dumps(payload)).text
