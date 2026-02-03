"""
CE-LIMS Main Application
Civil Engineering Laboratory Information Management System
ISO 17025 Compliant
"""

import streamlit as st
from auth import check_authentication, show_login_page, logout, get_current_user
from database import init_database
import os

# Page configuration
st.set_page_config(
    page_title="CE-LIMS",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize database if not exists
if not os.path.exists("ce_lims.db"):
    init_database()

# Check authentication
if not check_authentication():
    show_login_page()
else:
    user = get_current_user()
    
    # Route to appropriate dashboard based on role
    if user['role'] == 'field_tech':
        from field_tech import show_field_tech_dashboard
        show_field_tech_dashboard()
    
    elif user['role'] == 'supervisor':
        from supervisor import show_supervisor_dashboard
        show_supervisor_dashboard()
    
    elif user['role'] == 'lab_tech':
        from lab_tech import show_lab_tech_dashboard
        show_lab_tech_dashboard()
    
    elif user['role'] == 'manager':
        from manager import show_manager_dashboard
        show_manager_dashboard()
    
    else:
        st.error("❌ Invalid user role / دور المستخدم غير صالح")
    
    # Logout button in sidebar
    with st.sidebar:
        st.markdown("---")
        if st.button("🚪 Logout / تسجيل الخروج", use_container_width=True):
            logout()
