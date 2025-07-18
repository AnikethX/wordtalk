import streamlit as st
from sentence_transformers import SentenceTransformer, util

@st.cache_resource
def load_model():
    """Load sentence transformer model with caching"""
    try:
        return SentenceTransformer("all-MiniLM-L6-v2")
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

def get_score(user_input, words):
    """Calculate semantic similarity score"""
    if not user_input.strip():
        return 0
    
    try:
        model = load_model()
        if model is None:
            return 0
            
        embedding_input = model.encode(user_input, convert_to_tensor=True)
        embedding_words = model.encode(" ".join(words), convert_to_tensor=True)
        score = util.cos_sim(embedding_input, embedding_words).item()
        return max(0, min(10, round(score * 10)))
    except Exception as e:
        st.error(f"Error calculating score: {str(e)}")
        return 0