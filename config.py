import os
import streamlit as st
from groq import Groq

# Model configurations
TEXT_MODEL = "openai/gpt-oss-120b"
VISION_MODEL = "qwen/qwen3.6-27b"
import os
import streamlit as st
from groq import Groq

# Model configurations
TEXT_MODEL = "openai/gpt-oss-120b"
VISION_MODEL = "qwen/qwen3.6-27b"

def get_groq_client():
    """
    Safely retrieves the Groq API key from Streamlit secrets or environment variables.
    """
    api_key = None

    # 1. Search Streamlit Secrets safely across possible key formats
    try:
        if hasattr(st, "secrets"):
            if "GROQ_API_KEY" in st.secrets:
                api_key = st.secrets["GROQ_API_KEY"]
            elif "groq_api_key" in st.secrets:
                api_key = st.secrets["groq_api_key"]
            else:
                for k, v in st.secrets.items():
                    if str(k).upper() == "GROQ_API_KEY":
                        api_key = v
                        break
    except Exception:
        pass

    # 2. Fallback to system environment variables
    if not api_key:
        api_key = os.getenv("GROQ_API_KEY") or os.getenv("groq_api_key")

    # 3. Clean trailing spaces, newlines, and stray quotation marks
    if api_key:
        api_key = str(api_key).strip().strip('"').strip("'")

    # 4. Guard check: ensure key exists, starts with 'gsk_', and is not a placeholder
    if not api_key or not api_key.startswith("gsk_") or api_key == "gsk_your_groq_api_key_here":
        st.error(
            "⚠️ **Groq API Key not found or invalid!**\n\n"
            "Please check **App Settings > Secrets** in Streamlit Cloud and ensure it contains:\n"
            '```toml\nGROQ_API_KEY = "gsk_your_actual_key_here"\n```'
        )
        st.stop()

    return Groq(api_key=api_key)
def get_groq_client():
    """
    Safely retrieves the Groq API key from Streamlit secrets or environment variables.
    """
    api_key = None

    # 1. Check Streamlit secrets safely
    try:
        if "GROQ_API_KEY" in st.secrets:
            api_key = st.secrets["GROQ_API_KEY"]
        elif "groq_api_key" in st.secrets:
            api_key = st.secrets["groq_api_key"]
    except Exception:
        pass

    # 2. Fallback to OS environment variable
    if not api_key:
        api_key = os.getenv("GROQ_API_KEY") or os.getenv("groq_api_key")

    # Clean whitespace and accidental surrounding quotes
    if api_key:
        api_key = str(api_key).strip().strip('"').strip("'")

    # 3. Guard check
    if not api_key or api_key == "gsk_your_groq_api_key_here":
        st.error(
            "⚠️ **Groq API Key not found or unconfigured!**\n\n"
            "Please open **App Settings > Secrets** in Streamlit Cloud and add:\n"
            '```toml\nGROQ_API_KEY = "gsk_your_actual_key_here"\n```'
        )
        st.stop()

    return Groq(api_key=api_key)
