# AI Skin Disease Chatbot

A Streamlit demo that answers general questions about common skin conditions using a small local text knowledge base and Google's Gemini API.

> **Important:** This is an educational prototype, not a medical device. It cannot diagnose conditions or replace a licensed healthcare professional. Do not use it for emergencies.

## Features

- Text questions about topics represented in the `knowledge/` folder
- Grounded answers that are instructed to use the supplied knowledge base
- Clear configuration errors when the API key or knowledge files are missing
- Supports local `.env` configuration and hosted Streamlit Secrets

## Requirements

- Python 3.10 or later
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)

## Run locally (Windows PowerShell)

1. Clone the repository and enter its folder:

   ```powershell
   git clone https://github.com/GandhamSRILAKSHMI1357/AI_Skin_Disease_Chatbot.git
   cd AI_Skin_Disease_Chatbot
   ```

2. Create and activate a virtual environment:

   ```powershell
   py -3.12 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install the small set of packages this app actually uses:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Create a file named `.env` in the project root containing:

   ```text
   GOOGLE_API_KEY=your_gemini_api_key
   ```

   Do not commit your real API key to GitHub.

5. Start the app:

   ```powershell
   streamlit run app.py
   ```

## Deploy on Streamlit Community Cloud

1. Open [Streamlit Community Cloud](https://share.streamlit.io/) and sign in with GitHub.
2. Choose **Create app**, then select this repository, the `fix/streamlit-deployment-20261009` branch, and `app.py` as the entrypoint for the test deployment. After pull request [#1](https://github.com/GandhamSRILAKSHMI1357/AI_Skin_Disease_Chatbot/pull/1) is reviewed and merged, you can switch the app to `main`.
3. Open **Advanced settings** and choose Python 3.12.
4. In the **Secrets** field, add:

   ```toml
   GOOGLE_API_KEY = "your_gemini_api_key"
   ```

5. Click **Deploy** and inspect the app's logs if startup fails.

The hosted app uses the repository's `requirements.txt` to install its Python dependencies. The API key belongs in hosting Secrets, not in the repository.

## Project structure

```text
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
```
