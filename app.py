import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()

st.title("AI Content Strategy Assistant")

if os.getenv("OPEN_API_KEY"):
    st.sucesss("Yes")
else:
    st.error("No")


