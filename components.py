"""
CE-LIMS Shared Components
Reusable UI components matching the design mockup EXACTLY
"""

import streamlit as st
from auth import get_current_user, logout, get_role_name

def load_custom_css():
    """Load custom CSS matching the mockup design EXACTLY"""
    st.markdown("""
        <style>
        /* Import fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Tajawal:wght@400;500;700&display=swap');
        
        /* Global styles - EXACT colors from mockup */
        .stApp {
            background-color: #f0f2f5;
        }
        
        /* Hide Streamlit default elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Custom header - EXACT #151f32 */
        .custom-header {
            background-color: #151f32;
            color: white;
            padding: 1rem 2rem;
            margin: -1rem -1rem 2rem -1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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
            background: white;
            width: 32px;
            height: 32px;
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
        }
        
        .logo-text {
            font-size: 1.25rem;
            font-weight: bold;
            font-family: 'Inter', sans-serif;
            color: white;
        }
        
        .nav-links {
            display: flex;
            gap: 2rem;
            font-size: 0.9rem;
        }
        
        .nav-link {
            color: #9ca3af;
            text-decoration: none;
            transition: color 0.2s;
        }
        
        .nav-link:hover {
            color: white;
        }
        
        .nav-link.active {
            color: #60a5fa;
            border-bottom: 2px solid #60a5fa;
            padding-bottom: 1.25rem;
        }
        
        .user-profile {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        
        .user-avatar {
            background: #4b5563;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
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
            color: #9ca3af;
            font-family: 'Tajawal', sans-serif;
        }
        
        /* Page title bar - EXACT #354a65 */
        .page-title-bar {
            background-color: #354a65;
            color: white;
            padding: 1rem 2rem;
            margin: -1rem -1rem 2rem -1rem;
            text-align: center;
        }
        
        .page-title {
            font-size: 1.5rem;
            font-weight: 500;
            font-family: 'Inter', 'Tajawal', sans-serif;
        }
        
        /* Cards - White background */
        .custom-card {
            background: white;
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            border: 1px solid #e5e7eb;
            margin-bottom: 1.5rem;
        }
        
        .card-header {
            border-bottom: 1px solid #f3f4f6;
            padding-bottom: 1rem;
            margin-bottom: 1rem;
            background-color: #f8fafc;
            margin: -1.5rem -1.5rem 1rem -1.5rem;
            padding: 1.25rem 1.5rem;
        }
        
        .card-title {
            font-size: 1.125rem;
            font-weight: bold;
            color: #1f2937;
            font-family: 'Inter', 'Tajawal', sans-serif;
        }
        
        /* Bilingual text */
        .bilingual {
            display: flex;
            align-items: baseline;
            gap: 0.5rem;
        }
        
        .separator {
            color: #9ca3af;
        }
        
        .arabic-text {
            font-family: 'Tajawal', sans-serif;
        }
        
        /* Badges - Yellow from mockup */
        .badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 500;
        }
        
        .badge-warning {
            background-color: #fff3cd;
            color: #856404;
            border: 1px solid #fde68a;
        }
        
        .badge-success {
            background-color: #d1fae5;
            color: #065f46;
            border: 1px solid #a7f3d0;
        }
        
        .badge-info {
            background-color: #dbeafe;
            color: #1e40af;
            border: 1px solid #bfdbfe;
        }
        
        .badge-danger {
            background-color: #fee2e2;
            color: #991b1b;
            border: 1px solid #fecaca;
        }
        
        /* Form inputs */
        .stTextInput input, .stNumberInput input, .stSelectbox select, .stTextArea textarea {
            border-color: #d1d5db !important;
            border-radius: 6px !important;
            background-color: white !important;
            color: #374151 !important;
        }
        
        .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox select:focus, .stTextArea textarea:focus {
            border-color: #0e6ede !important;
            box-shadow: 0 0 0 1px #0e6ede !important;
        }
        
        /* Buttons - Brand blue #0e6ede */
        .stButton button {
            border-radius: 6px;
            font-weight: 500;
            padding: 0.5rem 1.5rem;
            transition: all 0.2s;
        }
        
        .stButton button[kind="primary"] {
            background-color: #0e6ede;
            color: white;
            border: none;
        }
        
        .stButton button[kind="primary"]:hover {
            background-color: #0c5bc4;
        }
        
        /* Progress bar - Dark blue #314a6b */
        .progress-container {
            margin-top: 1rem;
        }
        
        .progress-label {
            display: flex;
            justify-content: space-between;
            font-size: 0.75rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: #374151;
        }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background-color: #e5e7eb;
            border-radius: 9999px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background-color: #314a6b;
            border-radius: 9999px;
            transition: width 0.3s;
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
            color: #374151;
            font-size: 0.875rem;
            margin-bottom: 0.25rem;
        }
        
        .data-value {
            color: #111827;
            font-size: 0.875rem;
        }
        
        /* Upload area - Blue dashed border */
        .upload-area {
            border: 2px dashed #93c5fd;
            border-radius: 8px;
            background-color: rgba(59, 130, 246, 0.05);
            padding: 2rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .upload-area:hover {
            background-color: rgba(59, 130, 246, 0.1);
        }
        
        .upload-icon {
            background-color: #0e6ede;
            color: white;
            width: 48px;
            height: 48px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }
        
        /* Footer */
        .custom-footer {
            text-align: center;
            padding: 2rem;
            color: #6b7280;
            font-size: 0.75rem;
            margin-top: 3rem;
        }
        
        /* Table styles */
        .dataframe {
            font-size: 0.875rem !important;
        }
        
        .dataframe th {
            background-color: #f9fafb !important;
            font-weight: 600 !important;
            color: #374151 !important;
        }
        
        .dataframe td {
            color: #111827 !important;
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
