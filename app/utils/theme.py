"""
Injects the Study Nook visual theme (pastel notebook style) into every page.
Call apply_theme() once at the top of each page, right after st.set_page_config.
"""

import streamlit as st

MATH_COLOR = "#8B7FD6"
PHYSICS_COLOR = "#E0824F"
GOOD_COLOR = "#4FB286"
WARN_COLOR = "#E3A23A"

SUBJECT_COLORS = [MATH_COLOR, PHYSICS_COLOR, GOOD_COLOR, WARN_COLOR, "#5BAEE0", "#D9636B"]


def apply_theme():
    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Nunito:wght@400;600;700;800&family=Caveat:wght@600;700&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
        <style>
            html, body, [class*="css"]  {
                font-family: 'Nunito', sans-serif;
            }
            h1, h2, h3 {
                font-family: 'Fredoka', sans-serif !important;
            }
            .stApp {
                background-color: #F8F6FB;
            }
            section[data-testid="stSidebar"] {
                background: linear-gradient(180deg, #F3EEFC 0%, #F8F6FB 40%);
            }
            div[data-testid="stMetric"] {
                background: #FFFFFF;
                border-radius: 18px;
                padding: 14px 16px;
                box-shadow: 0 2px 6px rgba(138,120,190,0.10);
            }
            div[data-testid="stMetricValue"] {
                font-family: 'DM Mono', monospace;
                color: #6A5DC4;
            }
            .stButton > button {
                background: linear-gradient(135deg, #8B7FD6, #6A5DC4);
                color: white;
                border-radius: 13px;
                border: none;
                font-family: 'Fredoka', sans-serif;
                font-weight: 600;
            }
            div[data-testid="stForm"], .stTabs {
                background: #FFFFFF;
                border-radius: 20px;
                padding: 8px;
            }
            div[data-testid="stTextInputRootElement"],
            div[data-testid="stNumberInputContainer"],
            div[data-testid="stDateInputField"],
            div[data-baseweb="select"] > div {
                border: 2px solid #ECE7F6 !important;
                border-radius: 12px !important;
                background: #FFFFFF !important;
            }
            div[data-testid="stTextInputRootElement"]:focus-within,
            div[data-testid="stNumberInputContainer"]:focus-within,
            div[data-baseweb="select"] > div:focus-within {
                border-color: #8B7FD6 !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
