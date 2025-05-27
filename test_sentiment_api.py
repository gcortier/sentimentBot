from fastapi.testclient import TestClient
from sentiment_api import app

client = TestClient(app)

def test_root_route():
   response = client.get("/")
   assert response.status_code == 200
   assert response.json()["message"] == "Bienvenue sur l'API"


# def test_analyse_sentiment_positive():
response = client.post("/analyse_sentiment/", json={"texte": "i'm happy"})
assert response.status_code == 200
data = response.json()
assert "pos" in data and data["pos"] > 0

# def test_analyse_sentiment_negative():
response = client.post("/analyse_sentiment/", json={"texte": "i'm sad"})
assert response.status_code == 200
data = response.json()
assert "neg" in data and data["neg"] > 0
