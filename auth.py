import streamlit as st
import folium
from streamlit_folium import st_folium

def is_logged_in():
    """Check if user is logged in"""
    return st.session_state.get('logged_in', False)

def show_login_page(L):
    """Display login page"""
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 3rem;">
        <h1 class="stTitle">{L["title"]}</h1>
        <p style="font-size: 1.3rem; color: #7f8c8d; font-weight: 500;">{L["subtitle"]}</p>
        <div class="progress-bar"></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<div class="step-header glow-effect">{L["login_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-card"><p style="font-size: 1.1rem;">{L["login_subtitle"]}</p></div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        # Personal Details
        st.markdown("### 👤 Personal Information")
        col1, col2 = st.columns(2)
        
        with col1:
            nickname = st.text_input(L["nickname"], placeholder="Enter your nickname", key="login_nickname")
            name = st.text_input(L["name"], placeholder="Your full name", key="login_name")
            age = st.number_input(L["age"], min_value=10, max_value=100, value=25, key="login_age")
        
        with col2:
            gender = st.selectbox(L["gender"], ["Male", "Female", "Other", "Prefer not to say"], key="login_gender")
            education = st.selectbox(L["education"], 
                                   ["School", "Intermediate", "Graduate", "Post-Graduate", "PhD", "Other"], 
                                   key="login_education")
            occupation = st.text_input(L["occupation"], placeholder="Your occupation", key="login_occupation")
        
        st.markdown("---")
        
        # Location Details
        st.markdown("### 🌍 Location Information")
        geo_area = st.text_input(L["geo"], placeholder="e.g., Hyderabad, Telangana", key="login_geo")
        
        st.markdown(f"**{L['coordinates']}**")
        col_lat, col_lon = st.columns(2)
        with col_lat:
            latitude = st.number_input(L["latitude"], value=17.3850, format="%.6f", key="login_lat")
        with col_lon:
            longitude = st.number_input(L["longitude"], value=78.4867, format="%.6f", key="login_lon")
        
        # Location button
        if st.button(L["get_location"], key="get_location_btn"):
            st.markdown('<div class="warning-message">📍 Please manually enter your coordinates above or use your device\'s GPS</div>', unsafe_allow_html=True)
        
        # Map display
        if latitude and longitude and geo_area:
            st.markdown("### 🗺️ Your Location Preview")
            try:
                m = folium.Map(location=[latitude, longitude], zoom_start=12)
                folium.Marker([latitude, longitude], popup=geo_area, tooltip=geo_area).add_to(m)
                st_folium(m, width=600, height=300)
            except Exception as e:
                st.warning(f"Map display error: {str(e)}")
        
        st.markdown("---")
        
        # Login button
        if st.button(L["login_btn"], key="login_submit", type="primary"):
            # Validate all required fields
            required_fields = [nickname, name, geo_area, education, occupation]
            
            if not all(required_fields) or not latitude or not longitude:
                st.markdown('<div class="error-message">❌ ' + L["validation_error"] + '</div>', unsafe_allow_html=True)
            else:
                # Save user data
                st.session_state.user_data = {
                    "nickname": nickname,
                    "name": name,
                    "age": age,
                    "gender": gender,
                    "education": education,
                    "occupation": occupation,
                    "geo_area": geo_area,
                    "latitude": latitude,
                    "longitude": longitude
                }
                
                st.session_state.logged_in = True
                st.session_state.current_page = 'main'
                st.markdown('<div class="success-message">✅ ' + L["login_success"] + '</div>', unsafe_allow_html=True)
                st.balloons()
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)