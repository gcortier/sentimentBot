from nltk.sentiment import SentimentIntensityAnalyzer
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from loguru import logger
import os
import torch

#DialogGPT
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# Define the model repo
# https://cobusgreyling.medium.com/using-dialogpt-for-conversational-response-generation-559e2a13b191
model_name = "microsoft/DialoGPT-medium" 
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)


# Ajout du pipeline de traduction
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en")

# Ajout du pipeline pour le modèle nlptown/bert-base-multilingual-uncased-sentiment
nlptown_sentiment = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# === CONFIGURATION LOGURU ===
# Création dossier si n'existe pas
os.makedirs('logs', exist_ok=True)
logger.remove()  # Nettoie la config de base

logger.add(
    "logs/sentiment_bot_api.log",
   	rotation="500MB",            
   	retention="7 days",         
   	level="INFO",               
   	format="{time} {level} {message}"
)



sia = SentimentIntensityAnalyzer()
app = FastAPI()

class SentimentRequest(BaseModel):
    text: str

class ChatRequest(BaseModel):
    prompt: str
    history: list[str] = []  # Liste des messages précédents (alternance user/bot)

class ChatResponse(BaseModel):
    response: str

class TranslateRequest(BaseModel):
    text: str

class NlpTownSentimentRequest(BaseModel):
    text: str


@app.get("/")
async def root(request: Request):
    logger.info(f"Route '{request.url.path}' called by  {request.client.host}")
    return {"message": "Bienvenue sur l'API"}

# route pour le sentiment (pas utilisé dans le projet)
@app.post("/analyse_sentiment/")
def analyse_sentiment(req: SentimentRequest, request: Request):
    logger.info(f"Route '{request.url.path}' :: params is  {req.text}")
    try:
        sentiment = sia.polarity_scores(req.text)
        logger.info(f"Route '{request.url.path}' :: response is  {sentiment}")
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
    logger.info(f"Route '{request.url.path}' :: params is  {req.prompt}\nhistory: {req.history}")
    try:
        # Ajout de l'historique utilisateur uniquement sinon le bot "boucle" trop
        dialogue = ""
        for i, msg in enumerate(req.history):
            if i % 2 == 0:
                dialogue += msg + tokenizer.eos_token
        dialogue += req.prompt + tokenizer.eos_token
        
        # tokenisation et réponse du bot
        input_ids = tokenizer.encode(dialogue, return_tensors="pt")
        attention_mask = torch.ones_like(input_ids)
        output = model.generate(
            input_ids,
            max_length=200,
            pad_token_id=tokenizer.eos_token_id,
            attention_mask=attention_mask
        )
        response = tokenizer.decode(output[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
        logger.debug(f"/chat:: parse response: {req.prompt}\n dialogue: {dialogue}\nresponse: {response}")
        logger.info(f"/chat:: Dialogue response: {response}")
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

@app.post("/nlptown_sentiment/")
def analyse_nlptown_sentiment(req: NlpTownSentimentRequest, request: Request):
    logger.info(f"Route '{request.url.path}' :: params is  {req.text}")
    try:
        result = nlptown_sentiment(req.text)[0]
        logger.info(f"Résultat nlptown: {result}")
        return result
    except Exception as e:
        logger.error(f"Erreur analyse_nlptown_sentiment: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de l'analyse du sentiment (nlptown).")
