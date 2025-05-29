# Projet 2 : Application conversationnelle avec traduction et analyse de sentiment

## Énoncé
Créez une application conversationnelle qui permet à l'utilisateur de dialoguer avec un chatbot. Pour chaque message de l'utilisateur et chaque réponse du chatbot, l'application doit :
- Afficher le message original.
- Afficher la traduction anglaise du message.
- Afficher le sentiment exprimé dans le message (positif, négatif, neutre).

## Actions réalisés :
 - Ajouts des logs et des tests unitaires
 - Gestion des bonnes pratiques pydantic pour description des routes API (Request / Response)
 - Test de pleinnnnns d'approche pour essayer de rendre le chat plus "humain"
 - Documentation
 - Clean

## Problemes rencontré :
- DialogGPT est très 'bête' et j'ai essayé surtout de trouver un moyen de le rendre le plus naturel possible.
La solution finale est d'historiser les dialogues de l'utilisateur  afin que la requete de chat ait un minimum de contexte. En ajoutant les messages précédents de l'utilisateur et du bot, le bot boucle trop en cas de répétition user /bot.
- J'ai essayé un LLM mais beaucoup trop lourd et je n'ai pas réussi à faire fonctionner finallement
(https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf)

# Installation
## Génération de l'environnement virtuel en début de projet
`python -m venv .venv`

## Activation de l'environnement virtuel
- Windows :  `.venv\Scripts\Activate.ps1`
- macOS/Linux: `source .venv/bin/activate`

## installation des bibliothèques de chat bot
`pip install transformers torch`
## installation des bibliothèques pour model NLP
`pip install sentencepiece sacremoses`
- ## installation des bibliothèques pour l'API FastAPI et le client Streamlit
`pip install nltk fastapi streamlit uvicorn requests pydantic loguru`
- ## installation des bibliothèques pour les tests unitaires
`pip install pytest httpx`

### Génération requirements.txt à chaque installation de module
`pip freeze > requirements.txt`

### ou directement : 
`pip install -r requierements.txt`

## lancer le client streamlit:
`streamlit run app.py`

## run server uvicorn :
`uvicorn sentiment_bot_api:app --host 127.0.0.1 --port 9000 --reload`

### Description des routes de l'API FastAPI :
=> http://127.0.0.1:9000/docs#/

### Lancer les tests
Pour exécuter les tests unitaires sur l'API FastAPI :
`pytest test_sentiment_bot_api.py`

# Arborescence du projet

```
sentimentBot/
├── .venv/                              # Environnement virtuel 
├── sentiment_bot_api.py                # API FastAPI pour l'analyse de sentiment
├── app.py                              # Application Streamlit pour l'interface utilisateur
├── requirements.txt                    # Liste des dépendances
├── logs/                               # Dossier pour les logs
│   ├── sentiment_bot_api.log           # Log de l'API FastAPI
│   └── app.log                         # Log de l'application Streamlit
├── readme.md                           # Ce fichier
```

=> https://github.com/gcortier/sentimentBot

# Documentations :
- [Streamlit Documentation](https://docs.streamlit.io/) 
- https://huggingface.co/microsoft/DialoGPT-medium
- https://huggingface.co/docs/transformers/installation
- https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment?library=transformers
- https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf
- https://cobusgreyling.medium.com/using-dialogpt-for-conversational-response-generation-559e2a13b191