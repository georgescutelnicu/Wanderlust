from flask import request, jsonify
from flask_paginate import Pagination
from model import Destination, User, db
from datetime import datetime
import requests
import random
import os


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
        "key": os.environ['WEATHER_API_KEY'],
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


def get_map(visited_destinations, planned_to_visit_destinations):
    visited = [coco.convert(d.destination.country, to="ISO3") for d in visited_destinations]
    plan_to_visit = [coco.convert(d.destination.country, to="ISO3") for d in planned_to_visit_destinations]

    all_countries = visited + plan_to_visit
    status = ["Visited"] * len(visited) + ["Plan to Visit"] * len(plan_to_visit)
    data = {
        "Country": all_countries,
        "Status": status
    }

    fig = px.choropleth(
        data,
        locations="Country",
        color="Status",
        color_discrete_map={"Visited": "green", "Plan to Visit": "blue"}
    )

    fig.update_layout(autosize=True, margin=dict(l=0, r=0, b=0, t=0), legend=dict(x=0.5, y=0.0, xanchor='center', yanchor='top',  orientation='h'),
                      legend_title=dict(text=''))

    html_plot = pyo.plot(fig, output_type='div', auto_open=False, show_link=False)

    return html_plot


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
