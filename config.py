import streamlit as st

def setup_page_config():
    """Set up Streamlit page configuration"""
    st.set_page_config(
        page_title="WordTalk – తెలుగు", 
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get help': None,
            'Report a bug': None,
            'About': "WordTalk - Telugu Slang Collector"
        }
    )

def load_custom_css():
    """Load custom CSS styling from a file"""
    with open("style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Add floating background shapes
    st.markdown("""
    <div class="floating-shapes">
        <div class="shape"></div>
        <div class="shape"></div>
        <div class="shape"></div>
    </div>
    """, unsafe_allow_html=True)