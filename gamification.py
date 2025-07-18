import streamlit as st
import random
from datetime import datetime, timedelta
import pandas as pd
import os

def get_user_level(total_score):
    """Calculate user level based on total score"""
    if total_score >= 1000:
        return "🏆 Slang Master", 10
    elif total_score >= 500:
        return "👑 Word Wizard", 9
    elif total_score >= 300:
        return "🌟 Language Legend", 8
    elif total_score >= 200:
        return "🎯 Slang Expert", 7
    elif total_score >= 150:
        return "🚀 Word Warrior", 6
    elif total_score >= 100:
        return "💎 Phrase Pro", 5
    elif total_score >= 70:
        return "🔥 Slang Scholar", 4
    elif total_score >= 50:
        return "⭐ Word Explorer", 3
    elif total_score >= 25:
        return "🌱 Language Learner", 2
    else:
        return "🐣 Slang Rookie", 1

def get_achievements(user_data, df):
    """Get user achievements based on their activity"""
    achievements = []
    nickname = user_data.get("nickname", "")
    
    if nickname and not df.empty:
        user_contributions = df[df["nickname"] == nickname]
        total_contributions = len(user_contributions)
        total_score = user_contributions["score"].sum()
        avg_score = user_contributions["score"].mean() if total_contributions > 0 else 0
        
        # Contribution-based achievements
        if total_contributions >= 100:
            achievements.append({"title": "Century Club", "icon": "💯", "desc": "Made 100+ contributions"})
        elif total_contributions >= 50:
            achievements.append({"title": "Half Century", "icon": "🎯", "desc": "Made 50+ contributions"})
        elif total_contributions >= 25:
            achievements.append({"title": "Quarter Master", "icon": "🏅", "desc": "Made 25+ contributions"})
        elif total_contributions >= 10:
            achievements.append({"title": "Perfect Ten", "icon": "🔟", "desc": "Made 10+ contributions"})
        elif total_contributions >= 5:
            achievements.append({"title": "High Five", "icon": "✋", "desc": "Made 5+ contributions"})
        elif total_contributions >= 1:
            achievements.append({"title": "First Steps", "icon": "👶", "desc": "Made your first contribution"})
        
        # Score-based achievements
        if avg_score >= 9:
            achievements.append({"title": "Perfectionist", "icon": "💎", "desc": "Average score 9+"})
        elif avg_score >= 8:
            achievements.append({"title": "Excellence", "icon": "⭐", "desc": "Average score 8+"})
        elif avg_score >= 7:
            achievements.append({"title": "Quality Control", "icon": "✅", "desc": "Average score 7+"})
        
        # Special achievements
        if total_score >= 500:
            achievements.append({"title": "Score Master", "icon": "🏆", "desc": "Earned 500+ total points"})
        
        # Check for perfect scores
        perfect_scores = len(user_contributions[user_contributions["score"] == 10])
        if perfect_scores >= 10:
            achievements.append({"title": "Perfect Storm", "icon": "⚡", "desc": "10+ perfect scores"})
        elif perfect_scores >= 5:
            achievements.append({"title": "Flawless Five", "icon": "🌟", "desc": "5+ perfect scores"})
        elif perfect_scores >= 1:
            achievements.append({"title": "Perfect Shot", "icon": "🎯", "desc": "First perfect score"})
    
    return achievements

def get_daily_challenge():
    """Get today's daily challenge"""
    challenges = [
        {"title": "Speed Demon", "desc": "Submit 5 contributions in under 10 minutes", "reward": "50 XP", "icon": "⚡"},
        {"title": "Quality Master", "desc": "Get an average score of 8+ today", "reward": "75 XP", "icon": "💎"},
        {"title": "Streak Builder", "desc": "Maintain your daily streak", "reward": "25 XP", "icon": "🔥"},
        {"title": "Explorer", "desc": "Try 3 different word categories", "reward": "40 XP", "icon": "🗺️"},
        {"title": "Perfectionist", "desc": "Get 3 perfect scores (10/10)", "reward": "100 XP", "icon": "⭐"},
        {"title": "Social Butterfly", "desc": "Use 10+ social media slang words", "reward": "60 XP", "icon": "📱"},
        {"title": "Culture Keeper", "desc": "Focus on folk language today", "reward": "80 XP", "icon": "🏛️"}
    ]
    
    # Use date as seed for consistent daily challenge
    today = datetime.now().date()
    random.seed(str(today))
    return random.choice(challenges)

def get_streak_count(nickname, df):
    """Calculate user's current streak"""
    if df.empty or nickname not in df["nickname"].values:
        return 0
    
    user_data = df[df["nickname"] == nickname].copy()
    user_data["date"] = pd.to_datetime(user_data["datetime"]).dt.date
    unique_dates = sorted(user_data["date"].unique(), reverse=True)
    
    if not unique_dates:
        return 0
    
    streak = 0
    current_date = datetime.now().date()
    
    for date in unique_dates:
        if date == current_date or date == current_date - timedelta(days=streak):
            streak += 1
            current_date = date
        else:
            break
    
    return streak

