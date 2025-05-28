# Installation
## Génération de l'environnement virtuel en début de projet
`python -m venv .venv`

## Activation de l'environnement virtuel
- Windows :  `.venv\Scripts\Activate.ps1`
- macOS/Linux: `source .venv/bin/activate`

## installation des bibliothèques de chat bot
- `pip install transformers torch`
## installation des bibliothèques pour model NLP
- `pip install sentencepiece sacremoses`
- ## installation des bibliothèques pour l'API FastAPI et le client Streamlit
- `pip install nltk fastapi streamlit uvicorn requests pydantic loguru`
- ## installation des bibliothèques pour les tests unitaires
- `pip install pytest httpx`

### Téléchargement du lexique VADER :
- `python -c "import nltk; nltk.download('vader_lexicon')"`


### Génération requirements.txt à chaque installation de module
- `pip freeze > requirements.txt`

### ou directement : 
- `pip install -r requierements.txt`


## run server uvicorn :
- `uvicorn sentiment_api:app --host 127.0.0.1 --port 9000 --reload`

## lancer le client streamlit:
`streamlit run app.py`

## Lancer les tests
Pour exécuter les tests unitaires sur l'API FastAPI :

`pytest test_sentiment_api.py`

## Arborescence du projet

```
Mod0Bref1Topics/
├── .venv/                              # Environnement virtuel 
├── sentiment_api.py                    # API FastAPI pour l'analyse de sentiment
├── app.py                              # Application Streamlit pour l'interface utilisateur
├── requirements.txt                    # Liste des dépendances
├── logs/                               # Dossier pour les logs
│   ├── sentiment_api.log               # Log de l'API FastAPI
│   └── sentiment_streamlit.log         # Log de l'application Streamlit
├── notebook.ipynb                      # Jupyter notebook pour tester le modèle
├── readme.md                           # Ce fichier
```

=> https://github.com/gcortier/

## Documentations :
- [Streamlit Documentation](https://docs.streamlit.io/) 
- https://huggingface.co/microsoft/DialoGPT-medium
- https://huggingface.co/docs/transformers/installation
- https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment?library=transformers
- https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf