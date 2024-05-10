import server
import pytest
import html
import datetime

@pytest.mark.parametrize(
    "club_name, competition_name, places, expected_value",
    [
        (
            "Club1",
            "Comp1",
            10,
            "Great-booking complete !",
        ),
        (
            "Club2",
            "Comp1",
            6,
            "You don't have enough points",
        ),
        (
            "Club1",
            "Comp2",
            6,
            "Not enough places available.",
        ),
        (
            "Club1",
            "Comp1",
            -100,
            "You can't book a negative number of places."
        ),
        (
            "Club1",
            "Comp1",
            13,
            "You can't book more than 12 places.",
        ),
    ]
)
def test_purchase_places_errors(
    client,
    mock_load_clubs,
    mock_load_competitions,
    club_name,
    competition_name,
    places,
    expected_value):
    club = next(c for c in server.clubs if c["name"]== club_name)
    club_points_before = club["points"]
    response = client.post("/purchase-places", data={"club": club_name, "competition": competition_name, "places": places})

    assert response.status_code == 302
    assert response.location == f"/show-summary?club={club_name}"

    response = client.get(response.location, follow_redirects=True)
    assert response.status_code == 200
    response_data = html.unescape(response.data.decode("utf-8"))
    assert expected_value in response_data

    if expected_value == "Great-booking complete !":
        club = next(c for c in server.clubs if c["name"]== club_name)
        club_points_after = int(club["points"])
        expected_points = int(club_points_before) - places
        assert club_points_after == expected_points
        assert club_points_after >= 0

