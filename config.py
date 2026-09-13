import os
import streamlit as st
from groq import Groq

# Model configurations
TEXT_MODEL = "openai/gpt-oss-120b"
VISION_MODEL = "qwen/qwen3.6-27b"

def get_groq_client():
    """
    Initializes and returns the Groq client checking Streamlit secrets 
    first, then falling back to environment variables.
    """
    api_key = None
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
    else:
        api_key = os.environ.get("GROQ_API_KEY")
        
    if not api_key or api_key == "gsk_your_groq_api_key_here":
        st.error("⚠️ Groq API Key not found or unconfigured! Please set GROQ_API_KEY in .streamlit/secrets.toml or Streamlit Cloud Secrets.")
        st.stop()
        
    return Groq(api_key=api_key)
