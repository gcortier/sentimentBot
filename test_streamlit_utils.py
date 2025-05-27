import pytest
from app import get_sentiment_emoji

def test_get_sentiment_emoji():
    # Cas positif
    assert get_sentiment_emoji({"compound": 0.8}) == "😊"
    # Cas négatif
    assert get_sentiment_emoji({"compound": -0.8}) == "😞"
    # Cas neutre
    assert get_sentiment_emoji({"compound": 0.0}) == "😐"
    # Cas limite positif
    assert get_sentiment_emoji({"compound": 0.05}) == "😊"
    # Cas limite négatif
    assert get_sentiment_emoji({"compound": -0.05}) == "😞"
    # Cas valeur manquante
    assert get_sentiment_emoji({}) == "😐"
