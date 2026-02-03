"""
CE-LIMS Shared Components
Modern Dark Mode Design with Blue Accent
"""

import streamlit as st
from auth import get_current_user, logout, get_role_name

def load_custom_css():
    """Load custom CSS with modern dark mode design"""
    st.markdown("""
        <style>
        /* Import fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Cairo:wght@400;600;700&display=swap');
        
        /* Global styles - Dark Mode */
        .stApp {
            background-color: #101922;
            color: #e2e8f0;
        }
        
        /* Hide Streamlit default elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Custom header - Dark with blue accent */
        .custom-header {
            background-color: #1a2632;
            border-bottom: 1px solid #334155;
            color: white;
            padding: 1rem 2rem;
            margin: -1rem -1rem 2rem -1rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        }
        
        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .logo-section {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .logo-icon {
            background: #137fec;
            width: 36px;
            height: 36px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            font-weight: bold;
            color: white;
            box-shadow: 0 4px 12px rgba(19, 127, 236, 0.3);
        }
        
        .logo-text {
            font-size: 1.25rem;
            font-weight: bold;
            font-family: 'Inter', sans-serif;
            color: white;
        }
        
        .logo-subtext {
            font-size: 0.7rem;
            color: #94a3b8;
            font-family: 'Cairo', sans-serif;
        }
        
        .nav-links {
            display: flex;
            gap: 2rem;
            font-size: 0.9rem;
        }
        
        .nav-link {
            color: #94a3b8;
            text-decoration: none;
            transition: color 0.2s;
        }
        
        .nav-link:hover {
            color: #137fec;
        }
        
        .nav-link.active {
            color: #137fec;
            border-bottom: 2px solid #137fec;
            padding-bottom: 1.25rem;
        }
        
        .user-profile {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        
        .user-avatar {
            background: linear-gradient(135deg, #137fec 0%, #0f62b5 100%);
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            box-shadow: 0 2px 8px rgba(19, 127, 236, 0.3);
        }
        
        .user-info {
            text-align: right;
            font-size: 0.75rem;
            line-height: 1.2;
        }
        
        .user-name {
            font-weight: 500;
            color: white;
        }
        
        .user-role {
            color: #94a3b8;
            font-family: 'Cairo', sans-serif;
        }
        
        /* Page title bar */
        .page-title-bar {
            background: linear-gradient(135deg, #1a2632 0%, #15202b 100%);
            border-bottom: 1px solid #334155;
            color: white;
            padding: 1.25rem 2rem;
            margin: -1rem -1rem 2rem -1rem;
            text-align: center;
        }
        
        .page-title {
            font-size: 1.5rem;
            font-weight: 600;
            font-family: 'Inter', 'Cairo', sans-serif;
        }
        
        /* Cards - Dark surface */
        .custom-card {
            background: #1a2632;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            border: 1px solid #334155;
            margin-bottom: 1.5rem;
            transition: all 0.2s;
        }
        
        .custom-card:hover {
            box-shadow: 0 4px 16px rgba(19, 127, 236, 0.15);
            border-color: #137fec;
        }
        
        .card-header {
            border-bottom: 1px solid #334155;
            padding-bottom: 1rem;
            margin-bottom: 1rem;
            background: linear-gradient(to bottom, #1e2936 0%, #1a2632 100%);
            margin: -1.5rem -1.5rem 1rem -1.5rem;
            padding: 1.25rem 1.5rem;
            border-radius: 12px 12px 0 0;
        }
        
        .card-title {
            font-size: 1.125rem;
            font-weight: bold;
            color: white;
            font-family: 'Inter', 'Cairo', sans-serif;
        }
        
        /* Bilingual text */
        .bilingual {
            display: flex;
            align-items: baseline;
            gap: 0.5rem;
        }
        
        .separator {
            color: #64748b;
        }
        
        .arabic-text {
            font-family: 'Cairo', sans-serif;
        }
        
        /* Badges */
        .badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        
        .badge-warning {
            background-color: rgba(251, 191, 36, 0.15);
            color: #fbbf24;
            border: 1px solid rgba(251, 191, 36, 0.3);
        }
        
        .badge-success {
            background-color: rgba(34, 197, 94, 0.15);
            color: #22c55e;
            border: 1px solid rgba(34, 197, 94, 0.3);
        }
        
        .badge-info {
            background-color: rgba(19, 127, 236, 0.15);
            color: #137fec;
            border: 1px solid rgba(19, 127, 236, 0.3);
        }
        
        .badge-danger {
            background-color: rgba(239, 68, 68, 0.15);
            color: #ef4444;
            border: 1px solid rgba(239, 68, 68, 0.3);
        }
        
        /* Form inputs - Dark mode */
        .stTextInput input, .stNumberInput input, .stSelectbox select, .stTextArea textarea {
            background-color: #15202b !important;
            color: #e2e8f0 !important;
            border: 1px solid #334155 !important;
            border-radius: 8px !important;
        }
        
        .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox select:focus, .stTextArea textarea:focus {
            border-color: #137fec !important;
            box-shadow: 0 0 0 2px rgba(19, 127, 236, 0.2) !important;
            background-color: #1a2632 !important;
        }
        
        /* Labels */
        .stTextInput label, .stNumberInput label, .stSelectbox label, .stTextArea label {
            color: #cbd5e1 !important;
            font-weight: 500 !important;
        }
        
        /* Buttons - Blue accent */
        .stButton button {
            border-radius: 8px;
            font-weight: 600;
            padding: 0.625rem 1.75rem;
            transition: all 0.2s;
            border: none;
        }
        
        .stButton button[kind="primary"] {
            background: linear-gradient(135deg, #137fec 0%, #0f62b5 100%);
            color: white;
            box-shadow: 0 4px 12px rgba(19, 127, 236, 0.3);
        }
        
        .stButton button[kind="primary"]:hover {
            background: linear-gradient(135deg, #0f62b5 0%, #0c4d8f 100%);
            transform: translateY(-1px);
            box-shadow: 0 6px 16px rgba(19, 127, 236, 0.4);
        }
        
        .stButton button[kind="secondary"] {
            background-color: #334155;
            color: #e2e8f0;
        }
        
        .stButton button[kind="secondary"]:hover {
            background-color: #475569;
        }
        
        /* Progress bar */
        .progress-container {
            margin-top: 1rem;
        }
        
        .progress-label {
            display: flex;
            justify-content: space-between;
            font-size: 0.75rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: #cbd5e1;
        }
        
        .progress-bar {
            width: 100%;
            height: 10px;
            background-color: #1e293b;
            border-radius: 9999px;
            overflow: hidden;
            border: 1px solid #334155;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #137fec 0%, #0f62b5 100%);
            border-radius: 9999px;
            transition: width 0.3s;
            box-shadow: 0 0 10px rgba(19, 127, 236, 0.5);
        }
        
        /* Data display */
        .data-row {
            padding: 0.75rem 0;
            border-bottom: 1px solid #334155;
        }
        
        .data-row:last-child {
            border-bottom: none;
        }
        
        .data-label {
            font-weight: 600;
            color: #94a3b8;
            font-size: 0.875rem;
            margin-bottom: 0.25rem;
        }
        
        .data-value {
            color: #e2e8f0;
            font-size: 0.875rem;
        }
        
        /* Upload area */
        .upload-area {
            border: 2px dashed #334155;
            border-radius: 12px;
            background: linear-gradient(135deg, rgba(19, 127, 236, 0.05) 0%, rgba(26, 38, 50, 0.5) 100%);
            padding: 2.5rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .upload-area:hover {
            background: linear-gradient(135deg, rgba(19, 127, 236, 0.1) 0%, rgba(26, 38, 50, 0.7) 100%);
            border-color: #137fec;
            box-shadow: 0 4px 16px rgba(19, 127, 236, 0.2);
        }
        
        .upload-icon {
            background: linear-gradient(135deg, #137fec 0%, #0f62b5 100%);
            color: white;
            width: 64px;
            height: 64px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            margin-bottom: 1rem;
            box-shadow: 0 6px 20px rgba(19, 127, 236, 0.4);
        }
        
        /* Footer */
        .custom-footer {
            text-align: center;
            padding: 2rem;
            color: #64748b;
            font-size: 0.75rem;
            margin-top: 3rem;
            border-top: 1px solid #334155;
        }
        
        /* Table styles - Dark mode */
        .dataframe {
            font-size: 0.875rem !important;
            background-color: #1a2632 !important;
        }
        
        .dataframe th {
            background: linear-gradient(135deg, #137fec 0%, #0f62b5 100%) !important;
            font-weight: 600 !important;
            color: white !important;
            border: 1px solid #334155 !important;
        }
        
        .dataframe td {
            color: #e2e8f0 !important;
            background-color: #15202b !important;
            border: 1px solid #334155 !important;
        }
        
        .dataframe tr:hover td {
            background-color: #1a2632 !important;
        }
        
        /* Selectbox dropdown */
        .stSelectbox div[data-baseweb="select"] {
            background-color: #15202b !important;
        }
        
        /* File uploader */
        .stFileUploader {
            background-color: #1a2632 !important;
            border: 1px solid #334155 !important;
            border-radius: 8px !important;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .nav-links {
                display: none;
            }
            
            .page-title {
                font-size: 1.25rem;
            }
        }
        </style>
    """, unsafe_allow_html=True)

