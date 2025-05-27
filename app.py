import streamlit as st
import requests
import os
from loguru import logger

st.title("Chatbot multilingue (API FastAPI)")

API_URL = "http://127.0.0.1:8000"


# === CONFIGURATION LOGURU ===
# Création dossier si n'existe pas
os.makedirs('logs', exist_ok=True)
logger.remove()  # Nettoie la config de base
logger.add(
   	"logs/app.log", # use "logs/app{time}.log" to use with timestamp
	# Nouveau fichier tous les 500 Mo
   	rotation="500 MB",            
	# Conserver les logs 7 jours
   	retention="7 days",         
# Compresser les anciens logs 
   	# compression="zip",          
# Niveau info
   	# level="INFO",               
   	level="DEBUG",               
   	format="{time} {level} {message}"
)
logger.debug(f"Starting project sentiment_bot")



# response = requests.post(
#     f"{API_URL}/analyse_sentiment/",
#     json={"text": "Bonjour, comment ça va aujourd'hui ?"})
# # Lève une exception pour les codes d'erreur HTTP (4xx ou 5xx)
# response.raise_for_status() 

# sentiment = response.json()



if "history" not in st.session_state:
    st.session_state.history = []


def classify_nlptown_label_emoji(label: str) -> str:
    logger.debug(f"classify_nlptown_label_emoji:: {label}")
    if label in ["1 star", "2 stars"]:
        return "😞"  # négatif
    elif label == "3 stars":
        return "😐"  # neutre
    else:  # "4 stars" ou "5 stars"
        return "😊"  # positif



with st.form("chat_form", clear_on_submit=True):
    user_message = st.text_input("Votre message :", "")
    submitted = st.form_submit_button("Envoyer")

if submitted and user_message:
    # Traduction utilisateur
    r = requests.post(f"{API_URL}/translate/", json={"text": user_message})
    logger.info(f"Texte à analyser: {user_message} ___ result : {r}")
    user_translation = r.json()["translation"]
    
    # Sentiment utilisateur
    r = requests.post(f"{API_URL}/nlptown_sentiment/", json={"text": user_message})
    user_sentiment = r.json()
    user_emoji = classify_nlptown_label_emoji(user_sentiment["label"])
    
    # Réponse chatbot
    past = st.session_state.history[-1]["bot_past"] if st.session_state.history else None
    r = requests.post(f"{API_URL}/chat/", json={"prompt": user_message})
    chat_response = r.json()
    bot_reply = chat_response.get("response", "")
    bot_past = chat_response.get("bot_past", None)
    
    # Sentiment bot
    r = requests.post(f"{API_URL}/nlptown_sentiment", json={"text": bot_reply})
    bot_sentiment = r.json()
    bot_emoji = classify_nlptown_label_emoji(bot_sentiment["label"])
    
    # Traduction bot
    # r = requests.post(f"{API_URL}/translate", json={"text": bot_reply})
    # bot_translation = r.json()["translation"]
    
    
    
    st.session_state.history.append({
        "user": user_message,
        "user_translation": f"{user_translation} {user_emoji}",
        "user_sentiment": user_sentiment,
        "bot": f"{bot_reply} {bot_emoji}",
        # "bot_translation": bot_translation,
        "bot_sentiment": bot_sentiment,
        "bot_past": bot_past
    })

for turn in st.session_state.history:
    st.markdown("**Utilisateur :**")
    st.write(turn["user"])
    st.markdown(f"*Traduction EN :* {turn['user_translation']}")
    st.markdown(f"*Sentiment :* {turn['user_sentiment']}")
    st.markdown("**Chatbot :**")
    st.write(turn["bot"])
    st.markdown(f"*Sentiment :* {turn['bot_sentiment']}")
    # st.markdown(f"*Traduction EN :* {turn['bot_translation']}")
    st.markdown("---")