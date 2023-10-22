from model import Destination, db
from datetime import datetime
import random
import requests



def get_random_locations_for_continent(continent, num_locations=3):
    all_locations = db.session.query(Destination).filter_by(continent=continent).all()
    random.shuffle(all_locations)
    selected_locations = all_locations[:num_locations]

    return selected_locations


def get_weather(city, datetime_to_dayname=True):
    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?'
    data = {
        "unitGroup": "metric",
        "include": "days",
        "key": "EWQXWJWCG6ZKZBDXUNLZRZK6T",           # ENV VAR
        "contentType": "json",
        "iconSet": 'icons2'
    }

    response = requests.get(url=url, params=data)

    if response.status_code == 200:
        weather_info_dict = {}
        i = 0
        for day in response.json()['days']:

            if datetime_to_dayname:
                date = datetime.strptime(day['datetime'], '%Y-%m-%d')
                date = date.strftime('%a')

            else:
                date = day['datetime']

            temp = round(day['temp'])
            description = day['icon']
            if i == 7:
                break
            i += 1


            weather_info_dict[date] = {'temp': temp, 'description': description}

        return weather_info_dict

    else:
        print("POST request for visualcrossing API failed with status code:", response.status_code)