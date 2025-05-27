from nltk.sentiment import SentimentIntensityAnalyzer
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from loguru import logger
import os

#DialogGPT
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# === CONFIGURATION LOGURU ===
# Création dossier si n'existe pas
os.makedirs('logs', exist_ok=True)
logger.remove()  # Nettoie la config de base

logger.add(
	# Fichier avec timestamp
    "logs/sentiment_api.log", # use "logs/sentiment_api_{time}.log" to use with timestamp
	# Nouveau fichier tous les 10 Mo
   	rotation="500MB",            
	# Conserver les logs 7 jours
   	retention="7 days",         
# Compresser les anciens logs 
   	# compression="zip",          
# Niveau minimal 
   	level="INFO",               
   	format="{time} {level} {message}"
)



sia = SentimentIntensityAnalyzer()
app = FastAPI()

class Texte(BaseModel):
    texte: str

@app.get("/")
async def root(request: Request):
    logger.info(f"Route '{request.url.path}' called by  {request.client.host}")
    return {"message": "Bienvenue sur l'API"}


@app.post("/analyse_sentiment/")
def analyse_sentiment(texte_object: Texte):
    try:
        logger.info(f"Requête reçue: {texte_object}")
        sentiment = sia.polarity_scores(texte_object.texte)
        logger.info(f"Résultat: {sentiment}")
        return {
            "neg": sentiment["neg"],
            "neu": sentiment["neu"],
            "pos": sentiment["pos"],
            "compound": sentiment["compound"],
        }
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de l'analyse du sentiment.")