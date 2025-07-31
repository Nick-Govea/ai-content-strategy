import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
import requests

load_dotenv()  # Load the .env file
api_key = os.getenv("GEMINI_API_KEY")  # Read variable from .env

if not api_key:
    st.error("GEMINI_API_KEY not found in environment variables")
    st.stop()

genai.configure(api_key=api_key)  # Configure Gemini with the key

# Create the model
model = genai.GenerativeModel('gemini-2.0-flash')

# Title of Page

st.title("Your all-in-one solution for market trend data")

#Reddit API




#Prompting
instructions = "Business Context: You are a consultant who works in the data analysis industry. I will provide you with data from reddit and your goal is to act like you scraped all this data and come up with solutions to the questions that i give you. you are to speak in a professional tone. keep your responses short but don't sacrifice clarity. Your job are to find market trends"

user_input = instructions + st.text_area("Ask me something")
submit = st.button("Send")

if user_input and submit:
    with st.spinner("Thinking..."):
        response = model.generate_content(user_input)
        st.success("✅ Done!")
        st.markdown("**Gemini:** " + response.text)