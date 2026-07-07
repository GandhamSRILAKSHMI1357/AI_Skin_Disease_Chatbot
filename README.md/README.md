# AI Skin Disease Chatbot

## Description
An AI-powered chatbot that answers questions related to common skin diseases using Google's Gemini API and a custom knowledge base.

## Features
- AI-powered responses
- Domain-specific chatbot
- Knowledge base support
- Streamlit web interface
- Handles Acne, Eczema, Psoriasis, Vitiligo and Fungal Infection

## Technologies Used
- Python
- Streamlit
- Google Gemini API
- python-dotenv

## How to Run

1. Clone the repository

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Add your API key in `.env`

```text
GOOGLE_API_KEY=YOUR_API_KEY
```

4. Run the application

```bash
python -m streamlit run app.py
```