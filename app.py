import streamlit as st
import requests
import os
from loguru import logger

st.title("Chatbot multilingue (API FastAPI)")

# FastApi URL
API_URL = "http://127.0.0.1:9000"


# === CONFIGURATION LOGURU ===
# création dossier si n'existe pas
os.makedirs('logs', exist_ok=True)
logger.remove()  # Nettoie la config de base
logger.add(
   	"logs/app.log",
   	rotation="500 MB",            
   	retention="7 days",         
    # compression="zip",                  
   	level="INFO",               
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


def display_chat(history):
    # Affiche les dialogues du plus récent au plus ancien
    for dialog in reversed(history):
        st.markdown("**Utilisateur :**")
        st.write(dialog["user"])
        st.markdown(f"*Traduction EN :* {dialog['user_translation']} {dialog['user_emoji']}")
        st.markdown(f"*Sentiment :* {dialog['user_sentiment']}")
        st.markdown("**Chatbot :**")
        st.write(f"{dialog['bot']} {dialog['bot_emoji']}")
        st.markdown(f"*Sentiment :* {dialog['bot_sentiment']}")
        st.markdown("---")


with st.form("chat_form", clear_on_submit=True):
    user_message = st.text_input("Votre message :", "")
    submitted = st.form_submit_button(">Envoyer")


if submitted and user_message:
    # user_message => english
    r = requests.post(f"{API_URL}/translate/", json={"text": user_message})
    user_translation = r.json()["translation"]
    logger.info(f"Texte à analyser: {user_message} ___ result : {user_translation}")
    
    # evaluation user_translation
    r = requests.post(f"{API_URL}/nlptown_sentiment/", json={"text": user_translation})
    user_sentiment = r.json()
    user_emoji = classify_nlptown_label_emoji(user_sentiment["label"])
    
    # ajout historic pour rendre le bot plus contextuel
    history = []
    for turn in st.session_state.history:
        history.append(turn["user_translation"])
        history.append(turn["bot"])
        
    # chat avec le bot
    r = requests.post(f"{API_URL}/chat/", json={"prompt": user_translation, "history": history})
    chat_response = r.json()
    bot_reply = chat_response.get("response", "")
    
    # evaluation du sentiment bot
    r = requests.post(f"{API_URL}/nlptown_sentiment", json={"text": bot_reply})
    bot_sentiment = r.json()
    bot_emoji = classify_nlptown_label_emoji(bot_sentiment["label"])
    

    st.session_state.history.append({
        "user": user_message,
        "user_translation": f"{user_translation}",
        "user_emoji": user_emoji,
        "user_sentiment": user_sentiment,
        "bot": f"{bot_reply}",
        "bot_sentiment": bot_sentiment,
        "bot_emoji": bot_emoji
    })

# Affichage de l'historique
display_chat(st.session_state.history)