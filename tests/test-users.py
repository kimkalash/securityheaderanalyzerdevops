from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_and_get_user():
    # Create a user
    response = client.post("/users/", json={
        "username": "testuser",
        "email": "test@example.com",
        "password_hash": "hashedpass"
    })
    assert response.status_code == 200
    user_data = response.json()
    assert "id" in user_data
    assert user_data["username"] == "testuser"

    # Fetch the user
    user_id = user_data["id"]
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 200
    assert get_response.json()["username"] == "testuser"
