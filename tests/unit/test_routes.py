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