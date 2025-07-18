import streamlit as st
from datetime import datetime
import pandas as pd
import os
from scoring import get_score
from words import get_words
from gamification import get_user_level, calculate_combo_multiplier, show_achievement_popup
import random

CSV_FILE = "userdata.csv"

def show_word_explanation(L):
    """Display word explanation page"""
    user_data = st.session_state.user_data
    corpus_data = st.session_state.corpus_data
    
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 3rem;">
        <h1 class="stTitle">🧠 Word Explanation</h1>
        <p style="font-size: 1.3rem; color: #7f8c8d; font-weight: 500;">Express your creativity with Telugu slang!</p>
        <div class="progress-bar"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Show corpus context
    st.markdown(f"""
    <div class="info-card">
        <h4>📋 Your Corpus Context</h4>
        <p><strong>Category:</strong> {corpus_data.get('category', 'N/A')}</p>
        <p><strong>Title:</strong> {corpus_data.get('title', 'N/A')}</p>
        <p><strong>Description:</strong> {corpus_data.get('description', 'N/A')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate words (persistent in session)
    if "current_words" not in st.session_state:
        st.session_state["current_words"] = get_words()
    
    words = st.session_state["current_words"]
    
    # Add game elements
    col_info1, col_info2, col_info3 = st.columns(3)
    
    # Load existing data for game stats
    df = pd.DataFrame()
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
        except:
            df = pd.DataFrame()
    
    nickname = user_data.get("nickname", "")
    user_contributions = df[df["nickname"] == nickname] if nickname and not df.empty else pd.DataFrame()
    
    with col_info1:
        total_score = user_contributions["score"].sum() if not user_contributions.empty else 0
        level_name, level_num = get_user_level(total_score)
        st.markdown(f"""
        <div class="metric-card">
            <h4>🎯 Current Level</h4>
            <h3>{level_name}</h3>
            <p>Level {level_num}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_info2:
        contributions_today = len(user_contributions[
            pd.to_datetime(user_contributions["datetime"]).dt.date == pd.Timestamp.now().date()
        ]) if not user_contributions.empty else 0
        st.markdown(f"""
        <div class="metric-card">
            <h4>📈 Today's Progress</h4>
            <h3>{contributions_today}</h3>
            <p>Contributions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_info3:
        if len(user_contributions) >= 3:
            recent_scores = user_contributions.tail(5)["score"].tolist()
            multiplier = calculate_combo_multiplier(recent_scores)
            st.markdown(f"""
            <div class="metric-card">
                <h4>🔥 Combo Multiplier</h4>
                <h3>{multiplier}x</h3>
                <p>Bonus Active</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="metric-card">
                <h4>⭐ Potential</h4>
                <h3>Unlimited</h3>
                <p>Keep Going!</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Main explanation card
    st.markdown(f'<div class="explanation-card">', unsafe_allow_html=True)
    
    # Display words prominently
    st.markdown(f"""
    <div class="word-display">
        <h3 style="margin-bottom: 1rem;">{L["words_to_explain"]}</h3>
        <div style="font-size: 2.5rem; font-weight: 800; margin: 1rem 0;">
            {" • ".join(words)}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        explanation = st.text_area(
            L["words_label"],
            height=200,
            placeholder="Express these words in your own unique style and context. Show how you use them in daily conversation...",
            key="word_explanation_text"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(L["new_words"], key="new_words_btn", use_container_width=True):
            st.session_state["current_words"] = get_words()
            st.balloons()
            st.rerun()
        
        # Add word difficulty indicator
        difficulty = random.choice(["Easy 🟢", "Medium 🟡", "Hard 🔴"])
        st.markdown(f"""
        <div style="text-align: center; margin-top: 1rem; padding: 0.5rem; 
                   background: rgba(255,255,255,0.2); border-radius: 10px;">
            <small>Difficulty: {difficulty}</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Navigation and Submit
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button(L["back_to_corpus"], key="back_to_corpus", use_container_width=True):
            st.session_state.current_page = 'main'
            st.rerun()
    
    with col2:
        if explanation and explanation.strip():
            if st.button("🎯 Submit Contribution", key="submit_contribution", use_container_width=True):
                submit_contribution(user_data, corpus_data, explanation, words, L)

def check_achievements(user_data, total_contributions, total_score, score):
    """Check for new achievements and show popups"""
    achievements_unlocked = []
    
    # Milestone achievements
    if total_contributions == 1:
        achievements_unlocked.append({"title": "First Steps", "icon": "👶", "desc": "Made your first contribution"})
    elif total_contributions == 5:
        achievements_unlocked.append({"title": "High Five", "icon": "✋", "desc": "Made 5 contributions"})
    elif total_contributions == 10:
        achievements_unlocked.append({"title": "Perfect Ten", "icon": "🔟", "desc": "Made 10 contributions"})
    elif total_contributions == 25:
        achievements_unlocked.append({"title": "Quarter Master", "icon": "🏅", "desc": "Made 25 contributions"})
    
    # Score achievements
    if score == 10:
        achievements_unlocked.append({"title": "Perfect Shot", "icon": "🎯", "desc": "Got a perfect score!"})
    
    # Level up achievements
    _, new_level = get_user_level(total_score)
    _, old_level = get_user_level(total_score - score)
    
    if new_level > old_level:
        achievements_unlocked.append({"title": "Level Up!", "icon": "🆙", "desc": f"Reached Level {new_level}!"})
    
    return achievements_unlocked
def submit_contribution(user_data, corpus_data, explanation, words, L):
    """Submit user contribution"""
    try:
        # Calculate score
        score = get_score(explanation, words)
        
        # Apply combo multiplier
        df = pd.DataFrame()
        if os.path.exists(CSV_FILE):
            try:
                df = pd.read_csv(CSV_FILE)
            except:
                df = pd.DataFrame()
        
        nickname = user_data.get("nickname", "")
        user_contributions = df[df["nickname"] == nickname] if nickname and not df.empty else pd.DataFrame()
        
        if len(user_contributions) >= 3:
            recent_scores = user_contributions.tail(5)["score"].tolist()
            multiplier = calculate_combo_multiplier(recent_scores)
            bonus_points = int(score * (multiplier - 1))
            total_score_earned = score + bonus_points
        else:
            multiplier = 1.0
            bonus_points = 0
            total_score_earned = score
        
        level = "🥉 Bronze"
        if total_score_earned >= 7:
            level = "🥇 Gold"
        elif total_score_earned >= 4:
            level = "🥈 Silver"
        
        # Prepare data
        data = {
            **user_data,
            **corpus_data,
            "explanation": explanation,
            "words": ", ".join(words),
            "score": total_score_earned,
            "base_score": score,
            "bonus_points": bonus_points,
            "multiplier": multiplier,
            "level": level,
            "datetime": str(datetime.now())
        }
        
        # Save to CSV
        df_new = pd.DataFrame([data])
        if os.path.exists(CSV_FILE):
            df = pd.read_csv(CSV_FILE)
            df = pd.concat([df, df_new], ignore_index=True)
        else:
            df = df_new
        df.to_csv(CSV_FILE, index=False)
        
        # Check for achievements
        total_contributions = len(df[df["nickname"] == nickname])
        total_user_score = df[df["nickname"] == nickname]["score"].sum()
        achievements = check_achievements(user_data, total_contributions, total_user_score, total_score_earned)
        
        # Success message
        success_message = f"🎉 Contribution Successfully Submitted!<br>"
        success_message += f"<div style='font-size: 1.2rem; margin-top: 1rem;'>"
        success_message += f"Base Score: {score}/10"
        
        if bonus_points > 0:
            success_message += f"<br>🔥 Combo Bonus: +{bonus_points} points ({multiplier}x multiplier)"
            success_message += f"<br><strong>Total Score: {total_score_earned}/10</strong>"
        
        success_message += f"<br>Level: {level}</div>"
        
        st.markdown(f"""
        <div class="score-card">
            {success_message}
        </div>
        """, unsafe_allow_html=True)
        
        # Show achievement popups
        for achievement in achievements:
            show_achievement_popup(achievement)
        
        st.balloons()
        
        # Add confetti for high scores
        if total_score_earned >= 8:
            st.snow()
        
        # Reset for next contribution
        st.session_state["current_words"] = get_words()
        st.session_state.corpus_data = {}
        
        # Show continue button instead of auto-redirect
        if st.button("🚀 Continue Playing", key="continue_playing", use_container_width=True):
            st.session_state.current_page = 'main'
            st.rerun()
        
    except Exception as e:
        st.markdown(f'<div class="error-message">❌ Error saving data: {str(e)}</div>', unsafe_allow_html=True)