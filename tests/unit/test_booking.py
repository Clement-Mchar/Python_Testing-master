import server
import pytest
import html
import datetime
import flask

def test_points_count(client, mock_load_clubs, mock_load_competitions,):
    places = 10
    club = next(c for c in server.clubs if c["name"]== "Club1")
    competition = next(comp for comp in server.competitions if comp["name"] == "Comp1")
    club_points_before = club["points"]

    response = client.post("/purchase-places", data={"club": club["name"], "competition": competition["name"], "places": places})

    assert response.status_code == 302
    assert response.location == f"/show-summary?club={club['name']}"

    flash_messages = flask.get_flashed_messages(with_categories=False)

    assert "Great-booking complete !" in flash_messages

    response = client.get(response.location, follow_redirects=True)
    assert response.status_code == 200

    club = next(c for c in server.clubs if c["name"]== "Club1")
    club_points_after = int(club["points"])
    expected_points = int(club_points_before) - places

    assert club_points_after == expected_points
    assert club_points_after >= 0

def test_places_count(client, mock_load_clubs, mock_load_competitions,):
    places = 10
    club = next(c for c in server.clubs if c["name"]== "Club1")
    competition = next(comp for comp in server.competitions if comp["name"] == "Comp1")
    places_left = competition["number_of_places"]

    response = client.post("/purchase-places", data={"club": club["name"], "competition": competition["name"], "places": places})

    assert response.status_code == 302
    assert response.location == f"/show-summary?club={club['name']}"

    flash_messages = flask.get_flashed_messages(with_categories=False)

    assert "Great-booking complete !" in flash_messages

    response = client.get(response.location, follow_redirects=True)

    assert response.status_code == 200

    competition = next(comp for comp in server.competitions if comp["name"] == "Comp1")
    places_left_after = int(competition["number_of_places"])
    expected_places_left = int(places_left) - places

    assert places_left_after == expected_places_left
    assert places_left_after >= 0

def test_negative_places_number(client, mock_load_clubs, mock_load_competitions,):
    places = -100
    club = next(c for c in server.clubs if c["name"]== "Club1")
    competition = next(comp for comp in server.competitions if comp["name"] == "Comp1")

    response = client.post("/purchase-places", data={"club": club["name"], "competition": competition["name"], "places": places})

    assert response.status_code == 302
    assert response.location == f"/show-summary?club={club['name']}"

    flash_messages = flask.get_flashed_messages(with_categories=False)
    
    assert "You can't book a negative number of places." in flash_messages

def test_too_many_places_booked(client, mock_load_clubs, mock_load_competitions,):
    places = 13
    club = next(c for c in server.clubs if c["name"]== "Club1")
    competition = next(comp for comp in server.competitions if comp["name"] == "Comp1")

    response = client.post("/purchase-places", data={"club": club["name"], "competition": competition["name"], "places": places})

    assert response.status_code == 302
    assert response.location == f"/show-summary?club={club['name']}"

    flash_messages = flask.get_flashed_messages(with_categories=False)

    assert "You can't book more than 12 places." in flash_messages

def test_not_enough_places(client, mock_load_clubs, mock_load_competitions,):
    places = 6
    club = next(c for c in server.clubs if c["name"]== "Club1")
    competition = next(comp for comp in server.competitions if comp["name"] == "Comp2")

    response = client.post("/purchase-places", data={"club": club["name"], "competition": competition["name"], "places": places})

    assert response.status_code == 302
    assert response.location == f"/show-summary?club={club['name']}"

    flash_messages = flask.get_flashed_messages(with_categories=False)

    assert "Not enough places available." in flash_messages

def test_not_enough_points(client, mock_load_clubs, mock_load_competitions,):
    places = 10
    club = next(c for c in server.clubs if c["name"]== "Club2")
    competition = next(comp for comp in server.competitions if comp["name"] == "Comp1")

    response = client.post("/purchase-places", data={"club": club["name"], "competition": competition["name"], "places": places})

    assert response.status_code == 302
    assert response.location == f"/show-summary?club={club['name']}"

    flash_messages = flask.get_flashed_messages(with_categories=False)

    assert "You don't have enough points." in flash_messages

def test_purchase_places_passed_date(client, mock_load_clubs, mock_load_competitions):
    now = datetime.datetime.now()
    competition = next(comp for comp in server.competitions if comp["name"] == "Comp3")
    competition_date = datetime.datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S")
    response = client.post("/purchase-places", data={"club": "Club1", "competition": "Comp3", "places": "10"})
    flash_messages = flask.get_flashed_messages(with_categories=False)

    assert now > competition_date
    assert "You can't purchase places to an already passed competition." in flash_messages
    assert response.status_code == 302
    assert response.location == f"/show-summary?club=Club1"

def test_invalid_places_input(client, mock_load_clubs, mock_load_competitions):
    response = client.post("/purchase-places", data={"club": "Club1", "competition": "Comp1", "places": "abc"})

    assert response.status_code == 200

    flash_messages = flask.get_flashed_messages(with_categories=False)
    assert "Please enter a valid number of places." in flash_messages