"""
CE-LIMS Authentication Module
Handles user authentication and role-based access control
"""

import streamlit as st
from database import get_connection, hash_password
import json

def check_authentication():
    """Check if user is authenticated"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    return st.session_state.authenticated

def login(username, password):
    """Authenticate user and set session"""
    conn = get_connection()
    cursor = conn.cursor()
    
    hashed_password = hash_password(password)
    
    cursor.execute("""
        SELECT id, username, full_name, full_name_ar, role, email, is_active
        FROM users
        WHERE username = ? AND password = ? AND is_active = 1
    """, (username, hashed_password))
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        st.session_state.authenticated = True
        st.session_state.user = {
            'id': user['id'],
            'username': user['username'],
            'full_name': user['full_name'],
            'full_name_ar': user['full_name_ar'],
            'role': user['role'],
            'email': user['email']
        }
        return True
    return False

def logout():
    """Logout user and clear session"""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.rerun()

def get_current_user():
    """Get current logged in user"""
    return st.session_state.user if 'user' in st.session_state else None

def check_role(allowed_roles):
    """Check if current user has required role"""
    user = get_current_user()
    if not user:
        return False
    return user['role'] in allowed_roles

def get_role_name(role):
    """Get role display name"""
    role_names = {
        'field_tech': ('Field Technician', 'فني ميداني'),
        'supervisor': ('Supervisor', 'مشرف'),
        'lab_tech': ('Lab Technician', 'فني مختبر'),
        'manager': ('Manager', 'مدير')
    }
    return role_names.get(role, ('Unknown', 'غير معروف'))

def show_login_page():
    """Display login page"""
    
    # Custom CSS for login page
    st.markdown("""
        <style>
        .login-container {
            max-width: 400px;
            margin: 100px auto;
            padding: 2rem;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .login-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        .login-logo {
            font-size: 3rem;
            color: #151f32;
            margin-bottom: 1rem;
        }
        .login-title {
            font-size: 1.5rem;
            font-weight: bold;
            color: #151f32;
            margin-bottom: 0.5rem;
        }
        .login-subtitle {
            color: #6b7280;
            font-size: 0.9rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div class="login-header">
                <div class="login-logo">🏗️</div>
                <div class="login-title">CE-LIMS</div>
                <div class="login-subtitle">Civil Engineering Laboratory Information Management System</div>
                <div class="login-subtitle" style="direction: rtl;">نظام إدارة معلومات مختبر الهندسة المدنية</div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username / اسم المستخدم", key="username_input")
            password = st.text_input("Password / كلمة المرور", type="password", key="password_input")
            
            col_a, col_b = st.columns(2)
            with col_a:
                submit = st.form_submit_button("Login / دخول", use_container_width=True)
            
            if submit:
                if username and password:
                    if login(username, password):
                        st.success("✅ Login successful! / تم تسجيل الدخول بنجاح!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials / بيانات غير صحيحة")
                else:
                    st.warning("⚠️ Please enter username and password / الرجاء إدخال اسم المستخدم وكلمة المرور")
        
        # Show demo credentials
        with st.expander("🔑 Demo Credentials / بيانات تجريبية"):
            st.markdown("""
                **Field Tech:** `ahmed` / `123456`  
                **Supervisor:** `sara` / `123456`  
                **Lab Tech:** `omar` / `123456`  
                **Manager:** `fatima` / `123456`
            """)
