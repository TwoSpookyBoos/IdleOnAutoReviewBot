def test_valid_input(client):
    response = client.get('/', query_string=dict(player="scoli"))
    assert response.status_code == 200
