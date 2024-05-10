import pytest
import server


@pytest.fixture(scope="module")
def client():
    server.app.config.update({"TESTING": True})
    with server.app.test_client() as client:
        yield client

@pytest.fixture
def mock_load_clubs(mocker):
    mock_data = [
        {
            "name": "Club1",
            "email": "club1@example.com",
            "points": "13"
        },
        {
            "name": "Club2",
            "email": "club2@example.com",
            "points": "5"
        },
        {
            "name": "Club3",
            "email": "club3@example.com",
            "points": "15"
        }
    ]

    mocker.patch("server.load_clubs", return_value=mock_data)
    server.clubs = server.load_clubs()
    yield

@pytest.fixture
def mock_load_competitions(mocker):
    mock_data = [
        {
            "name": "Comp1",
            "date": "2025-03-27 10:00:00",
            "number_of_places": "15"
        },
        {
            "name": "Comp2",
            "date": "2025-03-27 10:00:00",
            "number_of_places": "1"
        },
        {
            "name": "Comp3",
            "date": "2020-10-22 13:30:00",
            "number_of_places": "13"
        }
    ]

    mocker.patch("server.load_competitions", return_value=mock_data)
    server.competitions = server.load_competitions()
    yield