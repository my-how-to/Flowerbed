from fastapi.testclient import TestClient
from main import app

# Initialize a clean, database-free testing client instance
client = TestClient(app)

def test_read_root_endpoint():
    """
    Validates that the root endpoint is alive and returns the correct 
    service identity greeting payload without hitting any database tables.
    """
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert "identity" in data
    assert "Smart Flowerbed" in data["identity"]
