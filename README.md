# AI Skin Disease Chatbot

A Streamlit educational chatbot about common skin conditions. It uses the repository's local knowledge files for basic answers and can use Google's Gemini API when a key is configured.

> This project is for education only. It does not diagnose skin conditions or replace medical advice.

## Features

- Streamlit web interface
- Works without an API key using the local knowledge base
- Optional Gemini-generated answers when GOOGLE_API_KEY is configured
- Local fallback if Gemini is unavailable
- Supports information in the knowledge files for acne, eczema, psoriasis, vitiligo, and fungal infections
- No real API key is stored in this public repository

## Project structure

~~~text
AI_Skin_Disease_Chatbot/
├── app.py
├── requirements.txt
├── README.md
└── knowledge/
    ├── acne.txt
    ├── eczema.txt
    ├── psoriasis.txt
    ├── vitiligo.txt
    └── fungal_infection.txt
~~~

## Run locally

1. Install Python 3.10 or newer.
2. Open a terminal in the repository folder.
3. Install the small set of required packages:

   ~~~bash
   pip install -r requirements.txt
   ~~~

4. Start the app:

   ~~~bash
   streamlit run app.py
   ~~~

The app works in local knowledge mode without an API key.

## Enable Gemini locally (optional)

Create a file at .streamlit/secrets.toml and put your own key in it:

~~~toml
GOOGLE_API_KEY = "paste_your_own_key_here"
~~~

Restart the app after adding the key. Do not commit secrets.toml or a real key to GitHub.

## Enable Gemini on Streamlit Community Cloud (optional)

1. Open the deployed app in Streamlit Community Cloud.
2. Open **Manage app → Settings → Secrets**.
3. Add the following, replacing the example text with your own Google AI Studio API key:

   ~~~toml
   GOOGLE_API_KEY = "paste_your_own_key_here"
   ~~~

4. Save the secrets and reboot the app if it does not restart automatically.

Do not add the real key to app.py, requirements.txt, README, or any public GitHub file.

## Example questions

- What is acne?
- What is eczema?
- Tell me about psoriasis
- What causes vitiligo?
- What is a fungal infection?

If the app cannot connect to Gemini, it will still try to return information from the local knowledge base.

## Medical safety

The information in this demo is general and may be incomplete. Do not use it to self-diagnose or decide on treatment. Contact a licensed healthcare professional for individual symptoms, severe pain, fever, rapidly changing skin lesions, or worsening symptoms.
