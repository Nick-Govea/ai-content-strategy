import os
import streamlit as st

def get_secret(key):
    """
    Get secret from Streamlit secrets or environment variables.
    Prioritizes Streamlit secrets for cloud deployment, falls back to env vars for local development.
    
    Args:
        key (str): The secret key to retrieve
        
    Returns:
        str: The secret value or None if not found
    """
    try:
        # Try Streamlit secrets first (for cloud deployment)
        return st.secrets[key]
    except (KeyError, AttributeError):
        # Fall back to environment variables (for local development)
        return os.getenv(key)

# API Keys
GEMINI_API_KEY = get_secret("GEMINI_API_KEY")
REDDIT_CLIENT_ID = get_secret("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = get_secret("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = get_secret("REDDIT_USER_AGENT")

# Configuration validation
def validate_config():
    """
    Validate that all required configuration is present.
    
    Returns:
        bool: True if all required config is present, False otherwise
    """
    required_keys = {
        "GEMINI_API_KEY": GEMINI_API_KEY,
        "REDDIT_CLIENT_ID": REDDIT_CLIENT_ID,
        "REDDIT_CLIENT_SECRET": REDDIT_CLIENT_SECRET,
        "REDDIT_USER_AGENT": REDDIT_USER_AGENT
    }
    
    missing_keys = [key for key, value in required_keys.items() if not value]
    
    if missing_keys:
        print(f"Missing required configuration: {', '.join(missing_keys)}")
        return False
    
    return True

# Environment detection
def is_streamlit_cloud():
    """
    Detect if running on Streamlit Cloud.
    
    Returns:
        bool: True if running on Streamlit Cloud, False otherwise
    """
    try:
        return hasattr(st, 'secrets') and st.secrets is not None
    except:
        return False 