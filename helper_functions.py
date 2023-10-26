from model import Destination, db
from flask_paginate import Pagination
from flask import request, jsonify
from datetime import datetime
from model import User
import random
import requests



def get_random_locations_for_continent(continent, num_locations=3):
    all_locations = db.session.query(Destination).filter_by(continent=continent).all()
    random.shuffle(all_locations)
    selected_locations = all_locations[:num_locations]

    return selected_locations



def get_pagination_and_page(per_page, total):
    page = int(request.args.get('page', 1))
    pagination = Pagination(page=page, per_page=per_page, total=total, record_name='destinations')

    return pagination, page



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



def is_valid_api_key(api_key):
    return db.session.query(User).filter_by(api_key=api_key).first() is not None



def require_valid_api_key(func):
    def decorated_function(*args, **kwargs):
        api_key = request.args.get("api_key")
        if not api_key or not is_valid_api_key(api_key):
            return jsonify(error="Invalid API key"), 403
        return func(*args, **kwargs)
    decorated_function.__name__ = func.__name__
    return decorated_function