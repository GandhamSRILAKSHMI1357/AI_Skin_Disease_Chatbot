import os
from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge"
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")


@st.cache_data
def load_knowledge_files() -> dict[str, str]:
    """Load the text knowledge files committed with this app."""
    if not KNOWLEDGE_DIR.is_dir():
        return {}

    documents: dict[str, str] = {}
    for file_path in sorted(KNOWLEDGE_DIR.glob("*.txt")):
        try:
            body = file_path.read_text(encoding="utf-8").strip()
        except OSError:
            continue
        if body:
            documents[file_path.stem.lower()] = body
    return documents


def get_api_key() -> str | None:
    """Read the API key from Streamlit Secrets or environment variables."""
    try:
        key = st.secrets.get("GOOGLE_API_KEY", "")
    except Exception:
        # Streamlit raises an exception when no secrets file is configured.
        key = ""

    return (
        str(key).strip()
        or os.getenv("GOOGLE_API_KEY", "").strip()
        or os.getenv("GEMINI_API_KEY", "").strip()
        or None
    )


def local_answer(question: str, documents: dict[str, str]) -> str:
    """Return educational information from the local knowledge base."""
    q = question.casefold()
    aliases = {
        "fungal_infection": (
            "fungal", "ringworm", "itchy ring", "athlete's foot", "athletes foot",
            "jock itch", "fungus",
        ),
        "psoriasis": ("psoriasis", "scaly patches", "silvery scales"),
        "vitiligo": (
            "vitiligo", "white patches", "loss of skin colour", "loss of skin color",
        ),
        "eczema": ("eczema", "dermatitis", "dry itchy skin"),
        "acne": (
            "acne", "pimples", "pimple", "blackheads", "whiteheads", "breakouts",
        ),
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
        f"Try asking about: {available}. For personal symptoms, consult a licensed "
        "healthcare professional."
    )


def gemini_answer(question: str, documents: dict[str, str], api_key: str) -> str:
    """Generate a knowledge-grounded educational response using Gemini."""
    from google import genai

    knowledge = "\n\n".join(
        f"TOPIC: {topic.replace('_', ' ')}\n{body}"
        for topic, body in documents.items()
    )
    prompt = f"""
You are an educational assistant about common skin conditions.
Use only the knowledge base below. Do not diagnose the user, infer a disease
from personal symptoms, or invent treatments or medical facts. If the knowledge
base does not answer the question, say so clearly and suggest a licensed
healthcare professional. Use simple English and short paragraphs.

Knowledge base:
{knowledge}

User question:
{question}
"""
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    answer = (response.text or "").strip()
    if not answer:
        raise RuntimeError("The AI service returned an empty answer.")
    return answer


def answer_question(question: str, documents: dict[str, str]) -> tuple[str, str]:
    """Use Gemini when configured; otherwise safely fall back to local answers."""
    api_key = get_api_key()
    if api_key:
        try:
            return gemini_answer(question, documents, api_key), "Gemini AI"
        except Exception:
            # Never display credentials or raw request details to the user.
            local = local_answer(question, documents)
            return (
                f"{local}\n\n"
                "Note: Gemini could not be reached, so this answer came from the "
                "local knowledge base. Check the API key, model access, and deployment logs.",
                "Local knowledge fallback",
            )

    return local_answer(question, documents), "Local knowledge base"


st.set_page_config(page_title="AI Skin Disease Chatbot", page_icon="🩺", layout="centered")

st.title("🩺 AI Skin Disease Chatbot")
st.caption(
    "Educational information only. This app cannot diagnose a skin condition "
    "or replace advice from a licensed healthcare professional."
)

documents = load_knowledge_files()
if not documents:
    st.error(
        "The knowledge base is missing or empty. In GitHub, check that the "
        "knowledge/ folder and its .txt files are included on the deployed branch."
    )
    st.stop()

api_key = get_api_key()
if api_key:
    st.success("Gemini API key detected. AI responses are enabled.")
else:
    st.info(
        "The app is ready in local knowledge mode. No API key is required for "
        "basic answers. Add a Gemini key in Streamlit Secrets to enable AI-generated responses."
    )

with st.form("question_form", clear_on_submit=False):
    user_input = st.text_input(
        "Ask about a common skin condition",
        placeholder="Example: What is acne?",
        max_chars=500,
    )
    submitted = st.form_submit_button("Ask", type="primary", use_container_width=True)

if submitted:
    question = user_input.strip()
    if not question:
        st.warning("Please enter a question first.")
    else:
        with st.spinner("Preparing your educational answer..."):
            answer, source = answer_question(question, documents)
        st.subheader("Educational information")
        st.caption(f"Answer source: {source}")
        st.markdown(answer)
        st.warning(
            "This is general educational information, not a diagnosis or personal "
            "treatment plan. Please contact a licensed healthcare professional for "
            "personal symptoms, severe pain, fever, rapidly changing skin lesions, "
            "or symptoms that are worsening."
        )

with st.expander("How to enable Gemini AI responses"):
    st.markdown(
        "1. Open your app in Streamlit Community Cloud.\n"
        "2. Select **Manage app → Settings → Secrets**.\n"
        '3. Add GOOGLE_API_KEY = "your_actual_api_key" and save.\n\n'
        "Keep the key in Streamlit Secrets. **Do not commit a real API key to a public GitHub repository.**"
    )
