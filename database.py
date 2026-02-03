"""
CE-LIMS Database Module
ISO 17025 Compliant Database Structure
"""

import sqlite3
from datetime import datetime
import hashlib
import os

DB_PATH = "ce_lims.db"

def get_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_database():
    """Initialize database with all required tables"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users table with roles
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            full_name_ar TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('field_tech', 'supervisor', 'lab_tech', 'manager')),
            email TEXT,
            phone TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_by INTEGER,
            updated_at TIMESTAMP,
            updated_by INTEGER
        )
    """)
    
    # Projects table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_code TEXT UNIQUE NOT NULL,
            project_name TEXT NOT NULL,
            project_name_ar TEXT NOT NULL,
            client_name TEXT,
            client_name_ar TEXT,
            location TEXT,
            location_ar TEXT,
            start_date DATE,
            end_date DATE,
            status TEXT DEFAULT 'active' CHECK(status IN ('active', 'completed', 'archived')),
            notes TEXT,
            is_deleted INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_by INTEGER,
            updated_at TIMESTAMP,
            updated_by INTEGER,
            FOREIGN KEY (created_by) REFERENCES users(id),
            FOREIGN KEY (updated_by) REFERENCES users(id)
        )
    """)
    
    # Samples table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS samples (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sample_id TEXT UNIQUE NOT NULL,
            project_id INTEGER NOT NULL,
            material_type TEXT NOT NULL,
            material_type_ar TEXT NOT NULL,
            sample_location TEXT,
            sample_location_ar TEXT,
            quantity REAL,
            quantity_unit TEXT,
            collection_date DATE,
            collection_time TIME,
            received_date DATE,
            received_time TIME,
            received_by INTEGER,
            temperature REAL,
            condition TEXT,
            condition_ar TEXT,
            priority TEXT DEFAULT 'normal' CHECK(priority IN ('low', 'normal', 'high', 'urgent')),
            priority_ar TEXT,
            notes TEXT,
            notes_ar TEXT,
            status TEXT DEFAULT 'registered' CHECK(status IN ('registered', 'assigned', 'in_progress', 'completed', 'approved', 'archived')),
            is_deleted INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_by INTEGER,
            updated_at TIMESTAMP,
            updated_by INTEGER,
            FOREIGN KEY (project_id) REFERENCES projects(id),
            FOREIGN KEY (received_by) REFERENCES users(id),
            FOREIGN KEY (created_by) REFERENCES users(id),
            FOREIGN KEY (updated_by) REFERENCES users(id)
        )
    """)
    
    # Test methods catalog
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_methods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_code TEXT UNIQUE NOT NULL,
            test_name TEXT NOT NULL,
            test_name_ar TEXT NOT NULL,
            standard TEXT NOT NULL,
            standard_ar TEXT,
            material_type TEXT NOT NULL,
            description TEXT,
            description_ar TEXT,
            parameters TEXT,
            calculation_formula TEXT,
            typical_duration INTEGER,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_by INTEGER,
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
    """)
    
    # Test assignments
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sample_id INTEGER NOT NULL,
            test_method_id INTEGER NOT NULL,
            assigned_to INTEGER,
            assigned_by INTEGER NOT NULL,
            assigned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            due_date DATE,
            priority TEXT DEFAULT 'normal' CHECK(priority IN ('low', 'normal', 'high', 'urgent')),
            status TEXT DEFAULT 'assigned' CHECK(status IN ('assigned', 'in_progress', 'completed', 'approved', 'rejected')),
            notes TEXT,
            is_deleted INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP,
            FOREIGN KEY (sample_id) REFERENCES samples(id),
            FOREIGN KEY (test_method_id) REFERENCES test_methods(id),
            FOREIGN KEY (assigned_to) REFERENCES users(id),
            FOREIGN KEY (assigned_by) REFERENCES users(id)
        )
    """)
    
    # Test results
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            assignment_id INTEGER NOT NULL,
            test_started_at TIMESTAMP,
            test_completed_at TIMESTAMP,
            tested_by INTEGER NOT NULL,
            equipment_id INTEGER,
            test_parameters TEXT,
            raw_data TEXT,
            calculated_results TEXT,
            result_value REAL,
            result_unit TEXT,
            pass_fail TEXT CHECK(pass_fail IN ('pass', 'fail', 'na', NULL)),
            observations TEXT,
            observations_ar TEXT,
            status TEXT DEFAULT 'draft' CHECK(status IN ('draft', 'submitted', 'approved', 'rejected')),
            approved_by INTEGER,
            approved_at TIMESTAMP,
            rejection_reason TEXT,
            is_deleted INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_by INTEGER,
            updated_at TIMESTAMP,
            updated_by INTEGER,
            FOREIGN KEY (assignment_id) REFERENCES test_assignments(id),
            FOREIGN KEY (tested_by) REFERENCES users(id),
            FOREIGN KEY (equipment_id) REFERENCES equipment(id),
            FOREIGN KEY (approved_by) REFERENCES users(id),
            FOREIGN KEY (created_by) REFERENCES users(id),
            FOREIGN KEY (updated_by) REFERENCES users(id)
        )
    """)
    
    # Equipment table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipment_code TEXT UNIQUE NOT NULL,
            equipment_name TEXT NOT NULL,
            equipment_name_ar TEXT NOT NULL,
            manufacturer TEXT,
            model TEXT,
            serial_number TEXT,
            calibration_date DATE,
            calibration_due_date DATE,
            calibration_certificate TEXT,
            status TEXT DEFAULT 'active' CHECK(status IN ('active', 'maintenance', 'calibration', 'retired')),
            location TEXT,
            notes TEXT,
            is_deleted INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_by INTEGER,
            updated_at TIMESTAMP,
            updated_by INTEGER,
            FOREIGN KEY (created_by) REFERENCES users(id),
            FOREIGN KEY (updated_by) REFERENCES users(id)
        )
    """)
    
    # Raw files storage
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_result_id INTEGER NOT NULL,
            file_name TEXT NOT NULL,
            file_path TEXT NOT NULL,
            file_type TEXT NOT NULL,
            file_size INTEGER,
            uploaded_by INTEGER NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            description TEXT,
            is_deleted INTEGER DEFAULT 0,
            FOREIGN KEY (test_result_id) REFERENCES test_results(id),
            FOREIGN KEY (uploaded_by) REFERENCES users(id)
        )
    """)
    
    # Audit log for ISO 17025 compliance
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_name TEXT NOT NULL,
            record_id INTEGER NOT NULL,
            action TEXT NOT NULL CHECK(action IN ('INSERT', 'UPDATE', 'DELETE', 'APPROVE', 'REJECT')),
            old_values TEXT,
            new_values TEXT,
            changed_by INTEGER NOT NULL,
            changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip_address TEXT,
            user_agent TEXT,
            FOREIGN KEY (changed_by) REFERENCES users(id)
        )
    """)
    
    # Chain of custody
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chain_of_custody (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sample_id INTEGER NOT NULL,
            custody_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            from_person INTEGER,
            to_person INTEGER NOT NULL,
            location TEXT,
            purpose TEXT,
            condition TEXT,
            notes TEXT,
            FOREIGN KEY (sample_id) REFERENCES samples(id),
            FOREIGN KEY (from_person) REFERENCES users(id),
            FOREIGN KEY (to_person) REFERENCES users(id)
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

def seed_initial_data():
    """Seed database with initial data"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if users already exist
    cursor.execute("SELECT COUNT(*) as count FROM users")
    if cursor.fetchone()['count'] > 0:
        print("⚠️  Database already contains data. Skipping seed.")
        conn.close()
        return
    
    # Create default users for each role
    users = [
        ('ahmed', hash_password('123456'), 'Ahmed Mohamed', 'أحمد محمد', 'field_tech', 'ahmed@celims.com', '+966501234567'),
        ('sara', hash_password('123456'), 'Sara Ali', 'سارة علي', 'supervisor', 'sara@celims.com', '+966501234568'),
        ('omar', hash_password('123456'), 'Omar Hassan', 'عمر حسن', 'lab_tech', 'omar@celims.com', '+966501234569'),
        ('fatima', hash_password('123456'), 'Fatima Abdullah', 'فاطمة عبدالله', 'manager', 'fatima@celims.com', '+966501234570'),
    ]
    
    cursor.executemany("""
        INSERT INTO users (username, password, full_name, full_name_ar, role, email, phone)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, users)
    
    # Create sample projects
    projects = [
        ('PRJ-2024-001', 'Highway A7 Expansion', 'توسعة طريق A7 السريع', 'Ministry of Transport', 'وزارة النقل', 'Riyadh-Dammam', 'الرياض-الدمام', '2024-01-01', '2024-12-31', 'active'),
        ('PRJ-2024-002', 'King Abdullah Bridge', 'جسر الملك عبدالله', 'Royal Commission', 'الهيئة الملكية', 'Jeddah', 'جدة', '2024-02-01', '2024-11-30', 'active'),
    ]
    
    cursor.executemany("""
        INSERT INTO projects (project_code, project_name, project_name_ar, client_name, client_name_ar, location, location_ar, start_date, end_date, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, projects)
    
    # Create test methods
    test_methods = [
        ('ASTM-D5', 'Penetration Test', 'اختبار الاختراق', 'ASTM D5', 'ASTM D5', 'Asphalt Binder', 'Test for penetration of bituminous materials', 'اختبار اختراق المواد البيتومينية', '{"temperature": 25, "load": 100, "time": 5}', 'penetration = depth / 10', 60),
        ('ASTM-C39', 'Compressive Strength', 'مقاومة الضغط', 'ASTM C39', 'ASTM C39', 'Concrete', 'Standard test method for compressive strength of cylindrical concrete specimens', 'طريقة الاختبار القياسية لمقاومة الضغط للعينات الخرسانية الأسطوانية', '{"diameter": 150, "height": 300}', 'strength = load / area', 30),
        ('ASTM-D1557', 'Modified Proctor', 'بروكتور المعدل', 'ASTM D1557', 'ASTM D1557', 'Soil', 'Laboratory compaction characteristics of soil', 'خصائص الدمك المعملي للتربة', '{"layers": 5, "blows": 25}', 'density = mass / volume', 120),
        ('ASTM-D2166', 'Unconfined Compression', 'الضغط غير المحصور', 'ASTM D2166', 'ASTM D2166', 'Soil', 'Unconfined compressive strength of cohesive soil', 'مقاومة الضغط غير المحصور للتربة المتماسكة', '{"strain_rate": 1}', 'qu = P / A', 45),
        ('ASTM-D4318', 'Atterberg Limits', 'حدود أتربرج', 'ASTM D4318', 'ASTM D4318', 'Soil', 'Liquid limit, plastic limit, and plasticity index of soils', 'حد السيولة وحد اللدونة ومعامل اللدونة للتربة', '{}', 'PI = LL - PL', 90),
    ]
    
    cursor.executemany("""
        INSERT INTO test_methods (test_code, test_name, test_name_ar, standard, standard_ar, material_type, description, description_ar, parameters, calculation_formula, typical_duration)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, test_methods)
    
    # Create sample equipment
    equipment = [
        ('EQ-001', 'Penetrometer', 'جهاز الاختراق', 'Controls Group', 'Model 2020', 'SN-12345', '2024-01-15', '2025-01-15', 'CERT-2024-001', 'active', 'Lab Room 1'),
        ('EQ-002', 'Compression Machine', 'آلة الضغط', 'ELE International', 'ADR-3000', 'SN-67890', '2024-02-01', '2025-02-01', 'CERT-2024-002', 'active', 'Lab Room 2'),
        ('EQ-003', 'Proctor Mold', 'قالب بروكتور', 'Humboldt', 'H-4140', 'SN-11223', '2024-01-20', '2025-01-20', 'CERT-2024-003', 'active', 'Lab Room 1'),
    ]
    
    cursor.executemany("""
        INSERT INTO equipment (equipment_code, equipment_name, equipment_name_ar, manufacturer, model, serial_number, calibration_date, calibration_due_date, calibration_certificate, status, location)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, equipment)
    
    conn.commit()
    conn.close()
    print("✅ Initial data seeded successfully!")
    print("\n📋 Default Users Created:")
    print("  Field Tech    - Username: ahmed    Password: 123456")
    print("  Supervisor    - Username: sara     Password: 123456")
    print("  Lab Tech      - Username: omar     Password: 123456")
    print("  Manager       - Username: fatima   Password: 123456")

def log_audit(table_name, record_id, action, old_values, new_values, changed_by):
    """Log audit trail for ISO 17025 compliance"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO audit_log (table_name, record_id, action, old_values, new_values, changed_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (table_name, record_id, action, old_values, new_values, changed_by))
    
    conn.commit()
    conn.close()

def add_chain_of_custody(sample_id, from_person, to_person, location, purpose, condition, notes, conn=None):
    """Add chain of custody record"""
    close_conn = False
    if conn is None:
        conn = get_connection()
        close_conn = True
    
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO chain_of_custody (sample_id, from_person, to_person, location, purpose, condition, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (sample_id, from_person, to_person, location, purpose, condition, notes))
    
    if close_conn:
        conn.commit()
        conn.close()

if __name__ == "__main__":
    print("🚀 Initializing CE-LIMS Database...")
    init_database()
    seed_initial_data()
    print("\n✅ Database setup completed!")
