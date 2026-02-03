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
            background-color: #f8fafc;
        }
        
        /* Hide Streamlit default elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Custom header */
        .custom-header {
            background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
            color: white;
            padding: 1.25rem 2rem;
            margin: -1rem -1rem 2rem -1rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
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
        }
        
        .user-role {
            color: #9ca3af;
            font-family: 'Tajawal', sans-serif;
        }
        
        /* Page title bar */
        .page-title-bar {
            background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
            color: white;
            padding: 1.25rem 2rem;
            margin: -1rem -1rem 2rem -1rem;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        }
        
        .page-title {
            font-size: 1.5rem;
            font-weight: 500;
            font-family: 'Inter', 'Tajawal', sans-serif;
        }
        
        /* Cards */
        .custom-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            border: 1px solid #e2e8f0;
            margin-bottom: 1.5rem;
            transition: box-shadow 0.2s;
        }
        
        .custom-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .card-header {
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 1rem;
            margin-bottom: 1rem;
            background: linear-gradient(to bottom, #f8fafc 0%, #ffffff 100%);
            margin: -1.5rem -1.5rem 1rem -1.5rem;
            padding: 1.25rem 1.5rem;
            border-radius: 12px 12px 0 0;
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
        
        /* Badges */
        .badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 500;
        }
        
        .badge-warning {
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            color: #92400e;
            border: 1px solid #fbbf24;
            font-weight: 600;
        }
        
        .badge-success {
            background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
            color: #065f46;
            border: 1px solid #34d399;
            font-weight: 600;
        }
        
        .badge-info {
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
            color: #1e40af;
            border: 1px solid #60a5fa;
            font-weight: 600;
        }
        
        .badge-danger {
            background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
            color: #991b1b;
            border: 1px solid #f87171;
            font-weight: 600;
        }
        
        /* Form inputs */
        .stTextInput input, .stNumberInput input, .stSelectbox select, .stTextArea textarea {
            border-color: #d1d5db !important;
            border-radius: 6px !important;
        }
        
        .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox select:focus, .stTextArea textarea:focus {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 1px #3b82f6 !important;
        }
        
        /* Buttons */
        .stButton button {
            border-radius: 8px;
            font-weight: 600;
            padding: 0.625rem 1.75rem;
            transition: all 0.3s;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        }
        
        .stButton button[kind="primary"] {
            background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
            border: none;
        }
        
        .stButton button[kind="primary"]:hover {
            background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%);
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(37, 99, 235, 0.3);
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
            height: 8px;
            background-color: #e5e7eb;
            border-radius: 9999px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
            border-radius: 9999px;
            transition: width 0.3s;
            box-shadow: 0 2px 4px rgba(37, 99, 235, 0.3);
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
        
        /* Upload area */
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
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            color: white;
            width: 56px;
            height: 56px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 1.75rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
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
