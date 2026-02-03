"""
CE-LIMS Supervisor Module
Interface for assigning tests and managing workflow
"""

import streamlit as st
from database import get_connection, log_audit
from auth import get_current_user
from components import *
from datetime import datetime, date, timedelta
import json

def show_supervisor_dashboard():
    """Display Supervisor dashboard"""
    load_custom_css()
    show_header("tests")
    show_page_title("Test Assignment & Management", "تعيين وإدارة الاختبارات")
    
    user = get_current_user()
    
    # Tabs
    tab1, tab2, tab3 = st.tabs([
        "📋 Pending Samples / العينات المعلقة",
        "✅ Assigned Tests / الاختبارات المعينة",
        "📊 Overview / نظرة عامة"
    ])
    
    with tab1:
        show_pending_samples(user)
    
    with tab2:
        show_assigned_tests(user)
    
    with tab3:
        show_overview(user)
    
    show_footer()

def show_pending_samples(user):
    """Show samples pending test assignment"""
    st.markdown("### 📋 Samples Awaiting Test Assignment / العينات في انتظار تعيين الاختبارات")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get samples that are registered but not yet assigned
    cursor.execute("""
        SELECT 
            s.id,
            s.sample_id,
            s.material_type,
            s.material_type_ar,
            p.project_name,
            p.project_name_ar,
            s.collection_date,
            s.priority,
            s.priority_ar,
            s.status,
            s.notes,
            u.full_name as collected_by
        FROM samples s
        JOIN projects p ON s.project_id = p.id
        LEFT JOIN users u ON s.created_by = u.id
        WHERE s.status IN ('registered', 'assigned') AND s.is_deleted = 0
        ORDER BY 
            CASE s.priority
                WHEN 'urgent' THEN 1
                WHEN 'high' THEN 2
                WHEN 'normal' THEN 3
                WHEN 'low' THEN 4
            END,
            s.collection_date DESC
    """)
    
    samples = cursor.fetchall()
    
    if samples:
        st.markdown(f"**Total Pending: {len(samples)} / إجمالي المعلقة: {len(samples)}**")
        
        for sample in samples:
            with st.expander(
                f"🧪 {sample['sample_id']} - {sample['material_type']} | Priority: {sample['priority'].title()} / الأولوية: {sample['priority_ar']}"
            ):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    show_data_row("Sample ID", "معرف العينة", sample['sample_id'])
                    show_data_row("Project", "المشروع", f"{sample['project_name']} / {sample['project_name_ar']}")
                    show_data_row("Material", "المادة", f"{sample['material_type']} / {sample['material_type_ar']}")
                    show_data_row("Collection Date", "تاريخ الجمع", sample['collection_date'])
                    show_data_row("Collected By", "جمعت بواسطة", sample['collected_by'])
                    
                    if sample['notes']:
                        st.markdown(f"**Notes / ملاحظات:** {sample['notes']}")
                
                with col2:
                    st.markdown(get_priority_badge(sample['priority']), unsafe_allow_html=True)
                    st.markdown(get_status_badge(sample['status']), unsafe_allow_html=True)
                
                st.markdown("---")
                st.markdown("#### 🔬 Assign Tests / تعيين الاختبارات")
                
                # Get available test methods for this material type
                cursor.execute("""
                    SELECT id, test_code, test_name, test_name_ar, standard, typical_duration
                    FROM test_methods
                    WHERE material_type = ? AND is_active = 1
                """, (sample['material_type'],))
                
                test_methods = cursor.fetchall()
                
                if test_methods:
                    with st.form(f"assign_form_{sample['id']}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # Multi-select for tests
                            test_options = {
                                f"{tm['test_code']} - {tm['test_name']} / {tm['test_name_ar']}": tm['id']
                                for tm in test_methods
                            }
                            
                            selected_tests = st.multiselect(
                                "Select Tests / اختر الاختبارات *",
                                options=list(test_options.keys()),
                                key=f"tests_{sample['id']}"
                            )
                        
                        with col2:
                            # Get lab technicians
                            cursor.execute("""
                                SELECT id, full_name, full_name_ar
                                FROM users
                                WHERE role = 'lab_tech' AND is_active = 1
                            """)
                            lab_techs = cursor.fetchall()
                            
                            tech_options = {
                                f"{lt['full_name']} / {lt['full_name_ar']}": lt['id']
                                for lt in lab_techs
                            }
                            
                            assigned_tech = st.selectbox(
                                "Assign To / تعيين إلى *",
                                options=list(tech_options.keys()),
                                key=f"tech_{sample['id']}"
                            )
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            due_date = st.date_input(
                                "Due Date / تاريخ الاستحقاق *",
                                value=date.today() + timedelta(days=7),
                                key=f"due_{sample['id']}"
                            )
                        
                        with col2:
                            assignment_priority = st.selectbox(
                                "Test Priority / أولوية الاختبار",
                                options=["Low / منخفض", "Normal / عادي", "High / عالي", "Urgent / عاجل"],
                                index=1,
                                key=f"priority_{sample['id']}"
                            )
                        
                        assignment_notes = st.text_area(
                            "Assignment Notes / ملاحظات التعيين",
                            key=f"notes_{sample['id']}"
                        )
                        
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            assign_btn = st.form_submit_button(
                                "✅ Assign Tests / تعيين الاختبارات",
                                use_container_width=True,
                                type="primary"
                            )
                        
                        if assign_btn:
                            if selected_tests and assigned_tech:
                                try:
                                    tech_id = tech_options[assigned_tech]
                                    priority_value = assignment_priority.split(" / ")[0].lower()
                                    
                                    # Assign each selected test
                                    for test_key in selected_tests:
                                        test_id = test_options[test_key]
                                        
                                        cursor.execute("""
                                            INSERT INTO test_assignments (
                                                sample_id, test_method_id, assigned_to,
                                                assigned_by, due_date, priority, notes, status
                                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                                        """, (
                                            sample['id'], test_id, tech_id,
                                            user['id'], due_date, priority_value,
                                            assignment_notes, 'assigned'
                                        ))
                                        
                                        assignment_id = cursor.lastrowid
                                        
                                        # Log audit
                                        log_audit(
                                            'test_assignments', assignment_id, 'INSERT',
                                            None, json.dumps({
                                                'sample_id': sample['sample_id'],
                                                'test_id': test_id,
                                                'assigned_to': tech_id
                                            }),
                                            user['id']
                                        )
                                    
                                    # Update sample status
                                    cursor.execute("""
                                        UPDATE samples
                                        SET status = 'assigned', updated_at = CURRENT_TIMESTAMP, updated_by = ?
                                        WHERE id = ?
                                    """, (user['id'], sample['id']))
                                    
                                    conn.commit()
                                    st.success(f"✅ Tests assigned successfully for {sample['sample_id']}! / تم تعيين الاختبارات بنجاح!")
                                    st.rerun()
                                    
                                except Exception as e:
                                    conn.rollback()
                                    st.error(f"❌ Error: {str(e)}")
                            else:
                                st.warning("⚠️ Please select tests and technician / الرجاء اختيار الاختبارات والفني")
                else:
                    st.info(f"ℹ️ No test methods available for {sample['material_type']} / لا توجد طرق اختبار متاحة")
    else:
        st.info("ℹ️ No pending samples / لا توجد عينات معلقة")
    
    conn.close()

def show_assigned_tests(user):
    """Show all assigned tests"""
    st.markdown("### ✅ Assigned Tests / الاختبارات المعينة")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get all test assignments
    cursor.execute("""
        SELECT 
            ta.id,
            s.sample_id,
            s.material_type,
            tm.test_name,
            tm.test_name_ar,
            tm.standard,
            u.full_name as assigned_to_name,
            u.full_name_ar as assigned_to_name_ar,
            ta.assigned_date,
            ta.due_date,
            ta.priority,
            ta.status
        FROM test_assignments ta
        JOIN samples s ON ta.sample_id = s.id
        JOIN test_methods tm ON ta.test_method_id = tm.id
        JOIN users u ON ta.assigned_to = u.id
        WHERE ta.assigned_by = ? AND ta.is_deleted = 0
        ORDER BY ta.assigned_date DESC
        LIMIT 50
    """, (user['id'],))
    
    assignments = cursor.fetchall()
    
    if assignments:
        # Filter by status
        status_filter = st.selectbox(
            "Filter by Status / تصفية حسب الحالة",
            options=["All / الكل", "Assigned / معين", "In Progress / جاري العمل", "Completed / مكتمل", "Approved / معتمد"]
        )
        
        filtered_assignments = assignments
        if status_filter != "All / الكل":
            status_value = status_filter.split(" / ")[0].lower().replace(" ", "_")
            filtered_assignments = [a for a in assignments if a['status'] == status_value]
        
        st.markdown(f"**Total: {len(filtered_assignments)} / الإجمالي: {len(filtered_assignments)}**")
        
        # Display as table
        if filtered_assignments:
            for assignment in filtered_assignments:
                col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                
                with col1:
                    st.markdown(f"**{assignment['sample_id']}**")
                    st.caption(assignment['material_type'])
                
                with col2:
                    st.markdown(f"**{assignment['test_name']}**")
                    st.caption(f"{assignment['standard']}")
                
                with col3:
                    st.markdown(f"**{assignment['assigned_to_name']}**")
                    st.caption(f"Due: {assignment['due_date']}")
                
                with col4:
                    st.markdown(get_status_badge(assignment['status']), unsafe_allow_html=True)
                
                st.markdown("---")
        else:
            st.info("ℹ️ No assignments match the filter / لا توجد تعيينات تطابق الفلتر")
    else:
        st.info("ℹ️ No test assignments yet / لا توجد تعيينات اختبارات بعد")
    
    conn.close()

def show_overview(user):
    """Show supervisor overview dashboard"""
    st.markdown("### 📊 Supervisor Overview / نظرة عامة للمشرف")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        cursor.execute("SELECT COUNT(*) as count FROM samples WHERE status = 'registered' AND is_deleted = 0")
        pending_samples = cursor.fetchone()['count']
        st.metric("Pending Samples / العينات المعلقة", pending_samples)
    
    with col2:
        cursor.execute("SELECT COUNT(*) as count FROM test_assignments WHERE assigned_by = ? AND status = 'assigned'", (user['id'],))
        assigned_tests = cursor.fetchone()['count']
        st.metric("Assigned Tests / الاختبارات المعينة", assigned_tests)
    
    with col3:
        cursor.execute("SELECT COUNT(*) as count FROM test_assignments WHERE assigned_by = ? AND status = 'in_progress'", (user['id'],))
        in_progress = cursor.fetchone()['count']
        st.metric("In Progress / جاري العمل", in_progress)
    
    with col4:
        cursor.execute("SELECT COUNT(*) as count FROM test_assignments WHERE assigned_by = ? AND status = 'completed'", (user['id'],))
        completed = cursor.fetchone()['count']
        st.metric("Completed / مكتمل", completed)
    
    st.markdown("---")
    
    # Recent activity
    st.markdown("#### 📅 Recent Activity / النشاط الأخير")
    
    cursor.execute("""
        SELECT 
            s.sample_id,
            tm.test_name,
            u.full_name,
            ta.assigned_date,
            ta.status
        FROM test_assignments ta
        JOIN samples s ON ta.sample_id = s.id
        JOIN test_methods tm ON ta.test_method_id = tm.id
        JOIN users u ON ta.assigned_to = u.id
        WHERE ta.assigned_by = ?
        ORDER BY ta.assigned_date DESC
        LIMIT 10
    """, (user['id'],))
    
    recent = cursor.fetchall()
    
    if recent:
        for item in recent:
            st.markdown(f"""
                - **{item['sample_id']}** - {item['test_name']} → {item['full_name']} 
                  ({item['assigned_date'][:16]}) - {get_status_badge(item['status'])}
            """, unsafe_allow_html=True)
    else:
        st.info("ℹ️ No recent activity / لا يوجد نشاط حديث")
    
    conn.close()
