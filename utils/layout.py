import streamlit as st
from pathlib import Path
from utils.theme import YCP_THEME

def setup_page(title="York College Partnerships"):
    # Set page config
    st.set_page_config(
        page_title=title,
        page_icon="🏛️",
        layout="wide"
    )
    
    # Custom CSS for York College branding
    st.markdown("""
        <style>
            .stApp {
                background-color: #FFFFFF;
            }
            .stButton > button {
                background-color: #2B5234;
                color: white;
                border: none;
                padding: 0.5rem 1rem;
                border-radius: 4px;
            }
            .stButton > button:hover {
                background-color: #4C8B3F;
            }
            h1, h2, h3 {
                color: #2B5234;
                font-family: "Helvetica Neue", Arial, sans-serif;
            }
            .stMarkdown {
                color: #333333;
                font-family: Arial, sans-serif;
            }
            .stSelectbox label, .stTextInput label {
                color: #2B5234;
                font-weight: 500;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Add logo
    current_dir = Path(__file__).parent.parent
    image_path = current_dir / "public" / "images" / "york.png"
    if image_path.exists():
        st.image(str(image_path), width=YCP_THEME["logo"]["width"])
    else:
        st.error("Logo not found. Please ensure york.png is in public/images/")
