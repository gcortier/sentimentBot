from fastapi.testclient import TestClient
from sentiment_bot_api import app

client = TestClient(app)

def test_root_route():
   response = client.get("/")
   assert response.status_code == 200
   assert response.json()["message"] == "Bienvenue sur l'API"


def test_chat_basic():
    response = client.post("/chat/", json={"prompt": "Hello how is going today ?"})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert isinstance(data["response"], str)
    assert len(data["response"]) > 0

def test_translate_basic():
    response = client.post("/translate/", json={"text": "Bonjour, comment ça va aujourdhui ?"})
    assert response.status_code == 200
    data = response.json()
    assert "translation" in data
    assert isinstance(data["translation"], str)
    assert len(data["translation"]) > 0

def test_nlptown_sentiment_high():
    response = client.post("/nlptown_sentiment/", json={"text": "I love this product!"})
    assert response.status_code == 200
    data = response.json()
    assert data["label"] == "5 stars"
    assert "label" in data
    assert data["label"] in ["1 star", "2 stars", "3 stars", "4 stars", "5 stars"]
    assert "score" in data
    
def test_nlptown_sentiment_medium():
    response = client.post("/nlptown_sentiment/", json={"text": "It's a raining day!"})
    assert response.status_code == 200
    data = response.json()
    assert data["label"] == "3 stars"
    assert "label" in data
    assert data["label"] in ["1 star", "2 stars", "3 stars", "4 stars", "5 stars"]
    assert "score" in data
    
    
def test_nlptown_sentiment_ultra_low():
    response = client.post("/nlptown_sentiment/", json={"text": "This is the worst experience of my life. I hate everything about it. Absolutely terrible, disgusting and disappointing."})
    assert response.status_code == 200
    data = response.json()
    assert data["label"] == "1 star"
    assert "label" in data
    assert data["label"] in ["1 star", "2 stars", "3 stars", "4 stars", "5 stars"]
    assert "score" in data
    
    
def test_nlptown_sentiment_weird():
    response = client.post("/nlptown_sentiment/", json={"text": "Ma mère et mon père sont morts dans d'atroces souffrance et j'ai gagné au Loto aujourd'hui"})
    assert response.status_code == 200
    data = response.json()
    assert data["label"] == "5 stars"
    assert "label" in data
    assert data["label"] in ["1 star", "2 stars", "3 stars", "4 stars", "5 stars"]
    assert "score" in data
