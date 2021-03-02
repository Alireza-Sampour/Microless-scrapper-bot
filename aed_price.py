import requests
import json


def get_aed_price() -> int:
    URL = "https://hamyarandroid.com/api?t=currency"
    response = requests.get(url=URL)
    if response.status_code == 200:
        if json.loads(response.text)['ok'] is True:
            return int(str(json.loads(response.text)['list'][2]['price'])[:-1])
        else:
            print("Can't connect to web service.")
            return 0
    else:
        print(f"Can't connect, error code is: {response.status_code}")
        return 0