def show_header(active_page="dashboard"):
    """Display custom header with dark mode"""
    user = get_current_user()
    role_en, role_ar = get_role_name(user['role'])
    
    # Get first letter for avatar
    initial = user['full_name'][0].upper() if user['full_name'] else 'U'
    
    st.markdown(f"""
        <div class="custom-header">
            <div class="header-content">
                <div class="logo-section">
                    <div class="logo-icon">L</div>
                    <div>
                        <div class="logo-text">CE-LIMS</div>
                        <div class="logo-subtext">نظام إدارة المختبر</div>
                    </div>
                </div>
                <div class="user-profile">
                    <div class="user-avatar">{initial}</div>
                    <div class="user-info">
                        <div class="user-name">{role_en}: {user['full_name']}</div>
                        <div class="user-role">{role_ar}: {user['full_name_ar']}</div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def show_page_title(title_en, title_ar):
    """Display page title bar"""
    st.markdown(f"""
        <div class="page-title-bar">
            <div class="page-title">
                {title_en} / {title_ar}
            </div>
        </div>
    """, unsafe_allow_html=True)

def show_card(title_en, title_ar, content):
    """Display a custom card"""
    st.markdown(f"""
        <div class="custom-card">
            <div class="card-header">
                <div class="card-title">{title_en} / {title_ar}</div>
            </div>
            {content}
        </div>
    """, unsafe_allow_html=True)

def show_badge(text, badge_type="warning"):
    """Display a status badge"""
    return f'<span class="badge badge-{badge_type}">{text}</span>'

def show_progress(label_en, label_ar, percentage):
    """Display a progress bar"""
    return f"""
        <div class="progress-container">
            <div class="progress-label">
                <span>{label_en} / {label_ar}</span>
                <span>{percentage}%</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {percentage}%"></div>
            </div>
        </div>
    """

def show_data_row(label_en, label_ar, value):
    """Display a data row"""
    return f"""
        <div class="data-row">
            <div class="data-label">{label_en} / {label_ar}</div>
            <div class="data-value">{value}</div>
        </div>
    """

def show_footer():
    """Display custom footer"""
    st.markdown("""
        <div class="custom-footer">
            © 2024 CE-LIMS. All rights reserved. / جميع الحقوق محفوظة.
        </div>
    """, unsafe_allow_html=True)
