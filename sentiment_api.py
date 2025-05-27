from nltk.sentiment import SentimentIntensityAnalyzer
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from loguru import logger
import os

#DialogGPT
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline


import torch

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# Ajout du pipeline de traduction
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en")

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

class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    response: str

class TranslateRequest(BaseModel):
    text: str

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

@app.post("/chat/", response_model=ChatResponse)
def chat(req: ChatRequest, request: Request):
    logger.info(f"Route '{request.url.path}' :: params is  {req.prompt}")
    try:
        logger.info(f"Dialogue test prompt: {req.prompt}")
        input_ids = tokenizer.encode(req.prompt + tokenizer.eos_token, return_tensors="pt")
        output = model.generate(input_ids, max_length=100)
        response = tokenizer.decode(output[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
        logger.info(f"Dialogue test response: {response}")
        return {"response": response}
    except Exception as e:
        logger.error(f"Erreur /chat: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors du test dialogGPT.")

@app.post("/translate/")
def translate(req: TranslateRequest, request: Request):
    logger.info(f"Route '{request.url.path}' :: params is  {req.text}")
    try:
        logger.info(f"Traduction requête: {req.text}")
        translation = translator(req.text)[0]['translation_text']
        logger.info(f"Traduction résultat: {translation}")
        return {"translation": translation}
    except Exception as e:
        logger.error(f"Erreur traduction: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la traduction.")