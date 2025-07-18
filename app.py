import streamlit as st
from datetime import datetime
import os
import pandas as pd
from config import setup_page_config, load_custom_css
from auth import show_login_page, is_logged_in
from main_app import show_main_app
from word_explanation import show_word_explanation
from leaderboard import show_leaderboard
from language import get_language_dict
from admin import show_admin_panel
from gamification import show_gamification_sidebar, show_achievements_page
import pandas as pd
import os

CSV_FILE = "userdata.csv"

# Initialize the app
setup_page_config()
load_custom_css()

def main():
    """Main application controller"""
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'login'
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}
    if 'corpus_data' not in st.session_state:
        st.session_state.corpus_data = {}
    
    # Load data for gamification
    df = pd.DataFrame()
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
        except:
            df = pd.DataFrame()
    
    # Language selection and navigation
    lang = show_sidebar_navigation()
    L = get_language_dict(lang)
    
    # Show gamification sidebar
    show_gamification_sidebar(st.session_state.user_data, df)
    
    # Route to appropriate page
    if st.session_state.current_page == "login":
        show_login_page(L)
    elif st.session_state.current_page == "main":
        if is_logged_in():
            show_main_app(L)
        else:
            redirect_to_login()
    elif st.session_state.current_page == "word_explanation":
        if is_logged_in():
            show_word_explanation(L)
        else:
            redirect_to_login()
    elif st.session_state.current_page == "leaderboard":
        if is_logged_in():
            show_leaderboard(L)
        else:
            redirect_to_login()
    elif st.session_state.current_page == "achievements":
        if is_logged_in():
            show_achievements_page(st.session_state.user_data, df, L)
        else:
            redirect_to_login()

def show_sidebar_navigation():
    """Display sidebar navigation and language selection"""
    with st.sidebar:
        # Language selection
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   padding: 1.5rem; border-radius: 20px; margin-bottom: 1.5rem;">
            <h3 style="color: white; text-align: center; margin: 0;">🌐 Language Selection</h3>
        </div>
        """, unsafe_allow_html=True)
        
        lang = st.radio("Choose Language / భాష ఎంచుకోండి", ["తెలుగు", "English"])
        
        st.markdown("---")
        st.markdown("### 🧭 Navigation")
        
        # Navigation buttons
        if st.session_state.logged_in:
            if st.button("📚 Main App", key="nav_main", use_container_width=True):
                st.session_state.current_page = 'main'
                st.rerun()
            if st.button("🧠 Word Explanation", key="nav_words", use_container_width=True):
                st.session_state.current_page = 'word_explanation'
                st.rerun()
            if st.button("🏆 Leaderboard", key="nav_leaderboard", use_container_width=True):
                st.session_state.current_page = 'leaderboard'
                st.rerun()
            if st.button("🎮 Achievements", key="nav_achievements", use_container_width=True):
                st.session_state.current_page = 'achievements'
                st.rerun()
            if st.button("🚪 Logout", key="nav_logout", use_container_width=True):
                logout_user()
        else:
            st.info("Please login to access the app")
        
        # Admin panel
        show_admin_panel()
    
    return lang

def logout_user():
    """Handle user logout"""
    st.session_state.logged_in = False
    st.session_state.current_page = 'login'
    st.session_state.user_data = {}
    st.session_state.corpus_data = {}
    st.rerun()

def redirect_to_login():
    """Redirect to login page"""
    st.session_state.current_page = "login"
    st.rerun()

if __name__ == "__main__":
    main()