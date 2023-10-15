from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError, DataError
from model import db, Destination
import random

app = Blueprint('api', __name__)

VALID_FILTER_COLUMNS = [col.name for col in Destination.__table__.columns]


@app.route("/random")
def get_random_destination():
    all_destinations = db.session.query(Destination).all()
    random_destination = random.choice(all_destinations)
    return jsonify(destination=random_destination.to_dict())


@app.route("/all")
def get_all_destinations():
    all_destinations = db.session.query(Destination).order_by(Destination.id).all()
    return jsonify(destinations=[destination.to_dict() for destination in all_destinations])


@app.route("/recent")
def get_recent_destinations():
    recent_destinations = db.session.query(Destination).order_by(Destination.id.desc()).limit(3).all()

    if recent_destinations:
        return jsonify(destinations=[destination.to_dict() for destination in recent_destinations])
    else:
        return jsonify(error={"Not found": "No recent destinations found"})


@app.route("/search")
def search_destination():
    queries = request.args
    searching_filters = {}

    for key, value in queries.items():
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
def add_destination():
    data = request.json

    if any(field not in VALID_FILTER_COLUMNS for field in data):
        unexpected_fields = [field for field in data if field not in VALID_FILTER_COLUMNS]
        return jsonify(error=f"Unexpected fields in your request: {', '.join(unexpected_fields)}"), 400

    try:
        new_destination = Destination(**data)
        db.session.add(new_destination)
        db.session.commit()

    except IntegrityError as e:
        return jsonify(error="IntegrityError error: A constraint was violated. Check the following steps:"
                             "1. The following fields need to be defined: continent, country, city, description"
                             "2. Budget field should have a value of either 'affordable', 'moderate', or 'expensive'"
                             "3. The following field need to be strings (or NULL): picture, popular atractions"
                             "4. The other fields should have values between 0 and 5"), 400

    except DataError as e:
        return jsonify(error="Data error: " + str(e)), 500

    return jsonify(message="Destination added successfully", new_destination=new_destination.to_dict())


@app.route("/update_destination/<int:destination_id>", methods=["Patch"])
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
def delete_destination(destination_id):
    destination = Destination.query.get(destination_id)

    if not destination:
        return jsonify(error=f"Destination with the id {destination_id} was not found"), 404

    db.session.delete(destination)
    db.session.commit()

    return jsonify(message=f"Destination with ID {destination_id} has been deleted"), 200