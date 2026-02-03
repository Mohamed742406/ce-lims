"""
Add test data to demonstrate the system workflow
"""

from database import get_connection, log_audit, add_chain_of_custody
from datetime import date, datetime, timedelta
import json

def add_sample_workflow():
    """Add a complete workflow example"""
    conn = get_connection()
    cursor = conn.cursor()
    
    print("🚀 Adding test workflow data...")
    
    # 1. Field Tech registers a sample
    print("\n1️⃣ Field Tech (Ahmed) registers sample...")
    
    cursor.execute("""
        INSERT INTO samples (
            sample_id, project_id, material_type, material_type_ar,
            sample_location, quantity, quantity_unit,
            collection_date, collection_time, received_date, received_time,
            received_by, temperature, condition, condition_ar,
            priority, priority_ar, notes, status, created_by
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        'S-2024-02-03-001', 1, 'Asphalt Binder', 'رابط أسفلتي',
        'Station 5+200', 5.0, 'kg',
        date.today(), '09:30:00', date.today(), '10:15:00',
        1, 25.0, 'Good', 'جيدة',
        'high', 'عالي', 'Handle with care, temp sensitive.', 'registered', 1
    ))
    
    sample_id = cursor.lastrowid
    print(f"   ✅ Sample S-2024-02-03-001 registered (ID: {sample_id})")
    
    # Add chain of custody
    add_chain_of_custody(
        sample_id, None, 1,
        'Station 5+200', 'Sample Collection',
        'Good', 'Collected by Ahmed Mohamed', conn
    )
    
    # 2. Supervisor assigns tests
    print("\n2️⃣ Supervisor (Sara) assigns tests...")
    
    # Assign Penetration Test
    cursor.execute("""
        INSERT INTO test_assignments (
            sample_id, test_method_id, assigned_to, assigned_by,
            due_date, priority, notes, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        sample_id, 1, 3, 2,  # Assign to Omar (lab_tech)
        date.today() + timedelta(days=3), 'high',
        'Priority test - required for project milestone', 'assigned'
    ))
    
    assignment_id = cursor.lastrowid
    print(f"   ✅ Penetration Test assigned to Omar (Assignment ID: {assignment_id})")
    
    # Update sample status
    cursor.execute("""
        UPDATE samples SET status = 'assigned', updated_by = 2 WHERE id = ?
    """, (sample_id,))
    
    # 3. Add another sample for concrete testing
    print("\n3️⃣ Adding concrete sample...")
    
    cursor.execute("""
        INSERT INTO samples (
            sample_id, project_id, material_type, material_type_ar,
            sample_location, quantity, quantity_unit,
            collection_date, collection_time, received_date, received_time,
            received_by, temperature, condition, condition_ar,
            priority, priority_ar, notes, status, created_by
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        'S-2024-02-03-002', 2, 'Concrete', 'خرسانة',
        'Column C-15', 3.0, 'pieces',
        date.today() - timedelta(days=28), '08:00:00', date.today() - timedelta(days=28), '09:00:00',
        1, 20.0, 'Good', 'جيدة',
        'normal', 'عادي', '28-day strength test', 'registered', 1
    ))
    
    sample_id_2 = cursor.lastrowid
    print(f"   ✅ Concrete sample S-2024-02-03-002 registered (ID: {sample_id_2})")
    
    # Assign Compressive Strength Test
    cursor.execute("""
        INSERT INTO test_assignments (
            sample_id, test_method_id, assigned_to, assigned_by,
            due_date, priority, notes, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        sample_id_2, 2, 3, 2,  # ASTM C39
        date.today() + timedelta(days=1), 'normal',
        '28-day compressive strength', 'assigned'
    ))
    
    assignment_id_2 = cursor.lastrowid
    print(f"   ✅ Compressive Strength Test assigned (Assignment ID: {assignment_id_2})")
    
    cursor.execute("""
        UPDATE samples SET status = 'assigned', updated_by = 2 WHERE id = ?
    """, (sample_id_2,))
    
    # 4. Add a completed test for manager approval
    print("\n4️⃣ Adding completed test for approval...")
    
    cursor.execute("""
        INSERT INTO samples (
            sample_id, project_id, material_type, material_type_ar,
            sample_location, quantity, quantity_unit,
            collection_date, collection_time, received_date, received_time,
            received_by, temperature, condition, condition_ar,
            priority, priority_ar, notes, status, created_by
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        'S-2024-02-02-001', 1, 'Soil', 'تربة',
        'Borehole BH-5', 10.0, 'kg',
        date.today() - timedelta(days=5), '10:00:00', date.today() - timedelta(days=5), '11:00:00',
        1, 22.0, 'Good', 'جيدة',
        'normal', 'عادي', 'Soil classification test', 'completed', 1
    ))
    
    sample_id_3 = cursor.lastrowid
    
    cursor.execute("""
        INSERT INTO test_assignments (
            sample_id, test_method_id, assigned_to, assigned_by,
            due_date, priority, notes, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        sample_id_3, 5, 3, 2,  # Atterberg Limits
        date.today() - timedelta(days=2), 'normal',
        'Soil classification', 'completed'
    ))
    
    assignment_id_3 = cursor.lastrowid
    
    # Add test result
    test_data = {
        'liquid_limit': 45,
        'plastic_limit': 28
    }
    
    cursor.execute("""
        INSERT INTO test_results (
            assignment_id, tested_by, test_started_at, test_completed_at,
            test_parameters, raw_data, result_value, result_unit,
            observations, status, created_by
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        assignment_id_3, 3,
        datetime.now() - timedelta(days=2, hours=2),
        datetime.now() - timedelta(days=2),
        json.dumps(test_data), json.dumps(test_data),
        17.0, 'PI',
        'Soil shows medium plasticity characteristics',
        'submitted', 3
    ))
    
    print(f"   ✅ Atterberg Limits test completed and submitted for approval")
    
    conn.commit()
    conn.close()
    
    print("\n✅ Test workflow data added successfully!")
    print("\n📋 Summary:")
    print("   - 3 samples registered")
    print("   - 3 test assignments created")
    print("   - 1 test result submitted for approval")
    print("\n🔑 Login Credentials:")
    print("   Field Tech:  ahmed / 123456")
    print("   Supervisor:  sara / 123456")
    print("   Lab Tech:    omar / 123456")
    print("   Manager:     fatima / 123456")

if __name__ == "__main__":
    add_sample_workflow()
