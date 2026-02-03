"""
CE-LIMS Manager Module
Interface for approval, archiving, and reporting
"""

import streamlit as st
from database import get_connection, log_audit
from auth import get_current_user
from components import *
from datetime import datetime, date
import json
import pandas as pd

def show_manager_dashboard():
    """Display Manager dashboard"""
    load_custom_css()
    show_header("reports")
    show_page_title("Manager Dashboard", "لوحة تحكم المدير")
    
    user = get_current_user()
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "✅ Pending Approval / في انتظار الاعتماد",
        "📊 Reports / التقارير",
        "🗄️ Archive / الأرشيف",
        "📈 Analytics / التحليلات"
    ])
    
    with tab1:
        show_pending_approvals(user)
    
    with tab2:
        show_reports(user)
    
    with tab3:
        show_archive(user)
    
    with tab4:
        show_analytics(user)
    
    show_footer()

def show_pending_approvals(user):
    """Show test results pending approval"""
    st.markdown("### ✅ Test Results Pending Approval / نتائج الاختبارات في انتظار الاعتماد")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get completed test results awaiting approval
    cursor.execute("""
        SELECT 
            tr.id as result_id,
            s.sample_id,
            s.material_type,
            p.project_name,
            tm.test_name,
            tm.test_name_ar,
            tm.standard,
            tr.result_value,
            tr.result_unit,
            tr.test_completed_at,
            u.full_name as tested_by_name,
            tr.observations,
            tr.status,
            ta.id as assignment_id
        FROM test_results tr
        JOIN test_assignments ta ON tr.assignment_id = ta.id
        JOIN samples s ON ta.sample_id = s.id
        JOIN projects p ON s.project_id = p.id
        JOIN test_methods tm ON ta.test_method_id = tm.id
        JOIN users u ON tr.tested_by = u.id
        WHERE tr.status = 'submitted' AND tr.is_deleted = 0
        ORDER BY tr.test_completed_at DESC
    """)
    
    pending_results = cursor.fetchall()
    
    if pending_results:
        st.markdown(f"**Total Pending: {len(pending_results)} / إجمالي المعلقة: {len(pending_results)}**")
        
        for result in pending_results:
            with st.expander(
                f"🧪 {result['sample_id']} - {result['test_name']} | Result: {result['result_value']} {result['result_unit']}"
            ):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    show_data_row("Sample ID", "معرف العينة", result['sample_id'])
                    show_data_row("Project", "المشروع", result['project_name'])
                    show_data_row("Material", "المادة", result['material_type'])
                    show_data_row("Test Method", "طريقة الاختبار", f"{result['standard']} - {result['test_name']}")
                    show_data_row("Tested By", "تم الاختبار بواسطة", result['tested_by_name'])
                    show_data_row("Completed At", "تاريخ الإكمال", result['test_completed_at'][:16])
                    
                    st.markdown("---")
                    st.markdown(f"**Result / النتيجة:** {result['result_value']} {result['result_unit']}")
                    
                    if result['observations']:
                        st.markdown(f"**Observations / الملاحظات:**")
                        st.info(result['observations'])
                    
                    # Check for uploaded files
                    cursor.execute("""
                        SELECT file_name, file_path, file_type, uploaded_at
                        FROM raw_files
                        WHERE test_result_id = ? AND is_deleted = 0
                    """, (result['result_id'],))
                    
                    files = cursor.fetchall()
                    if files:
                        st.markdown("**Attached Files / الملفات المرفقة:**")
                        for file in files:
                            st.markdown(f"- 📎 {file['file_name']} ({file['file_type']}) - {file['uploaded_at'][:16]}")
                
                with col2:
                    st.markdown(get_status_badge(result['status']), unsafe_allow_html=True)
                
                st.markdown("---")
                st.markdown("#### 📝 Approval Decision / قرار الاعتماد")
                
                with st.form(f"approval_form_{result['result_id']}"):
                    decision = st.radio(
                        "Decision / القرار",
                        options=["Approve / اعتماد", "Reject / رفض"],
                        key=f"decision_{result['result_id']}"
                    )
                    
                    approval_notes = st.text_area(
                        "Notes / ملاحظات",
                        placeholder="Enter approval notes or rejection reason...\nأدخل ملاحظات الاعتماد أو سبب الرفض...",
                        key=f"notes_{result['result_id']}"
                    )
                    
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        submit_btn = st.form_submit_button(
                            "✅ Submit Decision / إرسال القرار",
                            use_container_width=True,
                            type="primary"
                        )
                    
                    if submit_btn:
                        try:
                            if decision.startswith("Approve"):
                                # Approve result
                                cursor.execute("""
                                    UPDATE test_results
                                    SET status = 'approved',
                                        approved_by = ?,
                                        approved_at = CURRENT_TIMESTAMP,
                                        updated_at = CURRENT_TIMESTAMP,
                                        updated_by = ?
                                    WHERE id = ?
                                """, (user['id'], user['id'], result['result_id']))
                                
                                # Update assignment status
                                cursor.execute("""
                                    UPDATE test_assignments
                                    SET status = 'approved'
                                    WHERE id = ?
                                """, (result['assignment_id'],))
                                
                                # Check if all tests for this sample are approved
                                cursor.execute("""
                                    SELECT COUNT(*) as total FROM test_assignments 
                                    WHERE sample_id = (SELECT sample_id FROM test_assignments WHERE id = ?)
                                """, (result['assignment_id'],))
                                total = cursor.fetchone()['total']
                                
                                cursor.execute("""
                                    SELECT COUNT(*) as approved FROM test_assignments 
                                    WHERE sample_id = (SELECT sample_id FROM test_assignments WHERE id = ?) 
                                    AND status = 'approved'
                                """, (result['assignment_id'],))
                                approved = cursor.fetchone()['approved']
                                
                                if total == approved:
                                    # Update sample status to approved
                                    cursor.execute("""
                                        UPDATE samples
                                        SET status = 'approved'
                                        WHERE id = (SELECT sample_id FROM test_assignments WHERE id = ?)
                                    """, (result['assignment_id'],))
                                
                                log_audit(
                                    'test_results', result['result_id'], 'APPROVE',
                                    json.dumps({'status': 'submitted'}),
                                    json.dumps({'status': 'approved', 'notes': approval_notes}),
                                    user['id']
                                )
                                
                                conn.commit()
                                st.success("✅ Test result approved! / تم اعتماد نتيجة الاختبار!")
                                st.rerun()
                            else:
                                # Reject result
                                cursor.execute("""
                                    UPDATE test_results
                                    SET status = 'rejected',
                                        rejection_reason = ?,
                                        updated_at = CURRENT_TIMESTAMP,
                                        updated_by = ?
                                    WHERE id = ?
                                """, (approval_notes, user['id'], result['result_id']))
                                
                                # Update assignment status back to in_progress
                                cursor.execute("""
                                    UPDATE test_assignments
                                    SET status = 'in_progress'
                                    WHERE id = ?
                                """, (result['assignment_id'],))
                                
                                log_audit(
                                    'test_results', result['result_id'], 'REJECT',
                                    json.dumps({'status': 'submitted'}),
                                    json.dumps({'status': 'rejected', 'reason': approval_notes}),
                                    user['id']
                                )
                                
                                conn.commit()
                                st.warning("⚠️ Test result rejected. / تم رفض نتيجة الاختبار.")
                                st.rerun()
                        
                        except Exception as e:
                            conn.rollback()
                            st.error(f"❌ Error: {str(e)}")
    else:
        st.info("ℹ️ No test results pending approval / لا توجد نتائج في انتظار الاعتماد")
    
    conn.close()

