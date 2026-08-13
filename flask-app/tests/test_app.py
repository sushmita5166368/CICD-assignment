from app import app

def test_health_success():
    client=app.test_client()
    response =client.get("/health")
    assert response.status_code ==200
    assert response.json["status"] =="healthy"

def test_home_success():
    client=app.test_client()
    response =client.get("/")
    assert response.status_code==200
    assert b"Hello from Flask!" in response.data

def test_invalid_route():
    client=app.test_client()
    response = client.get("/invalid")
    assert response.status_code == 404
    
