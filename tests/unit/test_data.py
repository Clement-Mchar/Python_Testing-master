import server

def test_load_clubs_with_mock(mock_load_clubs):
    server.clubs = server.load_clubs()
    assert server.clubs == [
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

def test_load_competitions_with_mock(mock_load_competitions):

    server.competitions = server.load_competitions()
    assert server.competitions == [
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
