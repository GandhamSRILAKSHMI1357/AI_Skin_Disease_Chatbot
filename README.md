# AI Skin Disease Chatbot

## Description
An AI-powered chatbot that answers questions about common skin diseases using Google's Gemini API and a custom knowledge base.

## Features
- AI-powered responses
- Streamlit web interface
- Knowledge-base based answers
- Supports Acne, Eczema, Psoriasis, Vitiligo, and Fungal Infection

## Technologies Used
- Python
- Streamlit
- Google Gemini API
- python-dotenv

## Project Structure

```
AI_Skin_Disease_Chatbot/
│── app.py
│── requirements.txt
│── .gitignore
│── README.md
│── knowledge/
│   ├── acne.txt
│   ├── eczema.txt
│   ├── psoriasis.txt
│   ├── vitiligo.txt
│   └── fungal_infection.txt
```

## Installation

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```text
GOOGLE_API_KEY=YOUR_API_KEY
```

Run:

```bash
python -m streamlit run app.py
```

## Example Questions

- What is acne?
- What is eczema?
- What is psoriasis?
- What is vitiligo?
- What is fungal infection?

Questions outside the knowledge base will return:

> I don't have enough information in my knowledge base to answer that.