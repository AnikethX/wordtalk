import streamlit as st
import os

CSV_FILE = "userdata.csv"

def show_admin_panel():
    """Display admin panel in sidebar"""
    st.markdown("---")
    st.markdown("### 🔐 Admin Panel")
    admin_key = st.text_input("Admin Key", type="password")
    
    if admin_key == "admin@123":
        st.success("✅ Admin access granted!")
        
        if os.path.exists(CSV_FILE):
            with open(CSV_FILE, "rb") as file:
                st.download_button(
                    label="⬇️ Download Data",
                    data=file,
                    file_name="WordTalk_Contributions.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        
        if st.button("🗑️ Reset Data", use_container_width=True):
            try:
                if os.path.exists(CSV_FILE):
                    os.remove(CSV_FILE)
                    st.success("✅ Data reset successfully!")
                    st.rerun()
                else:
                    st.info("No data file found to reset")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    elif admin_key:
        st.error("❌ Invalid Admin Key")