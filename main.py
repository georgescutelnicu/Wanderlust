from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError, DataError
from model import db, Destination
from api import app as api_blueprint
from api import swaggerui_blueprint
import random


app = Flask(__name__)
app.register_blueprint(api_blueprint, url_prefix='/api')
app.register_blueprint(swaggerui_blueprint)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/travel'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.sort_keys = False

db.init_app(app)


VALID_FILTER_COLUMNS = [col.name for col in Destination.__table__.columns]


def get_random_locations_for_continent(continent, num_locations=3):
    all_locations = db.session.query(Destination).filter_by(continent=continent).all()
    random.shuffle(all_locations)
    selected_locations = all_locations[:num_locations]

    return selected_locations


@app.route("/")
def home():
    continents = ['Europe']#, 'North America', 'Asia', 'South America', 'Africa', 'Australia']
    continent_locations = {continent: get_random_locations_for_continent(continent) for continent in continents}

    return render_template("index.html", continent_locations=continent_locations)







if __name__ == '__main__':
    app.run(debug=True)