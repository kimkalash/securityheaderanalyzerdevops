from fastapi.testclient import TestClient
from main import app  # Make sure main.py contains: app = FastAPI()

client = TestClient(app)

def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert "security" in response.text.lower()
