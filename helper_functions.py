from flask import request, jsonify
from flask_paginate import Pagination
from model import Destination, User, db
import country_converter as coco
from datetime import datetime
import plotly.express as px
import plotly.offline as pyo
import requests
import random
import os


def get_random_locations_for_continent(continent, num_locations=3):
    """
        Get a random selection of locations from a specific continent.

        Args:
            continent (str): The continent to filter locations.
            num_locations (int): Number of locations to retrieve.

        Returns:
            list: List of randomly selected locations.
    """
    all_locations = db.session.query(Destination).filter_by(continent=continent).all()
    random.shuffle(all_locations)
    selected_locations = all_locations[:num_locations]

    return selected_locations


def get_pagination_and_page(per_page, total):
    """
        Get pagination object and current page number.

        Args:
            per_page (int): Number of items per page.
            total (int): Total number of items.

        Returns:
            Pagination object and current page number.
    """
    page = int(request.args.get('page', 1))
    pagination = Pagination(page=page, per_page=per_page, total=total, record_name='destinations')

    return pagination, page


def get_weather(city, datetime_to_dayname=True):
    """
        Get weather information for a specific city using visualcrossing API.

        Args:
            city (str): The city name.
            datetime_to_dayname (bool): Convert datetime to day name.

        Returns:
            dict: Weather information for the upcoming days.
    """
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


def get_info(country):
    """
        Get additional information about a country using dev.me API.

        Args:
            country (str): The country name.

        Returns:
            dict: Information about the country.
    """
    data = {}

    country_code = coco.convert(country, to="ISO2")
    url = f"https://api.dev.me/v1-get-country-details?code={country_code}"
    api_key = os.environ["DEV_API_KEY"]

    headers = {
        "Accept": "application/json",
        "x-api-key": api_key
    }

    response = requests.get(url, headers=headers).json()

    try:
        data["borders"] = ", ".join([coco.convert(country, to="name") for country in response["borders"]])
    except:
        data["borders"] = f"{country} has no neighboring countries!"

    data["currency"] = f"{list(response['currencies'])[0]} - " \
                       f"{response['currencies'][list(response['currencies'])[0]]['name']}"
    data["timezones"] = ", ".join([timezone for timezone in response["timezones"]])
    data["capital"] = ", ".join([capital for capital in response["capital"]])
    data["languages"] = ", ".join(response["languages"].values())
    data["subregion"] = response["subregion"]
    data["flag"] = response["flags"]["png"]

    return data


def get_map(visited_destinations, planned_to_visit_destinations):
    """
       Generate a choropleth map based on visited and planned-to-visit destinations.

       Args:
           visited_destinations (list): List of visited destinations.
           planned_to_visit_destinations (list): List of planned-to-visit destinations.

       Returns:
           str: HTML representation of the choropleth map.
    """
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

    fig.update_layout(autosize=True, margin=dict(l=0, r=0, b=0, t=0),
                      legend=dict(x=0.5, y=0.0, xanchor='center', yanchor='top', orientation='h'),
                      legend_title=dict(text=''))

    html_plot = pyo.plot(fig, output_type='div', auto_open=False, show_link=False)

    return html_plot


def get_title(visited_destinations, planned_to_visit_destinations):
    """
       Determine the user's title based on visited and planned-to-visit destinations.

       Args:
           visited_destinations (list): List of visited destinations.
           planned_to_visit_destinations (list): List of planned-to-visit destinations.

       Returns:
           str: User's title.
    """
    titles = {
        1: "Novice Explorer",
        2: "Epic Explorer",
        3: "Seasoned Adventurer",
        4: "Ultimate Pathfinder"
    }

    count_badges = 1

    if len(planned_to_visit_destinations) > 2:
        count_badges += 1

    if len(visited_destinations) > 4:
        count_badges += 1

    continents_visited = set(d.destination.continent for d in visited_destinations)

    if len(continents_visited) == 6:
        count_badges += 1

    return titles[count_badges]


def is_valid_api_key(api_key):
    """
        Check if the provided API key is valid.

        Args:
            api_key (str): The API key to validate.

        Returns:
            bool: True if the API key is valid, False otherwise.
    """
    return db.session.query(User).filter_by(api_key=api_key).first() is not None


def require_valid_api_key(func):
    """
        Decorator function to require a valid API key for a specific route.

        Args:
            func (function): The function to decorate.

        Returns:
            function: Decorated function with API key validation.
    """
    def decorated_function(*args, **kwargs):
        api_key = request.args.get("api_key")
        if not api_key or not is_valid_api_key(api_key):
            return jsonify(error="Invalid API key"), 403
        return func(*args, **kwargs)
    decorated_function.__name__ = func.__name__
    return decorated_function
