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


def test_add_destination(client):
    data = {
        "city": "Bucharest",
        "continent": "Europe",
        "country": "Unknown",
        "description": "A beautiful destination",
        "popular_attractions": "Attraction A, Attraction B",
    }

    response_400 = client.post(f"/api/add_destination", json=data, headers=headers)

    assert response_400.status_code == 400
    assert f"{data['city']} is already in our database" in response_400.json["error"]

    data["city"] = 123

    response_500 = client.post(f"/api/add_destination", json=data, headers=headers)

    assert response_500.status_code == 500
    assert "An error has occurred!" in response_500.json["error"]

    db.session.rollback()
    data["city"] = "Arad42"

    response_400 = client.post(f"/api/add_destination", json=data, headers=headers)

    assert response_400.status_code == 400
    assert f"{data['country']} is not a valid country name" in response_400.json["error"]

    data["country"] = "Romania"

    response_201 = client.post(f"/api/add_destination", json=data, headers=headers)

    assert response_201.status_code == 201
    assert "Destination added successfully" in response_201.json["message"]


def test_update_destination(client):
    destination_id = Destination.query.order_by(Destination.id.desc()).first().id

    data = {
        "country": "XYZ",
    }

    response_400 = client.patch(f'/api/update_destination/{destination_id}', json=data, headers=headers)

    assert response_400.status_code == 400
    assert "not a valid country name" in response_400.json["error"]

    data = {
        "continent": "XYZ"
    }

    response_400 = client.patch(f'/api/update_destination/{destination_id}', json=data, headers=headers)

    assert response_400.status_code == 400
    assert "Invalid continent" in response_400.json["error"]

    data = {
        "popular_attractions": "Attraction X, Attraction Y, Attraction Z",
        "hiking": 5,
        "budget": "affordable"
    }

    response_200 = client.patch(f'/api/update_destination/{destination_id}', json=data, headers=headers)

    assert response_200.status_code == 200
    assert f"Destination with ID {destination_id} updated successfully" in response_200.json["message"]


def test_delete_destination(client):
    destination_id = Destination.query.order_by(Destination.id.desc()).first().id + 1

    response_404 = client.delete(f"/api/delete_destination/{destination_id}", headers=headers)

    assert response_404.status_code == 404
    assert f"Destination with ID {destination_id} was not found" in response_404.json["error"]

    destination_id -= 1

    response_204 = client.delete(f"/api/delete_destination/{destination_id}", headers=headers)

    assert response_204.status_code == 204

