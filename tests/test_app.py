import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Arrange-Act-Assert pattern for each test

def test_get_activities():
    # Arrange
    # (No setup needed, just use the client)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_success():
    # Arrange
    activity = "Soccer Team"
    email = "testuser1@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Clean up
    client.delete(f"/activities/{activity}/signup?email={email}")

def test_signup_duplicate():
    # Arrange
    activity = "Soccer Team"
    email = "testuser2@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]
    # Clean up
    client.delete(f"/activities/{activity}/signup?email={email}")

def test_unregister_success():
    # Arrange
    activity = "Soccer Team"
    email = "testuser3@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Removed {email}" in response.json()["message"]

def test_unregister_not_found():
    # Arrange
    activity = "Soccer Team"
    email = "notregistered@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "not registered" in response.json()["detail"]
