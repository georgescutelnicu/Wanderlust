from datetime import datetime, timedelta
from main import db, Destination
import os


headers = {
    "Authorization": os.environ['API_KEY']
}


def test_get_random_destinations(client):
    response = client.get(f"/api/random", headers=headers)
    destination_keys = len(Destination().to_dict().keys())
    response_keys = len(response.json['destination'].keys())

    assert response.status_code == 200
    assert "destination" in response.json
    assert destination_keys == response_keys


def test_get_all_destinations(client):
    response = client.get(f"/api/all", headers=headers)
    num_records_in_db = db.session.query(Destination).count()

    assert response.status_code == 200
    assert "destinations" in response.json
    assert len(response.json["destinations"]) == num_records_in_db


def test_get_recent_destinations(client):
    response = client.get(f"/api/recent", headers=headers)
    num_records_in_recent = len(response.json["destinations"])

    assert response.status_code == 200
    assert "destinations" in response.json
    assert num_records_in_recent == 3


def test_search_destination(client):
    response_200 = client.get(f"/api/search?continent=Europe&city=Bucharest", headers=headers)

    assert response_200.status_code == 200
    assert "destinations" in response_200.json

    response_400 = client.get(f"/api/search?Continent=Europe&City=Bucharest", headers=headers)

    assert response_400.status_code == 400
    assert "Invalid Argument" in response_400.json["error"]

    response_404 = client.get(f"/api/search?continent=Europeee&city=Bucharesttt", headers=headers)

    assert response_404.status_code == 404
    assert "Not found" in response_404.json["error"]


def test_destination_weather(client):
    response_200 = client.get(f"/api/get_weather/Bucharest", headers=headers)
    tomorrows_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    assert response_200.status_code == 200
    assert tomorrows_date in response_200.json

    response_404 = client.get(f"/api/get_weather/Bucharesttt", headers=headers)

    assert response_404.status_code == 404
    assert "City not found" in response_404.json["error"]
