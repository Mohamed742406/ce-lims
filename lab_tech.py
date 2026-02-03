"""
CE-LIMS Lab Technician Module
Interface for test execution and data entry (matching mockup design)
"""

import streamlit as st
from database import get_connection, log_audit
from auth import get_current_user
from components import *
from datetime import datetime
import json
import os

def show_lab_tech_dashboard():
    """Display Lab Tech dashboard"""
    load_custom_css()
    show_header("tests")
    show_page_title("Technician Test Execution", "تنفيذ الاختبار")
    
    user = get_current_user()
    
    # Get assigned tests
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            ta.id as assignment_id,
            s.id as sample_id,
            s.sample_id as sample_code,
            s.material_type,
            s.material_type_ar,
            p.project_name,
            p.project_name_ar,
            tm.id as test_method_id,
            tm.test_name,
            tm.test_name_ar,
            tm.standard,
            tm.parameters,
            s.received_date,
            s.priority,
            s.priority_ar,
            s.notes,
            ta.status,
            ta.due_date
        FROM test_assignments ta
        JOIN samples s ON ta.sample_id = s.id
        JOIN projects p ON s.project_id = p.id
        JOIN test_methods tm ON ta.test_method_id = tm.id
        WHERE ta.assigned_to = ? AND ta.is_deleted = 0 AND ta.status IN ('assigned', 'in_progress')
        ORDER BY 
            CASE s.priority
                WHEN 'urgent' THEN 1
                WHEN 'high' THEN 2
                WHEN 'normal' THEN 3
                WHEN 'low' THEN 4
            END,
            ta.due_date ASC
    """, (user['id'],))
    
    assignments = cursor.fetchall()
    
    if assignments:
        # Select test to work on
        test_options = {
            f"{a['sample_code']} - {a['test_name']} / {a['test_name_ar']}": a['assignment_id']
            for a in assignments
        }
        
        selected_test = st.selectbox(
            "Select Test to Execute / اختر الاختبار للتنفيذ",
            options=list(test_options.keys()),
            key="test_selector"
        )
        
        if selected_test:
            assignment_id = test_options[selected_test]
            assignment = next(a for a in assignments if a['assignment_id'] == assignment_id)
            
            show_test_execution_interface(user, assignment, conn)
    else:
        st.info("ℹ️ No tests assigned to you / لا توجد اختبارات معينة لك")
        st.markdown("Please wait for your supervisor to assign tests. / يرجى الانتظار حتى يقوم المشرف بتعيين الاختبارات.")
    
    conn.close()
    show_footer()

def show_test_execution_interface(user, assignment, conn):
    """Show test execution interface matching the mockup design"""
    
    # Calculate progress
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) as total FROM test_assignments WHERE sample_id = ? AND is_deleted = 0
    """, (assignment['sample_id'],))
    total_tests = cursor.fetchone()['total']
    
    cursor.execute("""
        SELECT COUNT(*) as completed FROM test_assignments 
        WHERE sample_id = ? AND status IN ('completed', 'approved') AND is_deleted = 0
    """, (assignment['sample_id'],))
    completed_tests = cursor.fetchone()['completed']
    
    progress = int((completed_tests / total_tests * 100)) if total_tests > 0 else 0
    
    # Two-column layout matching mockup
    col_left, col_right = st.columns([4, 8])
    
    # LEFT PANEL: Sample Details
    with col_left:
        st.markdown("""
            <div class="custom-card">
                <div class="card-header" style="display: flex; justify-content: space-between; align-items: start;">
                    <h2 class="card-title">
                        Sample Details <span class="separator">/</span> <span class="arabic-text">تفاصيل العينة</span>
                    </h2>
        """, unsafe_allow_html=True)
        
        # Status badge
        status_html = get_status_badge(assignment['status'])
        st.markdown(status_html + "</div></div>", unsafe_allow_html=True)
        
        # Sample details
        show_data_row("Sample ID", "معرف العينة", assignment['sample_code'])
        show_data_row("Project", "المشروع", assignment['project_name'])
        show_data_row("Material", "المادة", f"{assignment['material_type']}")
        show_data_row("Test Method", "طريقة الاختبار", f"{assignment['standard']} - {assignment['test_name']}")
        show_data_row("Date Received", "تاريخ الاستلام", assignment['received_date'])
        show_data_row("Priority", "الأولوية", f"{assignment['priority'].title()} / {assignment['priority_ar']}")
        
        if assignment['notes']:
            show_data_row("Notes", "ملاحظات", assignment['notes'])
        
        # Progress bar
        show_progress_bar("Progress complete", "التقدم المكتمل", progress)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # RIGHT PANEL: Test Execution
    with col_right:
        st.markdown("""
            <div class="custom-card">
                <div class="card-header">
                    <h2 class="card-title">
                        Test Execution <span class="separator">/</span> <span class="arabic-text">تنفيذ الاختبار</span>
                    </h2>
                    <p style="color: #6b7280; font-size: 0.875rem; margin-top: 0.25rem;">
        """, unsafe_allow_html=True)
        
        st.markdown(f"{assignment['test_name']} <span class='separator'>/</span> <span class='arabic-text'>{assignment['test_name_ar']}</span>", unsafe_allow_html=True)
        st.markdown("</p></div>", unsafe_allow_html=True)
        
        # Test Parameters Form
        st.markdown("<h3 style='font-weight: bold; color: #1f2937; margin-top: 1rem;'>Test Parameters <span class='separator'>/</span> <span class='arabic-text'>معلومات الاختبار</span></h3>", unsafe_allow_html=True)
        
        # Check if test result already exists
        cursor.execute("""
            SELECT id, test_parameters, raw_data, result_value, result_unit, observations, status
            FROM test_results
            WHERE assignment_id = ? AND is_deleted = 0
        """, (assignment['assignment_id'],))
        
        existing_result = cursor.fetchone()
        
        with st.form(f"test_execution_form_{assignment['assignment_id']}"):
            # Parse test parameters
            try:
                params = json.loads(assignment['parameters']) if assignment['parameters'] else {}
            except:
                params = {}
            
            # Dynamic form based on test type
            test_data = {}
            
            if assignment['standard'] == 'ASTM D5':  # Penetration Test
                col1, col2 = st.columns(2)
                
                with col1:
                    temperature = st.number_input(
                        "Temperature / درجة الحرارة (°C):",
                        min_value=0.0,
                        max_value=100.0,
                        value=25.0,
                        step=0.1,
                        key=f"temp_{assignment['assignment_id']}"
                    )
                    test_data['temperature'] = temperature
                
                with col2:
                    needle_load = st.number_input(
                        "Needle Load / حمل الإبرة (g):",
                        min_value=0.0,
                        max_value=200.0,
                        value=100.0,
                        step=1.0,
                        key=f"load_{assignment['assignment_id']}"
                    )
                    test_data['needle_load'] = needle_load
                
                st.markdown("#### Penetration Readings / قراءات الاختراق")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    reading1 = st.number_input("Reading 1 (0.1mm)", min_value=0.0, step=0.1, key=f"r1_{assignment['assignment_id']}")
                with col2:
                    reading2 = st.number_input("Reading 2 (0.1mm)", min_value=0.0, step=0.1, key=f"r2_{assignment['assignment_id']}")
                with col3:
                    reading3 = st.number_input("Reading 3 (0.1mm)", min_value=0.0, step=0.1, key=f"r3_{assignment['assignment_id']}")
                
                test_data['readings'] = [reading1, reading2, reading3]
                
                # Auto-calculate average
                if reading1 > 0 or reading2 > 0 or reading3 > 0:
                    avg_penetration = sum([reading1, reading2, reading3]) / 3
                    st.info(f"📊 Average Penetration: {avg_penetration:.1f} (0.1mm) / متوسط الاختراق: {avg_penetration:.1f}")
                    test_data['result_value'] = avg_penetration
                    test_data['result_unit'] = '0.1mm'
            
            elif assignment['standard'] == 'ASTM C39':  # Compressive Strength
                col1, col2 = st.columns(2)
                
                with col1:
                    diameter = st.number_input(
                        "Diameter / القطر (mm):",
                        min_value=0.0,
                        value=150.0,
                        step=1.0,
                        key=f"dia_{assignment['assignment_id']}"
                    )
                    test_data['diameter'] = diameter
                
                with col2:
                    height = st.number_input(
                        "Height / الارتفاع (mm):",
                        min_value=0.0,
                        value=300.0,
                        step=1.0,
                        key=f"height_{assignment['assignment_id']}"
                    )
                    test_data['height'] = height
                
                max_load = st.number_input(
                    "Maximum Load / الحمل الأقصى (kN):",
                    min_value=0.0,
                    step=0.1,
                    key=f"load_{assignment['assignment_id']}"
                )
                test_data['max_load'] = max_load
                
                # Auto-calculate compressive strength
                if diameter > 0 and max_load > 0:
                    area = 3.14159 * (diameter/2)**2  # mm²
                    strength = (max_load * 1000) / area  # MPa
                    st.info(f"📊 Compressive Strength: {strength:.2f} MPa / مقاومة الضغط: {strength:.2f}")
                    test_data['result_value'] = strength
                    test_data['result_unit'] = 'MPa'
            
            else:  # Generic test
                result_value = st.number_input(
                    "Result Value / قيمة النتيجة:",
                    min_value=0.0,
                    step=0.1,
                    key=f"result_{assignment['assignment_id']}"
                )
                
                result_unit = st.text_input(
                    "Unit / الوحدة:",
                    key=f"unit_{assignment['assignment_id']}"
                )
                
                test_data['result_value'] = result_value
                test_data['result_unit'] = result_unit
            
            # Estimated Time
            estimated_time = st.text_input(
                "Estimated Time / الوقت المتوقع",
                placeholder="e.g., 45 min",
                key=f"time_{assignment['assignment_id']}"
            )
            test_data['estimated_time'] = estimated_time
            
            # Upload Area (matching mockup)
            st.markdown("""
                <div style="margin-top: 1.5rem; border: 2px dashed #93c5fd; border-radius: 8px; 
                     background-color: rgba(59, 130, 246, 0.05); padding: 2rem; text-align: center;">
                    <div style="background-color: #2563eb; color: white; width: 48px; height: 48px; 
                         border-radius: 50%; display: inline-flex; align-items: center; 
                         justify-content: center; font-size: 1.5rem; margin-bottom: 1rem;">
                        ⬆️
                    </div>
                    <h4 style="font-weight: bold; color: #1f2937; margin-bottom: 0.5rem;">
                        Upload Drafts & Raw Data <span class="separator">/</span> 
                        <span class="arabic-text">رفع المسودات والبيانات الخام</span>
                    </h4>
                    <p style="font-size: 0.875rem; color: #6b7280;">
                        Drag files here or click to select<br>
                        <span class="arabic-text">اسحب الملفات هنا أو اضغط للاختيار</span>
                    </p>
                    <p style="font-size: 0.75rem; color: #9ca3af; margin-top: 0.5rem;">
                        Supports file types: .pdf, .csv, .xlsx, .jpg
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            uploaded_files = st.file_uploader(
                "Browse Files / تصفح الملفات",
                accept_multiple_files=True,
                type=['pdf', 'csv', 'xlsx', 'jpg', 'png'],
                key=f"files_{assignment['assignment_id']}"
            )
            
            # Observations
            observations = st.text_area(
                "Observations / الملاحظات",
                placeholder="Enter any observations or notes about the test...\nأدخل أي ملاحظات حول الاختبار...",
                height=100,
                key=f"obs_{assignment['assignment_id']}"
            )
            
            # Action buttons matching mockup
            col1, col2 = st.columns(2)
            
            with col1:
                start_btn = st.form_submit_button(
                    "▶️ Start Test / بدء الاختبار",
                    use_container_width=True
                )
            
            with col2:
                finish_btn = st.form_submit_button(
                    "✅ Finish Testing / إنهاء الاختبارات",
                    use_container_width=True,
                    type="primary"
                )
            
            if start_btn:
                # Update assignment status to in_progress
                cursor.execute("""
                    UPDATE test_assignments
                    SET status = 'in_progress'
                    WHERE id = ?
                """, (assignment['assignment_id'],))
                
                # Create or update test result
                cursor.execute("""
                    INSERT OR REPLACE INTO test_results (
                        assignment_id, tested_by, test_started_at, status
                    ) VALUES (?, ?, CURRENT_TIMESTAMP, 'draft')
                """, (assignment['assignment_id'], user['id']))
                
                conn.commit()
                st.success("✅ Test started! / بدأ الاختبار!")
                st.rerun()
            
            if finish_btn:
                if 'result_value' in test_data and test_data['result_value'] > 0:
                    try:
                        # Save uploaded files
                        file_ids = []
                        if uploaded_files:
                            upload_dir = f"/home/ubuntu/ce-lims/uploads/{assignment['sample_code']}"
                            os.makedirs(upload_dir, exist_ok=True)
                            
                            for uploaded_file in uploaded_files:
                                file_path = os.path.join(upload_dir, uploaded_file.name)
                                with open(file_path, "wb") as f:
                                    f.write(uploaded_file.getbuffer())
                                
                                # Save to database
                                if existing_result:
                                    cursor.execute("""
                                        INSERT INTO raw_files (test_result_id, file_name, file_path, file_type, file_size, uploaded_by)
                                        VALUES (?, ?, ?, ?, ?, ?)
                                    """, (
                                        existing_result['id'], uploaded_file.name, file_path,
                                        uploaded_file.type, uploaded_file.size, user['id']
                                    ))
                                    file_ids.append(cursor.lastrowid)
                        
                        # Insert or update test result
                        if existing_result:
                            cursor.execute("""
                                UPDATE test_results
                                SET test_completed_at = CURRENT_TIMESTAMP,
                                    test_parameters = ?,
                                    raw_data = ?,
                                    result_value = ?,
                                    result_unit = ?,
                                    observations = ?,
                                    status = 'submitted',
                                    updated_at = CURRENT_TIMESTAMP,
                                    updated_by = ?
                                WHERE id = ?
                            """, (
                                json.dumps(test_data), json.dumps(test_data),
                                test_data.get('result_value', 0), test_data.get('result_unit', ''),
                                observations, user['id'], existing_result['id']
                            ))
                            result_id = existing_result['id']
                        else:
                            cursor.execute("""
                                INSERT INTO test_results (
                                    assignment_id, tested_by, test_started_at, test_completed_at,
                                    test_parameters, raw_data, result_value, result_unit,
                                    observations, status, created_by
                                ) VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, 'submitted', ?)
                            """, (
                                assignment['assignment_id'], user['id'],
                                json.dumps(test_data), json.dumps(test_data),
                                test_data.get('result_value', 0), test_data.get('result_unit', ''),
                                observations, user['id']
                            ))
                            result_id = cursor.lastrowid
                        
                        # Update assignment status
                        cursor.execute("""
                            UPDATE test_assignments
                            SET status = 'completed'
                            WHERE id = ?
                        """, (assignment['assignment_id'],))
                        
                        # Update sample status
                        cursor.execute("""
                            UPDATE samples
                            SET status = 'completed'
                            WHERE id = ?
                        """, (assignment['sample_id'],))
                        
                        # Log audit
                        log_audit(
                            'test_results', result_id, 'INSERT',
                            None, json.dumps({'assignment_id': assignment['assignment_id'], 'status': 'submitted'}),
                            user['id']
                        )
                        
                        conn.commit()
                        st.success("✅ Test completed successfully! / تم إكمال الاختبار بنجاح!")
                        st.balloons()
                        st.rerun()
                        
                    except Exception as e:
                        conn.rollback()
                        st.error(f"❌ Error: {str(e)}")
                else:
                    st.warning("⚠️ Please enter test results / الرجاء إدخال نتائج الاختبار")
        
        st.markdown("</div>", unsafe_allow_html=True)
