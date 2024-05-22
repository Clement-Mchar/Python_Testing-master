import server
import html
import flask

def test_index_route(client):
    url = "/"
    response = client.get(url)

    assert b"GUDLFT Registration" in response.data
    assert response.status_code == 200

def test_show_summary_post_valid_request(client, mock_load_clubs):
    response = client.post("/show-summary", data={"email":"club1@example.com"})

    assert response.status_code == 200

def test_show_summary_post_invalid_request(client, mock_load_clubs):
    response = client.post("/show-summary", data={"email": "invalid@example.com"})
    flash_messages = flask.get_flashed_messages(with_categories=False, category_filter=())
    
    assert response.status_code == 302
    assert "This email is invalid, try again." in flash_messages

def test_show_summary_get_valid_request(client, mock_load_clubs):
    response = client.get("/show-summary?club=Club2")

    assert response.status_code == 200
    assert b"Welcome" in response.data

def test_show_summary_get_invalid_request(client, mock_load_clubs):
    response = client.get("/show-summary?club=Clubthatdoesnotexist")

    assert response.status_code == 404
    assert b"Please check the URL and try again." in response.data

def test_book_valid_url(client, mock_load_clubs, mock_load_competitions):
    response = client.get("/book/Comp1/Club1")

    assert response.status_code == 200
    assert b"How many places?" in response.data

def test_book_invalid_url(client, mock_load_clubs, mock_load_competitions):
    response = client.get("/book/Comp1/Clubthatdoesnotexist")

    assert response.status_code == 404
    assert b"Please check the URL and try again." in response.data

def test_purchase_places_valid_request(client, mock_load_clubs, mock_load_competitions):
    response = client.post("/purchase-places", data={"club": "Club1", "competition": "Comp1", "places": "5"})
    
    assert response.status_code == 302
    flash_messages= flask.get_flashed_messages(with_categories=False, category_filter=())
    assert "Great-booking complete !" in flash_messages

def test_purchase_places_invalid_request(client, mock_load_clubs, mock_load_competitions):
    response = client.post("/purchase-places", data={"club": "Club1", "competition": "Comp1", "places": "55"})
    flash_messages= flask.get_flashed_messages(with_categories=False, category_filter=())
    assert response.status_code == 302
    assert "Something went wrong :" in flash_messages

def test_logout_route(client):
    response = client.get("/logout")

    assert response.status_code == 302
    assert response.location == "/"

def test_points_display(client, mock_load_clubs):
    response = client.get("/points_display")

    assert response.status_code == 200
    for club in server.clubs :
        response_data = html.unescape(response.data.decode("utf-8"))
        assert club["points"] in response_data
    
def test_page_not_found(client):
    response = client.get("/invalid_adress")

    assert response.status_code == 404
    assert b"404" in response.data
