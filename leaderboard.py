import streamlit as st
import pandas as pd
import os
from gamification import get_user_level

CSV_FILE = "userdata.csv"

def show_leaderboard(L):
    """Display leaderboard page"""
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 3rem;">
        <h1 class="stTitle">🏆 Leaderboard</h1>
        <p style="font-size: 1.3rem; color: #7f8c8d; font-weight: 500;">Champions of Telugu Slang</p>
        <div class="progress-bar"></div>
    </div>
    """, unsafe_allow_html=True)
    
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            if not df.empty:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f'<div class="step-header">{L["top_contributors"]}</div>', unsafe_allow_html=True)
                    leaderboard = (
                        df.groupby("nickname")["score"]
                        .agg(['sum', 'count'])
                        .reset_index()
                        .sort_values(by="sum", ascending=False)
                        .head(10)
                    )
                    leaderboard.columns = ["Nickname", "Total Score", "Contributions"]
                    
                    # Add rank and medals
                    leaderboard["Rank"] = range(1, len(leaderboard) + 1)
                    leaderboard["Medal"] = ["🥇", "🥈", "🥉"] + ["🏅"] * 7
                    leaderboard = leaderboard[["Rank", "Medal", "Nickname", "Total Score", "Contributions"]]
                    
                    # Add level information
                    leaderboard["Level"] = leaderboard["Total Score"].apply(lambda x: get_user_level(x)[1])
                    
                    st.dataframe(leaderboard, use_container_width=True, hide_index=True)
                    
                    # Crown for #1 player
                    if len(leaderboard) > 0:
                        st.markdown(f"""
                        <div style="text-align: center; margin-top: 1rem;">
                            <div class="leaderboard-crown">👑</div>
                            <h4>Current Champion: {leaderboard.iloc[0]['Nickname']}</h4>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col2:
                    # User's personal stats
                    user_nickname = st.session_state.user_data.get("nickname", "")
                    if user_nickname:
                        user_data = df[df["nickname"] == user_nickname]
                        if not user_data.empty:
                            total_score = user_data["score"].sum()
                            total_contributions = len(user_data)
                            avg_score = user_data["score"].mean()
                            level_name, level_num = get_user_level(total_score)
                            
                            # Calculate user rank
                            user_rank = (df.groupby("nickname")["score"].sum().sort_values(ascending=False).reset_index()
                                       .reset_index().set_index("nickname").loc[user_nickname, "index"] + 1)
                            
                            st.markdown(f"""
                            <div class="metric-card glow-effect">
                                <h3>{L['your_score']}</h3>
                                <h2 style="color: #667eea; font-size: 2.5rem;">{total_score}</h2>
                                <p><strong>Rank:</strong> #{user_rank}</p>
                                <p><strong>Level:</strong> {level_name}</p>
                                <p><strong>Contributions:</strong> {total_contributions}</p>
                                <p><strong>Average:</strong> {avg_score:.1f}/10</p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Weekly challenge
                    st.markdown(f"""
                    <div class="challenge-card">
                        <h4>🏆 Weekly Challenge</h4>
                        <p><strong>Top the Leaderboard!</strong></p>
                        <p>Be #1 this week to earn the Champion badge!</p>
                        <small>Resets every Monday</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Platform Statistics
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>📊 Platform Stats</h4>
                        <p><strong>Total Users:</strong> {df['nickname'].nunique()}</p>
                        <p><strong>Total Contributions:</strong> {len(df)}</p>
                        <p><strong>Average Score:</strong> {df['score'].mean():.1f}/10</p>
                        <p><strong>Highest Score:</strong> {df['score'].max()}/10</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
        except Exception as e:
            st.markdown(f'<div class="error-message">❌ Error loading data: {str(e)}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="info-card">
            <h4>🎯 Be the First!</h4>
            <p>No contributions yet. Be the first to contribute and claim the top spot!</p>
        </div>
        """, unsafe_allow_html=True)