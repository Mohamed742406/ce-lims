"""
CE-LIMS Shared Components
Reusable UI components matching the design mockup
"""

import streamlit as st
from auth import get_current_user, logout, get_role_name

def load_custom_css():
    """Load custom CSS matching the mockup design"""
    st.markdown("""
        <style>
        /* Import fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Tajawal:wght@400;500;700&display=swap');
        
        /* Global styles */
        .stApp {
            background: linear-gradient(135deg, #1a1a1a 0%, #0a0a0a 100%);
        }
        
        /* Hide Streamlit default elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Custom header */
        .custom-header {
            background: linear-gradient(135deg, #000000 0%, #1a1a1a 50%, #000000 100%);
            border-bottom: 3px solid #d4af37;
            color: #d4af37;
            padding: 1.25rem 2rem;
            margin: -1rem -1rem 2rem -1rem;
            box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3);
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
            background: linear-gradient(135deg, #d4af37 0%, #f4d03f 100%);
            width: 36px;
            height: 36px;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.3rem;
            box-shadow: 0 2px 8px rgba(212, 175, 55, 0.4);
        }
        
        .logo-text {
            font-size: 1.35rem;
            font-weight: bold;
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #d4af37 0%, #f4d03f 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 0 20px rgba(212, 175, 55, 0.3);
        }
        
        .nav-links {
            display: flex;
            gap: 2rem;
            font-size: 0.9rem;
        }
        
        .nav-link {
            color: #888888;
            text-decoration: none;
            transition: all 0.3s;
        }
        
        .nav-link:hover {
            color: #d4af37;
            text-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
        }
        
        .nav-link.active {
            color: #d4af37;
            border-bottom: 2px solid #d4af37;
            padding-bottom: 1.25rem;
        }
        
        .user-profile {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        
        .user-avatar {
            background: linear-gradient(135deg, #d4af37 0%, #f4d03f 100%);
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 2px solid #d4af37;
            box-shadow: 0 2px 8px rgba(212, 175, 55, 0.4);
        }
        
        .user-info {
            text-align: right;
            font-size: 0.75rem;
            line-height: 1.2;
        }
        
        .user-name {
            font-weight: 500;
        }
        
        .user-role {
            color: #888888;
            font-family: 'Tajawal', sans-serif;
        }
        
        /* Page title bar */
        .page-title-bar {
            background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%);
            border-top: 2px solid #d4af37;
            border-bottom: 2px solid #d4af37;
            color: #d4af37;
            padding: 1.25rem 2rem;
            margin: -1rem -1rem 2rem -1rem;
            text-align: center;
            box-shadow: 0 4px 12px rgba(212, 175, 55, 0.2);
        }
        
        .page-title {
            font-size: 1.5rem;
            font-weight: 500;
            font-family: 'Inter', 'Tajawal', sans-serif;
        }
        
        /* Cards */
        .custom-card {
            background: linear-gradient(135deg, #1a1a1a 0%, #0f0f0f 100%);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 16px rgba(212, 175, 55, 0.15);
            border: 2px solid #d4af37;
            margin-bottom: 1.5rem;
            transition: all 0.3s;
        }
        
        .custom-card:hover {
            box-shadow: 0 6px 20px rgba(212, 175, 55, 0.3);
            border-color: #f4d03f;
            transform: translateY(-2px);
        }
        
        .card-header {
            border-bottom: 2px solid #d4af37;
            padding-bottom: 1rem;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
            margin: -1.5rem -1.5rem 1rem -1.5rem;
            padding: 1.25rem 1.5rem;
            border-radius: 10px 10px 0 0;
        }
        
        .card-title {
            font-size: 1.125rem;
            font-weight: bold;
            color: #d4af37;
            font-family: 'Inter', 'Tajawal', sans-serif;
            text-shadow: 0 0 10px rgba(212, 175, 55, 0.3);
        }
        
        /* Bilingual text */
        .bilingual {
            display: flex;
            align-items: baseline;
            gap: 0.5rem;
        }
        
        .separator {
            color: #d4af37;
        }
        
        .arabic-text {
            font-family: 'Tajawal', sans-serif;
        }
        
        /* Badges */
        .badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 500;
        }
        
        .badge-warning {
            background: linear-gradient(135deg, #d4af37 0%, #f4d03f 100%);
            color: #000000;
            border: 2px solid #d4af37;
            font-weight: 700;
            box-shadow: 0 2px 8px rgba(212, 175, 55, 0.3);
        }
        
        .badge-success {
            background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%);
            color: #d4af37;
            border: 2px solid #d4af37;
            font-weight: 700;
            box-shadow: 0 2px 8px rgba(212, 175, 55, 0.3);
        }
        
        .badge-info {
            background: linear-gradient(135deg, #d4af37 0%, #c9a02d 100%);
            color: #000000;
            border: 2px solid #d4af37;
            font-weight: 700;
            box-shadow: 0 2px 8px rgba(212, 175, 55, 0.3);
        }
        
        .badge-danger {
            background: linear-gradient(135deg, #8b7355 0%, #6b5644 100%);
            color: #d4af37;
            border: 2px solid #d4af37;
            font-weight: 700;
            box-shadow: 0 2px 8px rgba(212, 175, 55, 0.3);
        }
        
        /* Form inputs */
        .stTextInput input, .stNumberInput input, .stSelectbox select, .stTextArea textarea {
            background-color: #1a1a1a !important;
            color: #d4af37 !important;
            border: 2px solid #d4af37 !important;
            border-radius: 8px !important;
        }
        
        .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox select:focus, .stTextArea textarea:focus {
            border-color: #f4d03f !important;
            box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.3) !important;
            background-color: #0f0f0f !important;
        }
        
        /* Buttons */
        .stButton button {
            border-radius: 8px;
            font-weight: 700;
            padding: 0.75rem 2rem;
            transition: all 0.3s;
            box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3);
            border: 2px solid #d4af37;
        }
        
        .stButton button[kind="primary"] {
            background: linear-gradient(135deg, #d4af37 0%, #f4d03f 100%);
            color: #000000;
            border: 2px solid #d4af37;
        }
        
        .stButton button[kind="primary"]:hover {
            background: linear-gradient(135deg, #f4d03f 0%, #d4af37 100%);
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(212, 175, 55, 0.5);
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
        }
        
        .progress-bar {
            width: 100%;
            height: 10px;
            background-color: #1a1a1a;
            border: 1px solid #d4af37;
            border-radius: 9999px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #d4af37 0%, #f4d03f 100%);
            border-radius: 9999px;
            transition: width 0.3s;
            box-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
        }
        
        /* Data display */
        .data-row {
            padding: 0.75rem 0;
            border-bottom: 1px solid #f3f4f6;
        }
        
        .data-row:last-child {
            border-bottom: none;
        }
        
        .data-label {
            font-weight: 600;
            color: #d4af37;
            font-size: 0.875rem;
            margin-bottom: 0.25rem;
        }
        
        .data-value {
            color: #ffffff;
            font-size: 0.875rem;
        }
        
        /* Upload area */
        .upload-area {
            border: 3px dashed #d4af37;
            border-radius: 12px;
            background: linear-gradient(135deg, rgba(212, 175, 55, 0.05) 0%, rgba(26, 26, 26, 0.8) 100%);
            padding: 2.5rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .upload-area:hover {
            background: linear-gradient(135deg, rgba(212, 175, 55, 0.15) 0%, rgba(26, 26, 26, 0.9) 100%);
            border-color: #f4d03f;
            box-shadow: 0 4px 16px rgba(212, 175, 55, 0.3);
        }
        
        .upload-icon {
            background: linear-gradient(135deg, #d4af37 0%, #f4d03f 100%);
            color: #000000;
            width: 64px;
            height: 64px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            margin-bottom: 1rem;
            box-shadow: 0 6px 20px rgba(212, 175, 55, 0.5);
            border: 3px solid #d4af37;
        }
        
        /* Footer */
        .custom-footer {
            text-align: center;
            padding: 2rem;
            color: #888888;
            font-size: 0.75rem;
            margin-top: 3rem;
            border-top: 2px solid #d4af37;
        }
        
        /* Table styles */
        .dataframe {
            font-size: 0.875rem !important;
            background-color: #1a1a1a !important;
        }
        
        .dataframe th {
            background: linear-gradient(135deg, #d4af37 0%, #c9a02d 100%) !important;
            font-weight: 700 !important;
            color: #000000 !important;
            border: 1px solid #d4af37 !important;
        }
        
        .dataframe td {
            color: #d4af37 !important;
            background-color: #0f0f0f !important;
            border: 1px solid #333333 !important;
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
    """Display custom header matching mockup"""
    user = get_current_user()
    role_en, role_ar = get_role_name(user['role'])
    
    st.markdown(f"""
        <div class="custom-header">
            <div class="header-content">
                <div class="logo-section">
                    <div class="logo-icon">🏗️</div>
                    <div class="logo-text">CE-LIMS</div>
                </div>
                <div class="user-profile">
                    <div class="user-avatar">👤</div>
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
                {title_en} <span class="separator">/</span> <span class="arabic-text">{title_ar}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

def show_footer():
    """Display footer"""
    st.markdown("""
        <div class="custom-footer">
            <div>
                © 2024 CE-LIMS. All rights reserved. <span class="separator">/</span> 
                <span class="arabic-text">٢٠٢٤. جميع الحقوق محفوظة.</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

def bilingual_text(text_en, text_ar, separator="/"):
    """Display bilingual text"""
    return f'{text_en} <span class="separator">{separator}</span> <span class="arabic-text">{text_ar}</span>'

def show_badge(text_en, text_ar, badge_type="info"):
    """Display badge"""
    return f'<span class="badge badge-{badge_type}">{text_en} <span class="separator">/</span> <span class="arabic-text">{text_ar}</span></span>'

def show_progress_bar(label_en, label_ar, percentage):
    """Display progress bar"""
    st.markdown(f"""
        <div class="progress-container">
            <div class="progress-label">
                <span>{label_en} / <span class="arabic-text">{label_ar}</span></span>
                <span>{percentage}%</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {percentage}%"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def show_data_row(label_en, label_ar, value):
    """Display data row"""
    st.markdown(f"""
        <div class="data-row">
            <div class="data-label">{label_en} <span class="separator">/</span> <span class="arabic-text">{label_ar}</span></div>
            <div class="data-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)

def get_status_badge(status):
    """Get status badge HTML"""
    status_map = {
        'registered': ('Registered', 'مسجل', 'info'),
        'assigned': ('Assigned', 'معين', 'info'),
        'in_progress': ('In Progress', 'جاري العمل', 'warning'),
        'completed': ('Completed', 'مكتمل', 'success'),
        'approved': ('Approved', 'معتمد', 'success'),
        'rejected': ('Rejected', 'مرفوض', 'danger'),
        'archived': ('Archived', 'مؤرشف', 'info'),
    }
    
    if status in status_map:
        text_en, text_ar, badge_type = status_map[status]
        return show_badge(text_en, text_ar, badge_type)
    return status

def get_priority_badge(priority):
    """Get priority badge HTML"""
    priority_map = {
        'low': ('Low', 'منخفض', 'info'),
        'normal': ('Normal', 'عادي', 'info'),
        'high': ('High', 'عالي', 'warning'),
        'urgent': ('Urgent', 'عاجل', 'danger'),
    }
    
    if priority in priority_map:
        text_en, text_ar, badge_type = priority_map[priority]
        return show_badge(text_en, text_ar, badge_type)
    return priority
