from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError, DataError
from flask_swagger_ui import get_swaggerui_blueprint
from helper_functions import get_weather, require_valid_api_key
from model import db, Destination
import country_converter as coco
import random


app = Blueprint('api', __name__)

SWAGGER_URL = '/api/docs'
API_URL = '/static/json/openapi.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Test application"
    }
)

VALID_FILTER_COLUMNS = [col.name for col in Destination.__table__.columns]


@app.route("/random", methods=["GET"])
@require_valid_api_key
def get_random_destination():
    all_destinations = db.session.query(Destination).all()
    random_destination = random.choice(all_destinations)
    return jsonify(destination=random_destination.to_dict())


@app.route("/all", methods=["GET"])
@require_valid_api_key
def get_all_destinations():
    all_destinations = db.session.query(Destination).order_by(Destination.id).all()
    return jsonify(destinations=[destination.to_dict() for destination in all_destinations])


@app.route("/recent", methods=["GET"])
@require_valid_api_key
def get_recent_destinations():
    recent_destinations = db.session.query(Destination).order_by(Destination.id.desc()).limit(3).all()

    if recent_destinations:
        return jsonify(destinations=[destination.to_dict() for destination in recent_destinations])
    else:
        return jsonify(error={"Not found": "No recent destinations found"})


@app.route("/search", methods=["GET"])
@require_valid_api_key
def search_destination():
    queries = request.args
    searching_filters = {}

    for key, value in queries.items():
        if key != "api_key":
            if key not in VALID_FILTER_COLUMNS:
                return jsonify(error={"Invalid Argument": f"{key} is not a valid filter column."}), 400
            else:
                searching_filters[key] = value

    all_destinations = Destination.query.filter_by(**searching_filters).all()

    if all_destinations:
        return jsonify(destinations=[destination.to_dict() for destination in all_destinations]), 200
    else:
        return jsonify(error={"Not found": "No destinations match the provided criteria"}), 404


@app.route("/add_destination", methods=["POST"])
@require_valid_api_key
def add_destination():
    data = request.json

    try:
        if any(field not in VALID_FILTER_COLUMNS for field in data):
            unexpected_fields = [field for field in data if field not in VALID_FILTER_COLUMNS]
            return jsonify(error=f"Unexpected fields in your request: {', '.join(unexpected_fields)}"), 400

        existing_destination = Destination.query.filter_by(city=data['city']).first()
        if existing_destination:
            return jsonify(error=f"{data['city']}' is already in our database"), 400

        # I know Oceania is a geographical region, but I chose it instead of Australia to be able to include
        # as many countries as possible. Australia will be automatically converted to Oceania.
        allowed_continents = ['Europe', 'North America', 'Asia', 'South America', 'Africa', 'Oceania']

        if data['continent'].lower() == "australia":
            data['continent'] = "Oceania"

        if data['continent'] not in allowed_continents:
            return jsonify(error=f"Invalid continent. Allowed continents: {', '.join(allowed_continents)}. Australia"
                                 f" will be automatically converted to Oceania"), 400

        country_code = coco.convert(data["country"], to="ISO3")
        if country_code == "not found":
            return jsonify(error=f"{data['country']} is not a valid country name. You can check a list of valid country"
                                 f"names here: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3")

        new_destination = Destination(**data)
        db.session.add(new_destination)
        db.session.commit()

    except KeyError as e:
        return jsonify(error="The following field needs to be defined: " + str(e)), 400

    except IntegrityError:
        return jsonify(error="IntegrityError error: A constraint was violated. Check the following steps: "
                             "1. Next fields are mandatory and should be of type string: "
                             "country, continent, description, city, popular_attractions  "
                             "2. Budget field should have a value of either 'affordable', 'moderate', or 'expensive'  "
                             "3. The following field needs to be string (or NULL): picture  "
                             "4. The other fields should have values between 0 and 5"), 400

    except DataError as e:
        return jsonify(error="Data error: " + str(e)), 500

    except Exception as e:
        return jsonify(error="An error has occured! Make sure to check the following steps: "                           
                             "1. Next fields are mandatory and should be of type string: "
                             "country, continent, description, city, popular_attractions  "
                             "2. Budget field should have a value of either 'affordable', 'moderate', or 'expensive'  "
                             "3. The following field needs to be string (or NULL): picture  "
                             "4. The other fields should have values(integers) between 0 and 5  "
                             "Error: " + str(e)), 500

    return jsonify(message="Destination added successfully", new_destination=new_destination.to_dict()), 201


@app.route("/update_destination/<int:destination_id>", methods=["PATCH"])
@require_valid_api_key
def update_destination(destination_id):
    destination = Destination.query.get(destination_id)
    data = request.get_json()

    if not destination:
        return jsonify(error=f"Destination with the id {destination_id} was not found"), 404

    for field, value in data.items():
        if field in VALID_FILTER_COLUMNS:
            setattr(destination, field, value)

    try:
        db.session.commit()
        return jsonify(message=f"Destination with ID {destination_id} updated successfully"), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(error="Data error: " + str(e)), 500


@app.route("/delete_destination/<int:destination_id>", methods=["DELETE"])
@require_valid_api_key
def delete_destination(destination_id):
    destination = Destination.query.get(destination_id)

    if not destination:
        return jsonify(error=f"Destination with the id {destination_id} was not found"), 404

    db.session.delete(destination)
    db.session.commit()

    return jsonify(message=f"Destination with ID {destination_id} has been deleted"), 200


@app.route('/get_weather/<city>', methods=['GET'])
@require_valid_api_key
def destination_weather(city):
    destination = db.session.query(Destination).filter_by(city=city).first()

    if destination:
        weather_data = get_weather(city, datetime_to_dayname=False)

        if not weather_data:
            return jsonify(error="Weather data not available for this destination"), 404

        return jsonify(weather_data)

    return jsonify(error="City not found in the database"), 404
