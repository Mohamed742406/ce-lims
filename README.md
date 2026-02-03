# CE-LIMS - Civil Engineering Laboratory Information Management System
## نظام إدارة معلومات مختبر الهندسة المدنية

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![ISO 17025](https://img.shields.io/badge/ISO-17025%20Compliant-green.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.31.0-red.svg)

---

## 📋 Overview / نظرة عامة

**CE-LIMS** is a comprehensive, bilingual (English/Arabic) Laboratory Information Management System designed specifically for civil engineering material testing laboratories. The system is fully compliant with **ISO 17025** standards and provides complete workflow management from sample registration to final report approval.

**CE-LIMS** هو نظام شامل ثنائي اللغة (إنجليزي/عربي) لإدارة معلومات المختبرات مصمم خصيصاً لمختبرات اختبار مواد الهندسة المدنية. النظام متوافق بالكامل مع معايير **ISO 17025** ويوفر إدارة كاملة لسير العمل من تسجيل العينات إلى اعتماد التقرير النهائي.

---

## ✨ Key Features / المميزات الرئيسية

### 🔐 Role-Based Access Control / التحكم في الوصول حسب الدور

The system implements **4 distinct user roles**, each with specific responsibilities and interfaces:

يطبق النظام **4 أدوار مستخدمين مختلفة**، كل منها له مسؤوليات وواجهات محددة:

#### 1. **Field Technician** (فني ميداني)
- Register samples from field locations
- Record collection details (date, time, location, condition)
- Set priority levels
- Mobile-friendly interface
- **Username:** `ahmed` | **Password:** `123456`

#### 2. **Supervisor** (مشرف)
- View pending samples
- Assign tests to lab technicians
- Set test priorities and due dates
- Monitor test progress
- **Username:** `sara` | **Password:** `123456`

#### 3. **Lab Technician** (فني مختبر)
- Execute assigned tests
- Enter test parameters and results
- Upload raw data files (PDF, CSV, Excel, images)
- Automated ASTM calculations
- Submit results for approval
- **Username:** `omar` | **Password:** `123456`

#### 4. **Manager** (مدير)
- Approve or reject test results
- Generate reports
- Archive completed samples
- View analytics and statistics
- **Username:** `fatima` | **Password:** `123456`

---

### 🧪 Supported Test Methods / طرق الاختبار المدعومة

The system includes **automated calculations** for the following ASTM standards:

يتضمن النظام **حسابات آلية** للمعايير التالية:

| Test Code | Test Name | Standard | Material |
|-----------|-----------|----------|----------|
| **ASTM D5** | Penetration Test | اختبار الاختراق | Asphalt Binder / رابط أسفلتي |
| **ASTM C39** | Compressive Strength | مقاومة الضغط | Concrete / خرسانة |
| **ASTM D1557** | Modified Proctor | بروكتور المعدل | Soil / تربة |
| **ASTM D2166** | Unconfined Compression | الضغط غير المحصور | Soil / تربة |
| **ASTM D4318** | Atterberg Limits | حدود أتربرج | Soil / تربة |
| **ASTM D1883** | California Bearing Ratio (CBR) | نسبة تحمل كاليفورنيا | Soil / تربة |

---

### 📊 ISO 17025 Compliance Features / ميزات الامتثال لـ ISO 17025

✅ **Chain of Custody** - سلسلة الحفظ  
✅ **Audit Trail** - سجل المراجعة  
✅ **Equipment Traceability** - تتبع المعدات  
✅ **Raw Data Preservation** - حفظ البيانات الخام  
✅ **Soft Delete** (No permanent deletion) - حذف مؤقت  
✅ **Approval Workflow** - سير عمل الاعتماد  
✅ **Version Control** - التحكم في الإصدارات  

---

## 🚀 Installation & Setup / التثبيت والإعداد

### Prerequisites / المتطلبات الأساسية

```bash
# Python 3.11 or higher
python3 --version

# pip package manager
pip3 --version
```

### Installation Steps / خطوات التثبيت

```bash
# 1. Clone or download the project
cd /path/to/ce-lims

# 2. Install required packages
pip3 install -r requirements.txt

# 3. Initialize database
python3 database.py

# 4. (Optional) Add test data
python3 add_test_data.py

# 5. Run the application
streamlit run app.py
```

The application will be available at: `http://localhost:8501`

سيكون التطبيق متاحاً على: `http://localhost:8501`

---

## 📁 Project Structure / هيكل المشروع

```
ce-lims/
│
├── app.py                  # Main application entry point / نقطة الدخول الرئيسية
├── database.py             # Database schema and initialization / قاعدة البيانات
├── auth.py                 # Authentication and authorization / المصادقة والتفويض
├── components.py           # Reusable UI components / مكونات واجهة المستخدم
│
├── field_tech.py           # Field Technician interface / واجهة الفني الميداني
├── supervisor.py           # Supervisor interface / واجهة المشرف
├── lab_tech.py             # Lab Technician interface / واجهة فني المختبر
├── manager.py              # Manager interface / واجهة المدير
│
├── calculations.py         # ASTM automated calculations / الحسابات الآلية
├── add_test_data.py        # Test data generator / مولد البيانات التجريبية
│
├── ce_lims.db              # SQLite database / قاعدة بيانات SQLite
├── requirements.txt        # Python dependencies / المكتبات المطلوبة
└── README.md               # This file / هذا الملف
```

---

## 🗄️ Database Schema / مخطط قاعدة البيانات

The system uses **SQLite** with the following main tables:

يستخدم النظام **SQLite** مع الجداول الرئيسية التالية:

- **users** - User accounts and roles / حسابات المستخدمين والأدوار
- **projects** - Construction projects / المشاريع الإنشائية
- **samples** - Sample registration / تسجيل العينات
- **test_methods** - Test method catalog / كتالوج طرق الاختبار
- **test_assignments** - Test assignments / تعيينات الاختبارات
- **test_results** - Test results and data / نتائج الاختبارات والبيانات
- **equipment** - Laboratory equipment / معدات المختبر
- **raw_files** - Uploaded raw data files / ملفات البيانات الخام المرفوعة
- **audit_log** - Complete audit trail / سجل المراجعة الكامل
- **chain_of_custody** - Sample custody tracking / تتبع حفظ العينات

---

## 🎨 Design Philosophy / فلسفة التصميم

The user interface is designed with the following principles:

تم تصميم واجهة المستخدم وفقاً للمبادئ التالية:

1. **Bilingual First** - Every label, button, and message is in both English and Arabic
   - **ثنائية اللغة أولاً** - كل تسمية وزر ورسالة بالإنجليزية والعربية

2. **Clean Industrial Design** - Professional, minimalist interface suitable for laboratory environment
   - **تصميم صناعي نظيف** - واجهة احترافية بسيطة مناسبة لبيئة المختبر

3. **Role-Specific Workflows** - Each role sees only relevant information and actions
   - **سير عمل خاص بالدور** - كل دور يرى فقط المعلومات والإجراءات ذات الصلة

4. **Mobile-Friendly** - Field technician interface optimized for mobile devices
   - **متوافق مع الجوال** - واجهة الفني الميداني محسنة للأجهزة المحمولة

---

## 📊 Workflow Example / مثال على سير العمل

```
1. Field Tech (Ahmed) → Registers sample from construction site
   الفني الميداني (أحمد) → يسجل عينة من موقع البناء

2. Supervisor (Sara) → Assigns penetration test to lab technician
   المشرف (سارة) → تعين اختبار الاختراق لفني المختبر

3. Lab Tech (Omar) → Executes test, enters data, uploads raw files
   فني المختبر (عمر) → ينفذ الاختبار، يدخل البيانات، يرفع الملفات الخام

4. System → Automatically calculates results using ASTM formulas
   النظام → يحسب النتائج تلقائياً باستخدام معادلات ASTM

5. Lab Tech → Submits results for approval
   فني المختبر → يرسل النتائج للاعتماد

6. Manager (Fatima) → Reviews and approves results
   المدير (فاطمة) → تراجع وتعتمد النتائج

7. Manager → Archives completed sample
   المدير → تؤرشف العينة المكتملة
```

---

## 🔒 Security Features / ميزات الأمان

- **Password Hashing** - SHA256 encryption for all passwords
  - **تشفير كلمات المرور** - تشفير SHA256 لجميع كلمات المرور

- **Session Management** - Secure session handling with Streamlit
  - **إدارة الجلسات** - معالجة آمنة للجلسات

- **Role-Based Access** - Strict permission enforcement
  - **الوصول حسب الدور** - تطبيق صارم للصلاحيات

- **Audit Logging** - Every action is logged with timestamp and user
  - **تسجيل المراجعة** - كل إجراء يُسجل مع الوقت والمستخدم

---

## 📈 Reporting & Analytics / التقارير والتحليلات

The Manager dashboard provides:

توفر لوحة تحكم المدير:

- **Custom Date Range Reports** - تقارير حسب نطاق زمني مخصص
- **Project-Based Filtering** - تصفية حسب المشروع
- **CSV Export** - تصدير CSV
- **Material Type Statistics** - إحصائيات حسب نوع المادة
- **Test Status Overview** - نظرة عامة على حالة الاختبارات
- **Performance Metrics** - مقاييس الأداء

---

## 🛠️ Customization / التخصيص

### Adding New Test Methods / إضافة طرق اختبار جديدة

1. Add test method to `test_methods` table in database
2. Create calculation function in `calculations.py`
3. Update `lab_tech.py` to handle new test parameters

### Adding New Material Types / إضافة أنواع مواد جديدة

1. Update material type options in `field_tech.py`
2. Associate test methods with new material type
3. Update validation rules if needed

---

## 📞 Support & Maintenance / الدعم والصيانة

### Database Backup / النسخ الاحتياطي لقاعدة البيانات

```bash
# Create backup
cp ce_lims.db ce_lims_backup_$(date +%Y%m%d).db

# Restore from backup
cp ce_lims_backup_20240203.db ce_lims.db
```

### Logs & Debugging / السجلات وتصحيح الأخطاء

```bash
# View Streamlit logs
streamlit run app.py --logger.level=debug

# Check database integrity
sqlite3 ce_lims.db "PRAGMA integrity_check;"
```

---

## 📝 License / الترخيص

This project is developed for civil engineering laboratories and is compliant with ISO 17025 standards.

تم تطوير هذا المشروع لمختبرات الهندسة المدنية ويتوافق مع معايير ISO 17025.

---

## 👥 Default Users / المستخدمون الافتراضيون

| Role | Username | Password | Full Name |
|------|----------|----------|-----------|
| Field Tech | `ahmed` | `123456` | Ahmed Mohamed / أحمد محمد |
| Supervisor | `sara` | `123456` | Sara Ali / سارة علي |
| Lab Tech | `omar` | `123456` | Omar Hassan / عمر حسن |
| Manager | `fatima` | `123456` | Fatima Abdullah / فاطمة عبدالله |

⚠️ **Important:** Change default passwords in production environment!  
⚠️ **مهم:** قم بتغيير كلمات المرور الافتراضية في بيئة الإنتاج!

---

## 🎯 Future Enhancements / التحسينات المستقبلية

- [ ] PDF Report Generation / إنشاء تقارير PDF
- [ ] Email Notifications / إشعارات البريد الإلكتروني
- [ ] Equipment Calibration Reminders / تذكيرات معايرة المعدات
- [ ] Advanced Analytics Dashboard / لوحة تحليلات متقدمة
- [ ] Multi-Laboratory Support / دعم مختبرات متعددة
- [ ] API Integration / تكامل API
- [ ] Mobile App / تطبيق الجوال

---

## 📧 Contact / التواصل

For questions, support, or feature requests, please contact the development team.

للأسئلة أو الدعم أو طلبات الميزات، يرجى التواصل مع فريق التطوير.

---

**© 2024 CE-LIMS. All rights reserved. / جميع الحقوق محفوظة.**
