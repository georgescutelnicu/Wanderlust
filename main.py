from flask import Flask, render_template, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError, DataError
from model import db, Destination
from api import app as api_blueprint
from api import swaggerui_blueprint
from helper_functions import get_random_locations_for_continent, get_weather, get_pagination_and_page

import random


app = Flask(__name__)
app.register_blueprint(api_blueprint, url_prefix='/api')
app.register_blueprint(swaggerui_blueprint)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/travel'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.sort_keys = False

db.init_app(app)


VALID_FILTER_COLUMNS = [col.name for col in Destination.__table__.columns]
PER_PAGE = 10



@app.route("/")
def home():
    continents = ['Europe', 'North America', 'Asia', 'South America', 'Africa', 'Oceania']
    continent_locations = {continent: get_random_locations_for_continent(continent) for continent in continents}

    return render_template("index.html", continent_locations=continent_locations)


@app.route("/all")
def get_all_destinations():
    all_destinations = db.session.query(Destination).all()

    pagination, page = get_pagination_and_page(PER_PAGE, len(all_destinations))
    destinations_on_page = all_destinations[(page - 1) * PER_PAGE:page * PER_PAGE]

    return render_template("all.html", all_destinations=destinations_on_page, pagination=pagination)


@app.route("/all/<continent>")
def get_all_destinations_by_continent(continent):
    allowed_continents = ['Europe', 'North America', 'Asia', 'South America', 'Africa', 'Oceania']

    if continent not in allowed_continents:
        return render_template("404.html")

    all_destinations = db.session.query(Destination).filter_by(continent=continent).all()

    pagination, page = get_pagination_and_page(PER_PAGE, len(all_destinations))
    destinations_on_page = all_destinations[(page - 1) * PER_PAGE:page * PER_PAGE]

    return render_template("all.html", all_destinations_continent=destinations_on_page, pagination=pagination, continent=continent)


@app.route("/latest")
def get_latest_destinations():
    latest_destinations = db.session.query(Destination).order_by(Destination.id.desc()).limit(5).all()
    return render_template("latest.html", latest_destinations=latest_destinations)


@app.route("/most_visited")
def get_most_visited():
    top_cities = ["London", "Singapore", "Paris", "Dubai", "New York City", "Bangkok", "Istanbul", "Antalya", "Mumbai",
              "Rome", "Tokyo", "Taipei", "Guangzhou", "Prague", "Seoul"]
    existing_cities = []

    for city in top_cities:
        destination = Destination.query.filter_by(city=city).first()
        if destination:
            existing_cities.append(destination)

    pagination, page = get_pagination_and_page(PER_PAGE, len(existing_cities))
    destinations_on_page = existing_cities[(page - 1) * PER_PAGE:page * PER_PAGE]

    return render_template("most_visited.html", most_visited_destinations=destinations_on_page, pagination=pagination)


@app.route("/<city>")
def display_city(city):
    destination = Destination.query.filter_by(city=city).first()

    weather = get_weather(city)

    if destination:
        return render_template("city.html", destination=destination, weather=weather)
    else:
        return render_template("404.html")


@app.route("/random")
def get_random_destination():
    all_destinations = db.session.query(Destination).all()
    random_destination = random.choice(all_destinations)
    return redirect(f'/{random_destination.city}')


@app.route("/about")
def about():
    return render_template("about.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")



if __name__ == '__main__':
    app.run(debug=True)