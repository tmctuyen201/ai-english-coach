def test_list_vocabulary(client):
    response = client.get("/api/v1/vocabulary")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_due_vocabulary(client):
    response = client.get("/api/v1/vocabulary/due")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
