def test_get_current_user(client):
    response = client.get("/api/v1/users/me")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "phone" in data
    assert "name" in data
