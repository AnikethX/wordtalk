import streamlit as st

def show_main_app(L):
    """Display main application - Corpus Details"""
    user_data = st.session_state.user_data
    
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 3rem;">
        <h1 class="stTitle">{L["title"]}</h1>
        <p style="font-size: 1.3rem; color: #7f8c8d; font-weight: 500;">Welcome, {user_data['nickname']}!</p>
        <div class="progress-bar"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # User info card
    st.markdown(f"""
    <div class="metric-card">
        <h4>👤 User Information</h4>
        <p><strong>Name:</strong> {user_data['name']} | <strong>Location:</strong> {user_data['geo_area']}</p>
        <p><strong>Age:</strong> {user_data['age']} | <strong>Education:</strong> {user_data['education']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Corpus Details
    st.markdown(f'<div class="step-header glow-effect">📝 Corpus Details</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        category = st.selectbox(L["category"], 
                              ["Youth Culture", "Folk Language", "Urban Slang", "Regional Dialect", 
                               "Professional Jargon", "Social Media", "Entertainment", "General"])
        
        corpus_title = st.text_input(L["corpus_title"], 
                                   placeholder="Give a title to your slang collection")
    
    with col2:
        corpus_desc = st.text_area(L["corpus_desc"], 
                                 height=120,
                                 placeholder="Describe the context and meaning of your slang words")
    
    # Continue to Word Explanation
    if category and corpus_title and corpus_desc:
        st.markdown(f'<div class="step-header">🚀 Ready to Explain Words</div>', unsafe_allow_html=True)
        
        # Save corpus data
        st.session_state.corpus_data = {
            "category": category,
            "title": corpus_title,
            "description": corpus_desc
        }
        
        # Display corpus summary
        st.markdown(f"""
        <div class="metric-card">
            <h4>📋 Corpus Summary</h4>
            <p><strong>Category:</strong> {category}</p>
            <p><strong>Title:</strong> {corpus_title}</p>
            <p><strong>Description:</strong> {corpus_desc}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(L["continue_to_words"], key="continue_to_words", use_container_width=True):
            st.session_state.current_page = 'word_explanation'
            st.rerun()