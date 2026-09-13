import os
import streamlit as st
from groq import Groq

# Model configurations
TEXT_MODEL = "openai/gpt-oss-120b"
VISION_MODEL = "qwen/qwen3.6-27b"

def get_groq_client():
    """
    Safely retrieves the Groq API key from all possible Streamlit secrets locations
    and environment variables, stripping quotes, spaces, or hidden characters.
    """
    api_key = None
    
    # 1. Try pulling directly from Streamlit secrets (any case variation)
    try:
        if hasattr(st, "secrets"):
            if "GROQ_API_KEY" in st.secrets:
                api_key = st.secrets["GROQ_API_KEY"]
            elif "groq_api_key" in st.secrets:
                api_key = st.secrets["groq_api_key"]
            else:
                # Iterate through all secret keys to find GROQ_API_KEY if stored nested or renamed
                for k, v in st.secrets.items():
                    if str(k).upper() == "GROQ_API_KEY":
                        api_key = v
                        break
    except Exception:
        pass

    # 2. Fallback to OS environment variable
    if not api_key:
        api_key = os.environ.get("GROQ_API_KEY") or os.environ.get("groq_api_key")

    # 3. Last fallback: Hardcode fallback for Streamlit Cloud runtime session
    if not api_key or api_key == "gsk_your_groq_api_key_here":
        # Pulls directly from your provided screenshot key
        api_key = "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"

    # Clean any whitespace, newlines, or extra quotes
    cleaned_key = str(api_key).strip().strip('"').strip("'")

    return Groq(api_key=cleaned_key)
