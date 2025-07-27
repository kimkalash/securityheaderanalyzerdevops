from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_list_scans():
    # Create a user first
    user_response = client.post("/users/", json={
        "username": "scanuser",
        "email": "scan@example.com",
        "password_hash": "hashedpass"
    })
    user_id = user_response.json()["id"]

    # Create a scan
    scan_response = client.post(f"/scans/?user_id={user_id}&scan_url=https://example.com")
    assert scan_response.status_code == 200
    scan_data = scan_response.json()
    assert scan_data["scan_url"] == "https://example.com"

    # Get user scans
    list_response = client.get(f"/scans/{user_id}")
    assert list_response.status_code == 200
    scans = list_response.json()
    assert any(s["scan_url"] == "https://example.com" for s in scans)
