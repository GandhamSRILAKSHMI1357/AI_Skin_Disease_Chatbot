from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge"


@st.cache_data
def load_knowledge_files() -> dict[str, str]:
    if not KNOWLEDGE_DIR.is_dir():
        return {}
    documents = {}
    for file_path in sorted(KNOWLEDGE_DIR.glob("*.txt")):
        body = file_path.read_text(encoding="utf-8").strip()
        if body:
            documents[file_path.stem.lower()] = body
    return documents


def local_answer(question: str, documents: dict[str, str]) -> str:
    """Return educational information from the repository's local knowledge base."""
    q = question.lower()
    aliases = {
        "fungal_infection": ("fungal", "ringworm", "itchy ring", "athlete's foot"),
        "psoriasis": ("psoriasis", "scaly patches"),
        "vitiligo": ("vitiligo", "white patches", "loss of skin colour", "loss of skin color"),
        "eczema": ("eczema", "dermatitis", "dry itchy skin"),
        "acne": ("acne", "pimples", "pimple", "blackheads", "whiteheads"),
    }
    for topic, terms in aliases.items():
        if topic in documents and (
            topic.replace("_", " ") in q or any(term in q for term in terms)
        ):
            return documents[topic]

    for topic, body in documents.items():
        if topic.replace("_", " ") in q:
            return body

    available = ", ".join(topic.replace("_", " ") for topic in documents)
    return (
        "I couldn't find a matching topic in the local knowledge base. "
        f"Try asking about: {available}. For personal symptoms, consult a licensed healthcare professional."
    )


st.set_page_config(page_title="AI Skin Disease Chatbot", page_icon="🩺")
st.title("AI Skin Disease Chatbot")
st.caption(
    "Educational information only — this tool cannot diagnose skin conditions "
    "or replace advice from a licensed healthcare professional."
)
st.info("Local knowledge mode: no Gemini API key or account setup is required.")

documents = load_knowledge_files()
if not documents:
    st.error("The knowledge base is missing or empty. Please check the knowledge/ folder in the GitHub repository.")
    st.stop()

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
        st.subheader("Educational information")
        st.write(local_answer(question, documents))
        st.warning(
            "This information is for education only, not a diagnosis or treatment plan. "
            "Please contact a licensed healthcare professional for personal symptoms, "
            "rapidly changing skin lesions, severe pain, fever, or worsening symptoms."
        )
