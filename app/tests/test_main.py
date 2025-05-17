from fastapi.testclient import TestClient
from main import app  # ajuste si ton main.py est ailleurs
import pytest

client = TestClient(app)

def test_root_endpoint_exists():
    response = client.get("/schools")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_school_by_uai_not_found():
    response = client.get("/schools/INVALID_UAI")
    assert response.status_code == 404
    assert response.json()["detail"] == "École non trouvée"

def test_school_by_uai_valid():
    # ⚠️ Assure-toi qu'un UAI connu est présent en BDD avant de lancer ce test
    known_uai = "9710546S"  # à adapter
    response = client.get(f"/schools/{known_uai}")
    assert response.status_code == 200
    assert response.json()["uai"] == known_uai

def test_schools_by_ips_range():
    response = client.get("/schools/ips?min_ips=90&max_ips=100")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for school in response.json():
        assert 90 <= school["ips"] <= 100

def test_login_fail():
    response = client.post("/login", json={"username": "wrong", "password": "wrong"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Identifiants invalides"

def test_login_success_and_token():
    # ⚠️ Assure-toi que cet utilisateur existe dans la BDD
    response = client.post("/login", json={"username": "admin", "password": "1234"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


