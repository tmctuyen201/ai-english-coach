import pytest


def test_send_otp(client):
    response = client.post("/api/v1/auth/phone/send-otp", json={"phone": "+84912345678"})
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["phone"] == "+84912345678"


def test_verify_otp(client):
    # First send OTP
    client.post("/api/v1/auth/phone/send-otp", json={"phone": "+84912345678"})

    # Get the OTP from the in-memory store
    from app.api.v1.auth import otp_store
    otp = otp_store["+84912345678"]

    # Verify OTP
    response = client.post(
        "/api/v1/auth/phone/verify",
        json={"phone": "+84912345678", "otp": otp},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["access_token"].startswith("fake-jwt-token-")


def test_verify_wrong_otp(client):
    # First send OTP
    client.post("/api/v1/auth/phone/send-otp", json={"phone": "+84912345678"})

    # Verify with wrong OTP
    response = client.post(
        "/api/v1/auth/phone/verify",
        json={"phone": "+84912345678", "otp": "000000"},
    )
    assert response.status_code == 400
