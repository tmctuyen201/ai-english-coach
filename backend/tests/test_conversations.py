def test_start_conversation(client):
    response = client.post(
        "/api/v1/conversations/start",
        json={"topic_id": "daily-routine", "name": "Test User"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert "ai_greeting" in data


def test_get_conversation(client):
    # Start a conversation
    start_resp = client.post(
        "/api/v1/conversations/start",
        json={"topic_id": "daily-routine", "name": "Test User"},
    )
    session_id = start_resp.json()["session_id"]

    # Get conversation
    response = client.get(f"/api/v1/conversations/{session_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == session_id
    assert data["status"] == "active"


def test_end_conversation(client):
    # Start a conversation
    start_resp = client.post(
        "/api/v1/conversations/start",
        json={"topic_id": "daily-routine", "name": "Test User"},
    )
    session_id = start_resp.json()["session_id"]

    # End conversation
    response = client.post(f"/api/v1/conversations/{session_id}/end")
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == session_id
    assert data["status"] == "completed"
    assert "overall_score" in data
