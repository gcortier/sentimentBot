import streamlit as st
import requests

st.title("Chatbot multilingue (API FastAPI)")

API_URL = "http://127.0.0.1:9000"

if "history" not in st.session_state:
    st.session_state.history = []

with st.form("chat_form", clear_on_submit=True):
    user_message = st.text_input("Votre message :", "")
    submitted = st.form_submit_button("Envoyer")

if submitted and user_message:
    # Traduction utilisateur
    # r = requests.post(f"{API_URL}/translate", json={"text": user_message})
    # user_translation = r.json()["translation"]
    
    # Sentiment utilisateur
    # r = requests.post(f"{API_URL}/analyse_sentiment", json={"text": user_message})
    # user_sentiment = r.json()["analyse_sentiment"]
    
    # Réponse chatbot
    past = st.session_state.history[-1]["bot_past"] if st.session_state.history else None
    r = requests.post(f"{API_URL}/chat", json={"user_message": user_message, "past": past})
    chat_response = r.json()
    bot_reply = chat_response.get("bot_reply", "")
    bot_past = chat_response.get("bot_past", None)
    
    # Traduction bot
    # r = requests.post(f"{API_URL}/translate", json={"text": bot_reply})
    # bot_translation = r.json()["translation"]
    
    # Sentiment bot
    # r = requests.post(f"{API_URL}/analyse_sentiment", json={"text": bot_reply})
    # bot_sentiment = r.json()["sentiment"]
    
    
    st.session_state.history.append({
        "user": user_message,
        # "user_translation": user_translation,
        # "user_sentiment": user_sentiment,
        "bot": bot_reply,
        # "bot_translation": bot_translation,
        # "bot_sentiment": bot_sentiment,
        "bot_past": bot_past
    })

for turn in st.session_state.history:
    st.markdown("**Utilisateur :**")
    st.write(turn["user"])
    # st.markdown(f"*Traduction EN :* {turn['user_translation']}")
    # st.markdown(f"*Sentiment :* {turn['user_sentiment']}")
    st.markdown("**Chatbot :**")
    st.write(turn["bot"])
    # st.markdown(f"*Traduction EN :* {turn['bot_translation']}")
    # st.markdown(f"*Sentiment :* {turn['bot_sentiment']}")
    st.markdown("---")