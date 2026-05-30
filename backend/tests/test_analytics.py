def test_get_progress(client):
    response = client.get("/api/v1/analytics/progress")
    assert response.status_code == 200
    data = response.json()
    assert "total_conversations" in data
    assert "total_xp" in data
    assert "current_level" in data
    assert "current_streak" in data