def show_reports(user):
    """Show reports generation interface"""
    st.markdown("### 📊 Generate Reports / إنشاء التقارير")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Report filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Get projects
        cursor.execute("SELECT id, project_code, project_name FROM projects WHERE is_deleted = 0")
        projects = cursor.fetchall()
        project_options = ["All / الكل"] + [f"{p['project_code']} - {p['project_name']}" for p in projects]
        selected_project = st.selectbox("Project / المشروع", options=project_options)
    
    with col2:
        start_date = st.date_input("Start Date / تاريخ البداية", value=date.today().replace(day=1))
    
    with col3:
        end_date = st.date_input("End Date / تاريخ النهاية", value=date.today())
    
    if st.button("📊 Generate Report / إنشاء التقرير", type="primary"):
        # Build query
        query = """
            SELECT 
                s.sample_id,
                p.project_name,
                s.material_type,
                tm.test_name,
                tm.standard,
                tr.result_value,
                tr.result_unit,
                tr.test_completed_at,
                tr.status,
                u1.full_name as tested_by,
                u2.full_name as approved_by
            FROM test_results tr
            JOIN test_assignments ta ON tr.assignment_id = ta.id
            JOIN samples s ON ta.sample_id = s.id
            JOIN projects p ON s.project_id = p.id
            JOIN test_methods tm ON ta.test_method_id = tm.id
            JOIN users u1 ON tr.tested_by = u1.id
            LEFT JOIN users u2 ON tr.approved_by = u2.id
            WHERE DATE(tr.test_completed_at) BETWEEN ? AND ?
        """
        
        params = [start_date, end_date]
        
        if selected_project != "All / الكل":
            project_code = selected_project.split(" - ")[0]
            query += " AND p.project_code = ?"
            params.append(project_code)
        
        query += " ORDER BY tr.test_completed_at DESC"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        if results:
            # Convert to DataFrame
            df = pd.DataFrame([dict(r) for r in results])
            
            st.markdown(f"**Total Results: {len(results)} / إجمالي النتائج: {len(results)}**")
            
            # Display table
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )
            
            # Download options
            col1, col2 = st.columns(2)
            
            with col1:
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 Download CSV / تحميل CSV",
                    csv,
                    f"report_{start_date}_{end_date}.csv",
                    "text/csv",
                    use_container_width=True
                )
            
            with col2:
                # Summary statistics
                st.metric("Approved / معتمد", len(df[df['status'] == 'approved']))
        else:
            st.info("ℹ️ No results found for the selected criteria / لا توجد نتائج للمعايير المحددة")
    
    conn.close()

