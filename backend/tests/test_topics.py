def test_list_topics(client):
    response = client.get("/api/v1/topics")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    for topic in data:
        assert "id" in topic
        assert "title_en" in topic
        assert "title_vi" in topic
        assert "level" in topic
        assert "icon" in topic
