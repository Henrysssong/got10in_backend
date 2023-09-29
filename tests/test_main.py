from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register_new_user():
    response = client.post("/register/", json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully!"}

def test_register_existing_user():
    response = client.post("/register/", json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already exists"}

# Add more tests for login, preferences, and other endpoints
