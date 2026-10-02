import os
from dotenv import load_dotenv

load_dotenv()

try:
    import streamlit as st
    DATABASE_URL = st.secrets["DATABASE_URL"]
except Exception:
    DATABASE_URL = os.environ["DATABASE_URL"]
