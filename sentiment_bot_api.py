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


app = FastAPI()

class BaseResponse(BaseModel):
    response: str
    
class BaseRequest(BaseModel):
    text: str

class ChatRequest(BaseModel):
    prompt: str
    history: list[str] = []  # Liste des messages précédents (alternance user/bot)
    
class SentimentResponse(BaseModel):
    label: str
    score: float




@app.get("/",
    response_model=BaseResponse,
    summary="Route par defaut",
    description="Affiche un message 'Bienvenue sur l'API' pour vérifier que l'API fonctionne."
)
async def root(request: Request):
    logger.info(f"Route '{request.url.path}' called")
    return {"response": "Bienvenue sur l'API"}


@app.post("/chat/",
    response_model=BaseResponse,
    summary="Envoie d'un dialogue au chatbot (DialogGPT)",
    description="Génère une réponse du chatbot en tenant compte de l'historique de la conversation. L'historique doit être une liste alternant messages utilisateur et bot. Le prompt est le message utilisateur courant."
)
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

@app.post("/translate/",
          response_model=BaseResponse,
          summary="Traduction d'un texte en français vers l'anglais",
          description="Utilise le modèle Helsinki-NLP/opus-mt-fr-en pour traduire un texte en français vers l'anglais. Retourne la traduction."
)
def translate(req: BaseRequest, request: Request):
    logger.info(f"Route '{request.url.path}' :: params is  {req.text}")
    try:
        logger.info(f"Traduction requête: {req.text}")
        translation = translator(req.text)[0]['translation_text']
        logger.info(f"Traduction résultat: {translation}")
        return {"response": translation}
    except Exception as e:
        logger.error(f"Erreur traduction: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la traduction.")

@app.post("/nlptown_sentiment/",
    response_model=SentimentResponse,
    summary="Analyse le sentiment d'un texte en anglais",
    description="Analyse le sentiment d'un texte en anglais en utilisant le modèle nlptown/bert-base-multilingual-uncased-sentiment. Retourne un label et un score de sentiment."
)
def analyse_nlptown_sentiment(req: BaseRequest, request: Request):
    logger.info(f"Route '{request.url.path}' :: params is  {req.text}")
    try:
        result = nlptown_sentiment(req.text)[0]
        logger.info(f"Résultat nlptown: {result}")
        return result
    except Exception as e:
        logger.error(f"Erreur analyse_nlptown_sentiment: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de l'analyse du sentiment (nlptown).")
