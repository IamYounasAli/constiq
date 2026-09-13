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
    
    # 1. Check Streamlit secrets
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

    # 2. Fallback to OS environment variable
    if not api_key:
        api_key = os.environ.get("GROQ_API_KEY") or os.environ.get("groq_api_key")

    # Clean any whitespace, newlines, or extra quotes
    if api_key:
        api_key = str(api_key).strip().strip('"').strip("'")

    # 3. Guard check
    if not api_key or api_key == "gsk_your_groq_api_key_here":
        st.error("⚠️ Groq API Key not found or unconfigured! Please set GROQ_API_KEY in Streamlit Cloud Secrets.")
        st.stop()

    return Groq(api_key=api_key)