def calculate_combo_multiplier(recent_scores):
    """Calculate combo multiplier based on recent performance"""
    if len(recent_scores) < 3:
        return 1.0
    
    # Check for consecutive high scores
    high_scores = [score >= 7 for score in recent_scores[-5:]]
    consecutive_high = 0
    
    for score in reversed(high_scores):
        if score:
            consecutive_high += 1
        else:
            break
    
    if consecutive_high >= 5:
        return 2.5
    elif consecutive_high >= 4:
        return 2.0
    elif consecutive_high >= 3:
        return 1.5
    else:
        return 1.0

def get_power_ups():
    """Get available power-ups"""
    return [
        {"name": "Double XP", "desc": "2x points for next 3 contributions", "cost": "100 XP", "icon": "⚡"},
        {"name": "Word Hint", "desc": "Get a hint for difficult words", "cost": "50 XP", "icon": "💡"},
        {"name": "Streak Shield", "desc": "Protect your streak for 1 day", "cost": "75 XP", "icon": "🛡️"},
        {"name": "Lucky Draw", "desc": "Get easier words for next round", "cost": "60 XP", "icon": "🍀"}
    ]

def show_achievement_popup(achievement):
    """Show achievement popup"""
    st.markdown(f"""
    <div class="achievement-popup">
        <div style="font-size: 3rem; margin-bottom: 1rem;">{achievement['icon']}</div>
        <h2>Achievement Unlocked!</h2>
        <h3>{achievement['title']}</h3>
        <p>{achievement['desc']}</p>
    </div>
    """, unsafe_allow_html=True)

def show_gamification_sidebar(user_data, df):
    """Show gamification elements in sidebar"""
    if not user_data:
        return
    
    nickname = user_data.get("nickname", "")
    
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🎮 Game Stats")
        
        if nickname and not df.empty:
            user_contributions = df[df["nickname"] == nickname]
            total_score = user_contributions["score"].sum()
            level_name, level_num = get_user_level(total_score)
            streak = get_streak_count(nickname, df)
            
            # Level display
            st.markdown(f"""
            <div class="level-badge">
                Level {level_num}: {level_name}
            </div>
            """, unsafe_allow_html=True)
            
            # XP Bar
            next_level_xp = [25, 50, 70, 100, 150, 200, 300, 500, 1000, 2000][level_num-1] if level_num < 10 else 2000
            current_xp = total_score % next_level_xp if level_num < 10 else total_score
            xp_percentage = (current_xp / next_level_xp) * 100 if level_num < 10 else 100
            
            st.markdown(f"""
            <div class="xp-bar">
                <div class="xp-fill" style="width: {xp_percentage}%"></div>
            </div>
            <p style="text-align: center; margin: 0.5rem 0;">
                XP: {current_xp}/{next_level_xp}
            </p>
            """, unsafe_allow_html=True)
            
            # Streak counter
            if streak > 0:
                st.markdown(f"""
                <div class="streak-counter">
                    🔥 {streak} Day Streak!
                </div>
                """, unsafe_allow_html=True)
            
            # Recent combo
            if len(user_contributions) >= 3:
                recent_scores = user_contributions.tail(5)["score"].tolist()
                multiplier = calculate_combo_multiplier(recent_scores)
                if multiplier > 1.0:
                    st.markdown(f"""
                    <div class="combo-multiplier">
                        🎯 {multiplier}x Combo!
                    </div>
                    """, unsafe_allow_html=True)
        
        # Daily Challenge
        challenge = get_daily_challenge()
        st.markdown(f"""
        <div class="daily-challenge">
            <h4>📅 Daily Challenge</h4>
            <div style="font-size: 2rem; margin: 1rem 0;">{challenge['icon']}</div>
            <h5>{challenge['title']}</h5>
            <p>{challenge['desc']}</p>
            <small>Reward: {challenge['reward']}</small>
        </div>
        """, unsafe_allow_html=True)

def show_achievements_page(user_data, df, L):
    """Show achievements page"""
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 3rem;">
        <h1 class="stTitle">🏆 Achievements</h1>
        <p style="font-size: 1.3rem; color: #7f8c8d; font-weight: 500;">Your Gaming Journey</p>
        <div class="progress-bar"></div>
    </div>
    """, unsafe_allow_html=True)
    
    achievements = get_achievements(user_data, df)
    
    if achievements:
        cols = st.columns(3)
        for i, achievement in enumerate(achievements):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="metric-card glow-effect">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">{achievement['icon']}</div>
                    <h4>{achievement['title']}</h4>
                    <p>{achievement['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-card">
            <h4>🎯 Start Your Journey!</h4>
            <p>Make your first contribution to unlock achievements!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Power-ups section
    st.markdown('<div class="step-header">⚡ Power-ups Shop</div>', unsafe_allow_html=True)
    
    power_ups = get_power_ups()
    cols = st.columns(2)
    
    for i, power_up in enumerate(power_ups):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="power-up-card">
                <div style="font-size: 2rem; margin-bottom: 1rem;">{power_up['icon']}</div>
                <h5>{power_up['name']}</h5>
                <p>{power_up['desc']}</p>
                <small>Cost: {power_up['cost']}</small>
            </div>
            """, unsafe_allow_html=True)