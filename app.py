import streamlit as st
import os
from components.auth import handle_authentication, check_authentication
from pages.landing import show_landing_page
from components.dashboard import show_dashboard
from pages.results import show_results_page
from pages.about import show_about_page
from utils.styling import load_custom_css

# Page configuration
st.set_page_config(
    page_title="🪐 ExoHunter - Exoplanet Discovery AI",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'page' not in st.session_state:
    st.session_state.page = "landing"

# Load custom CSS
load_custom_css()

def main():
    # Check authentication status
    if not st.session_state.authenticated:
        if st.session_state.page == "landing":
            show_landing_page()
        elif st.session_state.page == "auth":
            handle_authentication()
        elif st.session_state.page == "about":
            show_about_page()
    else:
        # Authenticated user pages
        if st.session_state.page == "dashboard":
            show_dashboard()
        elif st.session_state.page == "results":
            show_results_page()
        elif st.session_state.page == "about":
            show_about_page()
        else:
            # Default to dashboard for authenticated users
            st.session_state.page = "dashboard"
            st.rerun()

if __name__ == "__main__":
    main()
