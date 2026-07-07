import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# Configure Gemini
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("❌ GOOGLE_API_KEY not found in .env file")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")


# Function to read all knowledge files
def load_knowledge():
    knowledge = ""

    folder = "knowledge"

    for file in os.listdir(folder):
        if file.endswith(".txt"):
            with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
                knowledge += f.read() + "\n\n"

    return knowledge


knowledge = load_knowledge()

# Streamlit UI
st.title("🩺 AI Skin Disease Chatbot")

user_input = st.text_input("Ask your question")

if st.button("Ask"):

    if user_input.strip():

        prompt = f"""
You are an AI Skin Disease Assistant.

Answer ONLY using the information below.

If the answer is not present in the knowledge base, politely say:

"I don't have enough information in my knowledge base to answer that."

Knowledge Base:

{knowledge}

Question:
{user_input}
"""

        response = model.generate_content(prompt)

        st.subheader("Answer")
        st.write(response.text)