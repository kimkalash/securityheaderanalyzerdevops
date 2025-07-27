from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_add_header():
    # Create a user
    user_response = client.post("/users/", json={
        "username": "headeruser",
        "email": "header@example.com",
        "password_hash": "hashedpass"
    })
    user_id = user_response.json()["id"]

    # Create a scan
    scan_response = client.post(f"/scans/?user_id={user_id}&scan_url=https://test.com")
    scan_id = scan_response.json()["scan_id"]

    # Add a header result
    header_response = client.post(
        f"/headers/?scan_id={scan_id}&header_name=Content-Security-Policy&header_value=default-src"
    )
    assert header_response.status_code == 200
    data = header_response.json()
    assert data["header_name"] == "Content-Security-Policy"
