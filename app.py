import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from google import genai

BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge"
load_dotenv(BASE_DIR / ".env")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-flash-latest")


def get_api_key() -> str | None:
    key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if key:
        return key
    try:
        return st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY")
    except Exception:
        return None


@st.cache_data
def load_knowledge_files() -> dict[str, str]:
    if not KNOWLEDGE_DIR.is_dir():
        return {}
    return {
        file_path.stem.lower(): file_path.read_text(encoding="utf-8").strip()
        for file_path in sorted(KNOWLEDGE_DIR.glob("*.txt"))
        if file_path.read_text(encoding="utf-8").strip()
    }


def local_answer(question: str, documents: dict[str, str]) -> str:
    """Return a relevant entry from the bundled educational knowledge base."""
    q = question.lower()
    aliases = {
        "fungal_infection": ("fungal", "ringworm", "itchy ring", "athlete's foot"),
        "psoriasis": ("psoriasis", "scaly patches"),
        "vitiligo": ("vitiligo", "white patches", "loss of skin colour", "loss of skin color"),
        "eczema": ("eczema", "dermatitis", "dry itchy skin"),
        "acne": ("acne", "pimples", "pimple", "blackheads", "whiteheads"),
    }
    for topic, terms in aliases.items():
        if topic in documents and (topic.replace("_", " ") in q or any(term in q for term in terms)):
            return documents[topic]
    for topic, body in documents.items():
        if topic.replace("_", " ") in q:
            return body
    available = ", ".join(topic.replace("_", " ") for topic in documents)
    return (
        "I couldn't find a matching topic in the chatbot's local knowledge base. "
        f"You can ask about: {available}. For personal symptoms, consult a licensed healthcare professional."
    )


st.set_page_config(page_title="AI Skin Disease Chatbot", page_icon="🩺")
st.title("AI Skin Disease Chatbot")
st.caption(
    "Educational information only — this tool cannot diagnose skin conditions "
    "or replace advice from a licensed healthcare professional."
)

documents = load_knowledge_files()
if not documents:
    st.error("The knowledge base is missing or empty. Please check the knowledge/ folder in the GitHub repository.")
    st.stop()

api_key = get_api_key()
if not api_key:
    st.info("Basic knowledge mode is active. You can ask about topics in the built-in knowledge base without setting an API key.")
else:
    st.caption("AI mode is enabled when the configured Gemini API key is valid.")

user_input = st.text_input(
    "Ask a question about common skin conditions",
    placeholder="Example: What is acne?",
    max_chars=500,
)

if st.button("Ask", type="primary"):
    question = user_input.strip()
    if not question:
        st.warning("Please enter a question first.")
    else:
        answer = None
        if api_key:
            prompt = f"""
You are an educational skin-health information assistant, not a doctor.
Use ONLY the knowledge base below to answer the question.
Never give a definitive diagnosis. For personal symptoms or concerning changes,
recommend speaking with a licensed healthcare professional.

KNOWLEDGE BASE:
{chr(10).join(documents.values())}

QUESTION:
{question}
"""
            with st.spinner("Preparing an answer..."):
                try:
                    client = genai.Client(api_key=api_key)
                    response = client.models.generate_content(
                        model=MODEL_NAME,
                        contents=prompt,
                    )
                    answer = (response.text or "").strip()
                except Exception:
                    # Keep the app useful if a key is absent, expired, or invalid.
                    st.info("Gemini could not be reached, so a local knowledge-base answer is shown instead.")
        if not answer:
            answer = local_answer(question, documents)
        st.subheader("Educational information")
        st.write(answer)
        st.warning(
            "This information is for education only, not a diagnosis or treatment plan. "
            "Please contact a licensed healthcare professional for personal symptoms, "
            "rapidly changing skin lesions, severe pain, fever, or worsening symptoms."
        )