def show_archive(user):
    """Show archived samples and tests"""
    st.markdown("### 🗄️ Archive Management / إدارة الأرشيف")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get approved samples that can be archived
    cursor.execute("""
        SELECT 
            s.id,
            s.sample_id,
            p.project_name,
            s.material_type,
            s.status,
            COUNT(ta.id) as total_tests,
            s.collection_date
        FROM samples s
        JOIN projects p ON s.project_id = p.id
        LEFT JOIN test_assignments ta ON s.id = ta.sample_id
        WHERE s.status = 'approved' AND s.is_deleted = 0
        GROUP BY s.id
        ORDER BY s.collection_date DESC
    """)
    
    approved_samples = cursor.fetchall()
    
    if approved_samples:
        st.markdown(f"**Samples Ready for Archiving: {len(approved_samples)} / العينات الجاهزة للأرشفة: {len(approved_samples)}**")
        
        for sample in approved_samples:
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"**{sample['sample_id']}** - {sample['project_name']}")
                st.caption(f"{sample['material_type']} | {sample['total_tests']} tests | {sample['collection_date']}")
            
            with col2:
                st.markdown(get_status_badge(sample['status']), unsafe_allow_html=True)
            
            with col3:
                if st.button(f"🗄️ Archive", key=f"archive_{sample['id']}"):
                    # Archive sample (soft delete)
                    cursor.execute("""
                        UPDATE samples
                        SET status = 'archived', updated_at = CURRENT_TIMESTAMP, updated_by = ?
                        WHERE id = ?
                    """, (user['id'], sample['id']))
                    
                    log_audit(
                        'samples', sample['id'], 'UPDATE',
                        json.dumps({'status': 'approved'}),
                        json.dumps({'status': 'archived'}),
                        user['id']
                    )
                    
                    conn.commit()
                    st.success(f"✅ {sample['sample_id']} archived!")
                    st.rerun()
            
            st.markdown("---")
    else:
        st.info("ℹ️ No samples ready for archiving / لا توجد عينات جاهزة للأرشفة")
    
    # Show archived samples
    st.markdown("### 📦 Archived Samples / العينات المؤرشفة")
    
    cursor.execute("""
        SELECT 
            s.sample_id,
            p.project_name,
            s.material_type,
            s.updated_at as archived_at
        FROM samples s
        JOIN projects p ON s.project_id = p.id
        WHERE s.status = 'archived' AND s.is_deleted = 0
        ORDER BY s.updated_at DESC
        LIMIT 20
    """)
    
    archived = cursor.fetchall()
    
    if archived:
        for item in archived:
            st.markdown(f"- **{item['sample_id']}** - {item['project_name']} ({item['material_type']}) - Archived: {item['archived_at'][:16]}")
    else:
        st.info("ℹ️ No archived samples / لا توجد عينات مؤرشفة")
    
    conn.close()

