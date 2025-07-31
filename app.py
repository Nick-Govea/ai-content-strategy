import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()  # Load the .env file
api_key = os.getenv("GEMINI_API_KEY")  # Read variable from .env

if not api_key:
    st.error("GEMINI_API_KEY not found in environment variables")
    st.stop()

genai.configure(api_key=api_key)  # Configure Gemini with the key

# Create the model
model = genai.GenerativeModel('gemini-2.0-flash')

# Test the API
try:
    response = model.generate_content("Explain how AI works in a few words")
    st.write("Response:", response.text)
except Exception as e:
    st.error(f"Error calling Gemini API: {e}")