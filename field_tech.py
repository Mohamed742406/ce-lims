"""
CE-LIMS Field Technician Module
Mobile-friendly interface for sample registration
"""

import streamlit as st
from database import get_connection, log_audit, add_chain_of_custody
from auth import get_current_user
from components import *
from datetime import datetime, date
import json

def show_field_tech_dashboard():
    """Display Field Tech dashboard"""
    load_custom_css()
    show_header("samples")
    show_page_title("Sample Registration", "تسجيل العينات")
    
    user = get_current_user()
    
    # Main container
    st.markdown('<div style="max-width: 800px; margin: 0 auto;">', unsafe_allow_html=True)
    
    # Tabs for different views
    tab1, tab2 = st.tabs([
        "➕ Register New Sample / تسجيل عينة جديدة",
        "📋 My Samples / عيناتي"
    ])
    
    with tab1:
        show_sample_registration_form(user)
    
    with tab2:
        show_my_samples(user)
    
    st.markdown('</div>', unsafe_allow_html=True)
    show_footer()

def show_sample_registration_form(user):
    """Show sample registration form"""
    st.markdown("### 📝 New Sample Registration / تسجيل عينة جديدة")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get projects
    cursor.execute("SELECT id, project_code, project_name, project_name_ar FROM projects WHERE status = 'active' AND is_deleted = 0")
    projects = cursor.fetchall()
    
    with st.form("sample_registration_form"):
        st.markdown("#### 🏗️ Project Information / معلومات المشروع")
        
        col1, col2 = st.columns(2)
        
        with col1:
            project_options = {f"{p['project_code']} - {p['project_name']}": p['id'] for p in projects}
            selected_project = st.selectbox(
                "Project / المشروع *",
                options=list(project_options.keys()),
                key="project_select"
            )
            project_id = project_options[selected_project] if selected_project else None
        
        with col2:
            # Auto-generate sample ID
            today = date.today()
            cursor.execute("SELECT COUNT(*) as count FROM samples WHERE DATE(created_at) = ?", (today,))
            count = cursor.fetchone()['count'] + 1
            sample_id = f"S-{today.strftime('%Y-%m-%d')}-{count:03d}"
            st.text_input("Sample ID / معرف العينة", value=sample_id, disabled=True, key="sample_id")
        
        st.markdown("#### 🧪 Sample Details / تفاصيل العينة")
        
        col1, col2 = st.columns(2)
        
        with col1:
            material_type = st.selectbox(
                "Material Type / نوع المادة *",
                options=["Concrete / خرسانة", "Asphalt Binder / رابط أسفلتي", "Soil / تربة", "Aggregate / ركام", "Steel / حديد", "Other / أخرى"],
                key="material_type"
            )
            
            material_type_en = material_type.split(" / ")[0]
            material_type_ar = material_type.split(" / ")[1]
        
        with col2:
            sample_location = st.text_input(
                "Sample Location / موقع العينة",
                placeholder="e.g., Station 5+200 / مثال: محطة 5+200",
                key="sample_location"
            )
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            quantity = st.number_input(
                "Quantity / الكمية",
                min_value=0.0,
                step=0.1,
                key="quantity"
            )
        
        with col2:
            quantity_unit = st.selectbox(
                "Unit / الوحدة",
                options=["kg", "L", "m³", "pieces / قطع"],
                key="quantity_unit"
            )
        
        with col3:
            temperature = st.number_input(
                "Temperature (°C) / درجة الحرارة",
                min_value=-50.0,
                max_value=100.0,
                value=25.0,
                step=0.1,
                key="temperature"
            )
        
        st.markdown("#### 📅 Collection Information / معلومات الجمع")
        
        col1, col2 = st.columns(2)
        
        with col1:
            collection_date = st.date_input(
                "Collection Date / تاريخ الجمع *",
                value=date.today(),
                key="collection_date"
            )
        
        with col2:
            collection_time = st.time_input(
                "Collection Time / وقت الجمع *",
                value=datetime.now().time(),
                key="collection_time"
            )
        
        st.markdown("#### 🔍 Condition & Priority / الحالة والأولوية")
        
        col1, col2 = st.columns(2)
        
        with col1:
            condition = st.selectbox(
                "Sample Condition / حالة العينة *",
                options=["Good / جيدة", "Fair / مقبولة", "Poor / سيئة", "Damaged / تالفة"],
                key="condition"
            )
            
            condition_en = condition.split(" / ")[0]
            condition_ar = condition.split(" / ")[1]
        
        with col2:
            priority = st.selectbox(
                "Priority / الأولوية *",
                options=["Low / منخفض", "Normal / عادي", "High / عالي", "Urgent / عاجل"],
                index=1,
                key="priority"
            )
            
            priority_en = priority.split(" / ")[0].lower()
            priority_ar = priority.split(" / ")[1]
        
        st.markdown("#### 📝 Notes / ملاحظات")
        
        notes = st.text_area(
            "Additional Notes / ملاحظات إضافية",
            placeholder="Enter any special handling instructions or observations...\nأدخل أي تعليمات خاصة بالتعامل أو ملاحظات...",
            height=100,
            key="notes"
        )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button(
                "✅ Register Sample / تسجيل العينة",
                use_container_width=True,
                type="primary"
            )
        
        if submitted:
            if project_id and material_type and condition and priority:
                try:
                    # Insert sample
                    cursor.execute("""
                        INSERT INTO samples (
                            sample_id, project_id, material_type, material_type_ar,
                            sample_location, sample_location_ar, quantity, quantity_unit,
                            collection_date, collection_time, received_date, received_time,
                            received_by, temperature, condition, condition_ar,
                            priority, priority_ar, notes, status, created_by
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        sample_id, project_id, material_type_en, material_type_ar,
                        sample_location, sample_location, quantity, quantity_unit,
                        collection_date, collection_time, date.today(), datetime.now().time(),
                        user['id'], temperature, condition_en, condition_ar,
                        priority_en, priority_ar, notes, 'registered', user['id']
                    ))
                    
                    sample_db_id = cursor.lastrowid
                    
                    # Add chain of custody
                    add_chain_of_custody(
                        sample_db_id, None, user['id'],
                        sample_location, "Sample Collection",
                        condition_en, f"Collected by {user['full_name']}"
                    )
                    
                    # Log audit
                    log_audit(
                        'samples', sample_db_id, 'INSERT',
                        None, json.dumps({'sample_id': sample_id, 'status': 'registered'}),
                        user['id']
                    )
                    
                    conn.commit()
                    st.success(f"✅ Sample {sample_id} registered successfully! / تم تسجيل العينة {sample_id} بنجاح!")
                    st.balloons()
                    
                except Exception as e:
                    conn.rollback()
                    st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("⚠️ Please fill all required fields / الرجاء ملء جميع الحقول المطلوبة")
    
    conn.close()

def show_my_samples(user):
    """Show samples registered by current user"""
    st.markdown("### 📋 My Registered Samples / العينات المسجلة")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get samples created by current user
    cursor.execute("""
        SELECT 
            s.sample_id,
            s.material_type,
            s.material_type_ar,
            p.project_name,
            p.project_name_ar,
            s.collection_date,
            s.priority,
            s.priority_ar,
            s.status,
            s.created_at
        FROM samples s
        JOIN projects p ON s.project_id = p.id
        WHERE s.created_by = ? AND s.is_deleted = 0
        ORDER BY s.created_at DESC
        LIMIT 20
    """, (user['id'],))
    
    samples = cursor.fetchall()
    
    if samples:
        st.markdown(f"**Total Samples: {len(samples)} / إجمالي العينات: {len(samples)}**")
        
        for sample in samples:
            with st.expander(f"🧪 {sample['sample_id']} - {sample['material_type']} / {sample['material_type_ar']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Project / المشروع:**  \n{sample['project_name']}")
                    st.markdown(f"**Material / المادة:**  \n{sample['material_type']} / {sample['material_type_ar']}")
                    st.markdown(f"**Collection Date / تاريخ الجمع:**  \n{sample['collection_date']}")
                
                with col2:
                    st.markdown(f"**Priority / الأولوية:**  \n{sample['priority'].title()} / {sample['priority_ar']}")
                    st.markdown(f"**Status / الحالة:**  \n{sample['status'].replace('_', ' ').title()}")
                    st.markdown(f"**Registered / مسجل:**  \n{sample['created_at'][:16]}")
    else:
        st.info("ℹ️ No samples registered yet / لا توجد عينات مسجلة بعد")
    
    conn.close()