def show_analytics(user):
    """Show analytics and statistics"""
    st.markdown("### 📈 Analytics & Statistics / التحليلات والإحصائيات")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Overall statistics
    st.markdown("#### 📊 Overall Statistics / الإحصائيات العامة")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        cursor.execute("SELECT COUNT(*) as count FROM samples WHERE is_deleted = 0")
        total_samples = cursor.fetchone()['count']
        st.metric("Total Samples / إجمالي العينات", total_samples)
    
    with col2:
        cursor.execute("SELECT COUNT(*) as count FROM test_assignments WHERE is_deleted = 0")
        total_tests = cursor.fetchone()['count']
        st.metric("Total Tests / إجمالي الاختبارات", total_tests)
    
    with col3:
        cursor.execute("SELECT COUNT(*) as count FROM test_results WHERE status = 'approved'")
        approved_results = cursor.fetchone()['count']
        st.metric("Approved Results / النتائج المعتمدة", approved_results)
    
    with col4:
        cursor.execute("SELECT COUNT(*) as count FROM samples WHERE status = 'archived'")
        archived_samples = cursor.fetchone()['count']
        st.metric("Archived / المؤرشف", archived_samples)
    
    st.markdown("---")
    
    # Tests by material type
    st.markdown("#### 🧪 Tests by Material Type / الاختبارات حسب نوع المادة")
    
    cursor.execute("""
        SELECT s.material_type, COUNT(ta.id) as count
        FROM test_assignments ta
        JOIN samples s ON ta.sample_id = s.id
        WHERE ta.is_deleted = 0
        GROUP BY s.material_type
        ORDER BY count DESC
    """)
    
    material_stats = cursor.fetchall()
    
    if material_stats:
        df_materials = pd.DataFrame([dict(r) for r in material_stats])
        st.bar_chart(df_materials.set_index('material_type'))
    
    st.markdown("---")
    
    # Tests by status
    st.markdown("#### 📋 Tests by Status / الاختبارات حسب الحالة")
    
    cursor.execute("""
        SELECT status, COUNT(*) as count
        FROM test_assignments
        WHERE is_deleted = 0
        GROUP BY status
    """)
    
    status_stats = cursor.fetchall()
    
    if status_stats:
        for stat in status_stats:
            st.markdown(f"- **{stat['status'].replace('_', ' ').title()}**: {stat['count']}")
    
    conn.close()
