import server

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
    assert response.status_code == 302
    assert response.location == "/"
    
    response = client.get(response.location, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"This email is invalid, try again." in response.data

def test_show_summary_get(client, mock_load_clubs):
    response = client.get("/show-summary?club=Club2")

    assert response.status_code == 200
    assert b"Welcome" in response.data

def test_book(client, mock_load_clubs, mock_load_competitions):
    response = client.get("/book/Comp1/Club1")

    assert response.status_code == 200
    assert b"How many places?" in response.data

def test_purchase_places_valid_request(client, mock_load_clubs, mock_load_competitions):
    response = client.post("/purchase-places", data={"club": "Club1", "competition": "Comp1", "places": "5"})
    
    assert response.status_code == 302
    assert response.location == "/show-summary?club=Club1"
    response = client.get(response.location, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Great-booking complete !" in response.data

def test_purchase_places_invalid_request(client, mock_load_clubs, mock_load_competitions):
    response = client.post("/purchase-places", data={"club": "Club1", "competition": "Comp1", "places": "55"})

    assert response.status_code == 302
    assert response.location == "/show-summary?club=Club1"
    
    response = client.get(response.location, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Something went wrong :" in response.data

