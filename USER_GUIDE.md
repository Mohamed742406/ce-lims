# CE-LIMS User Guide / دليل المستخدم
## Quick Start Guide / دليل البدء السريع

---

## 🚀 Getting Started / البدء

### 1. Access the System / الوصول إلى النظام

Open your web browser and navigate to the CE-LIMS URL provided by your administrator.

افتح متصفح الويب الخاص بك وانتقل إلى عنوان URL لـ CE-LIMS المقدم من المسؤول.

### 2. Login / تسجيل الدخول

Enter your username and password, then click "Login / دخول"

أدخل اسم المستخدم وكلمة المرور، ثم انقر على "Login / دخول"

---

## 👷 Field Technician Guide / دليل الفني الميداني

### Role: Sample Registration / الدور: تسجيل العينات

As a Field Technician, your primary responsibility is to register samples collected from construction sites.

كفني ميداني، مسؤوليتك الأساسية هي تسجيل العينات المجمعة من مواقع البناء.

### Step-by-Step Process / العملية خطوة بخطوة

#### 1. Register New Sample / تسجيل عينة جديدة

1. Click on "Register New Sample / تسجيل عينة جديدة" tab
2. Select the **Project** from the dropdown list
3. The **Sample ID** is automatically generated (e.g., S-2024-02-03-001)
4. Select **Material Type** (Concrete, Asphalt, Soil, etc.)
5. Enter **Sample Location** (e.g., "Station 5+200")
6. Enter **Quantity** and select **Unit**
7. Enter **Temperature** if applicable
8. Select **Collection Date** and **Time**
9. Select **Sample Condition** (Good, Fair, Poor, Damaged)
10. Select **Priority** (Low, Normal, High, Urgent)
11. Add any **Notes** or special instructions
12. Click "✅ Register Sample / تسجيل العينة"

#### 2. View Your Samples / عرض عيناتك

Click on "My Samples / عيناتي" tab to see all samples you have registered.

انقر على علامة التبويب "My Samples / عيناتي" لرؤية جميع العينات التي سجلتها.

### Tips / نصائح

- ✅ Always verify project selection before registering
- ✅ Use clear, descriptive location names
- ✅ Set appropriate priority based on project requirements
- ✅ Add detailed notes for special handling requirements

---

## 👨‍💼 Supervisor Guide / دليل المشرف

### Role: Test Assignment & Management / الدور: تعيين وإدارة الاختبارات

As a Supervisor, you assign tests to lab technicians and monitor progress.

كمشرف، تقوم بتعيين الاختبارات لفنيي المختبر ومراقبة التقدم.

### Step-by-Step Process / العملية خطوة بخطوة

#### 1. Review Pending Samples / مراجعة العينات المعلقة

1. Go to "Pending Samples / العينات المعلقة" tab
2. Review the list of samples awaiting test assignment
3. Samples are sorted by priority (Urgent → High → Normal → Low)

#### 2. Assign Tests / تعيين الاختبارات

1. Click on a sample to expand its details
2. Review sample information (material type, project, notes)
3. Select one or more **Tests** from the available list
   - Tests are filtered based on material type
   - Example: For "Asphalt Binder" → ASTM D5 Penetration Test
4. Select **Lab Technician** to assign the test to
5. Set **Due Date**
6. Set **Test Priority**
7. Add **Assignment Notes** if needed
8. Click "✅ Assign Tests / تعيين الاختبارات"

#### 3. Monitor Assigned Tests / مراقبة الاختبارات المعينة

1. Go to "Assigned Tests / الاختبارات المعينة" tab
2. Filter by status (All, Assigned, In Progress, Completed, Approved)
3. View test details including:
   - Sample ID
   - Test name
   - Assigned technician
   - Due date
   - Current status

#### 4. View Overview / عرض النظرة العامة

The "Overview / نظرة عامة" tab provides:
- Pending samples count
- Assigned tests count
- In-progress tests count
- Completed tests count
- Recent activity log

### Tips / نصائح

- ✅ Assign urgent tests first
- ✅ Balance workload among lab technicians
- ✅ Set realistic due dates based on test complexity
- ✅ Add clear assignment notes for special requirements

---

## 🔬 Lab Technician Guide / دليل فني المختبر

### Role: Test Execution & Data Entry / الدور: تنفيذ الاختبار وإدخال البيانات

As a Lab Technician, you execute tests, enter data, and upload raw files.

كفني مختبر، تقوم بتنفيذ الاختبارات وإدخال البيانات ورفع الملفات الخام.

### Step-by-Step Process / العملية خطوة بخطوة

#### 1. Select Test to Execute / اختيار الاختبار للتنفيذ

1. From the dropdown, select the test you want to work on
2. The system shows tests assigned to you with status "Assigned" or "In Progress"

#### 2. Review Sample Details / مراجعة تفاصيل العينة

The left panel shows:
- Sample ID
- Project name
- Material type
- Test method
- Date received
- Priority
- Notes
- Progress percentage

#### 3. Start Test / بدء الاختبار

1. Click "▶️ Start Test / بدء الاختبار"
2. This changes the test status to "In Progress"

#### 4. Enter Test Parameters / إدخال معلمات الاختبار

Depending on the test type, enter required parameters:

**For ASTM D5 (Penetration Test):**
- Temperature (°C)
- Needle Load (g)
- Three penetration readings (0.1mm)
- System automatically calculates average

**For ASTM C39 (Compressive Strength):**
- Diameter (mm)
- Height (mm)
- Maximum Load (kN)
- System automatically calculates strength (MPa)

**For Other Tests:**
- Enter result value
- Enter unit
- Add estimated time

#### 5. Upload Raw Data Files / رفع ملفات البيانات الخام

1. Click on the upload area or drag files
2. Supported formats: PDF, CSV, Excel (.xlsx), JPG, PNG
3. Upload multiple files if needed
4. These files are preserved for ISO 17025 compliance

#### 6. Add Observations / إضافة الملاحظات

Enter any observations or notes about the test execution.

أدخل أي ملاحظات حول تنفيذ الاختبار.

#### 7. Finish Testing / إنهاء الاختبار

1. Review all entered data
2. Click "✅ Finish Testing / إنهاء الاختبارات"
3. The test is submitted for manager approval

### Tips / نصائح

- ✅ Always click "Start Test" before entering data
- ✅ Enter accurate measurements
- ✅ Upload all raw data files (Excel sheets, photos, etc.)
- ✅ Add detailed observations for unusual results
- ✅ Double-check calculations before submitting

---

## 👔 Manager Guide / دليل المدير

### Role: Approval, Archiving & Reporting / الدور: الاعتماد والأرشفة والتقارير

As a Manager, you approve test results, generate reports, and archive samples.

كمدير، تقوم باعتماد نتائج الاختبارات وإنشاء التقارير وأرشفة العينات.

### Step-by-Step Process / العملية خطوة بخطوة

#### 1. Review Pending Approvals / مراجعة الاعتمادات المعلقة

1. Go to "Pending Approval / في انتظار الاعتماد" tab
2. Review the list of submitted test results
3. Click on a test to expand details

#### 2. Approve or Reject Test Results / اعتماد أو رفض نتائج الاختبارات

1. Review all test information:
   - Sample details
   - Test method
   - Result value and unit
   - Observations
   - Attached files
2. Select decision: "Approve / اعتماد" or "Reject / رفض"
3. Add approval notes or rejection reason
4. Click "✅ Submit Decision / إرسال القرار"

**If Approved:**
- Test status changes to "Approved"
- Sample can be archived when all tests are approved

**If Rejected:**
- Test status changes to "Rejected"
- Test is sent back to lab technician for correction
- Rejection reason is logged

#### 3. Generate Reports / إنشاء التقارير

1. Go to "Reports / التقارير" tab
2. Select filters:
   - Project (or "All")
   - Start Date
   - End Date
3. Click "📊 Generate Report / إنشاء التقرير"
4. View results in table format
5. Download as CSV for further analysis

#### 4. Archive Completed Samples / أرشفة العينات المكتملة

1. Go to "Archive / الأرشيف" tab
2. View samples with status "Approved" (all tests completed)
3. Click "🗄️ Archive" button for each sample
4. Archived samples are moved to archive section
5. View archived samples in the bottom section

#### 5. View Analytics / عرض التحليلات

The "Analytics / التحليلات" tab provides:
- Total samples count
- Total tests count
- Approved results count
- Archived samples count
- Tests by material type (bar chart)
- Tests by status (breakdown)

### Tips / نصائح

- ✅ Review attached raw data files before approving
- ✅ Provide clear rejection reasons for learning
- ✅ Generate regular reports for project tracking
- ✅ Archive samples promptly after approval
- ✅ Use analytics to identify bottlenecks

---

## 🔒 Security Best Practices / أفضل ممارسات الأمان

1. **Change Default Passwords** / غير كلمات المرور الافتراضية
   - Change your password immediately after first login
   - Use strong passwords (minimum 8 characters)

2. **Logout After Use** / تسجيل الخروج بعد الاستخدام
   - Always click "Logout / تسجيل الخروج" when finished
   - Especially important on shared computers

3. **Protect Your Credentials** / احمِ بيانات الاعتماد الخاصة بك
   - Never share your username and password
   - Report suspicious activity to administrator

4. **Data Integrity** / سلامة البيانات
   - Enter accurate data
   - Do not modify data after submission (use rejection workflow)
   - Upload original raw data files

---

## ❓ Frequently Asked Questions / الأسئلة الشائعة

### Q1: Can I edit a sample after registration? / هل يمكنني تعديل عينة بعد التسجيل؟

**A:** No, samples cannot be edited after registration to maintain data integrity. If you made an error, contact your supervisor or manager.

**ج:** لا، لا يمكن تعديل العينات بعد التسجيل للحفاظ على سلامة البيانات. إذا ارتكبت خطأ، اتصل بالمشرف أو المدير.

### Q2: What happens if I submit incorrect test results? / ماذا يحدث إذا أرسلت نتائج اختبار غير صحيحة؟

**A:** The manager can reject your results with a reason. The test will return to "In Progress" status, and you can re-enter the correct data.

**ج:** يمكن للمدير رفض نتائجك مع ذكر السبب. سيعود الاختبار إلى حالة "جاري العمل"، ويمكنك إعادة إدخال البيانات الصحيحة.

### Q3: Why can't I see all samples? / لماذا لا أستطيع رؤية جميع العينات؟

**A:** Each role sees only relevant samples:
- Field Tech: Samples you registered
- Supervisor: Pending and assigned samples
- Lab Tech: Tests assigned to you
- Manager: All samples and tests

**ج:** كل دور يرى فقط العينات ذات الصلة:
- الفني الميداني: العينات التي سجلتها
- المشرف: العينات المعلقة والمعينة
- فني المختبر: الاختبارات المعينة لك
- المدير: جميع العينات والاختبارات

### Q4: Can I delete a sample or test? / هل يمكنني حذف عينة أو اختبار؟

**A:** No, the system uses "soft delete" for ISO 17025 compliance. Deleted items are hidden but remain in the database for audit purposes. Contact your administrator if you need to delete something.

**ج:** لا، يستخدم النظام "الحذف المؤقت" للامتثال لـ ISO 17025. العناصر المحذوفة مخفية ولكنها تبقى في قاعدة البيانات لأغراض المراجعة. اتصل بالمسؤول إذا كنت بحاجة لحذف شيء ما.

### Q5: How do I know which tests to assign for a material? / كيف أعرف الاختبارات التي يجب تعيينها لمادة معينة؟

**A:** The system automatically filters tests based on material type. For example:
- Asphalt Binder → Penetration Test (ASTM D5)
- Concrete → Compressive Strength (ASTM C39)
- Soil → Proctor, Atterberg Limits, etc.

**ج:** يقوم النظام تلقائياً بتصفية الاختبارات بناءً على نوع المادة. على سبيل المثال:
- رابط أسفلتي → اختبار الاختراق (ASTM D5)
- خرسانة → مقاومة الضغط (ASTM C39)
- تربة → بروكتور، حدود أتربرج، إلخ.

---

## 📞 Technical Support / الدعم الفني

If you encounter any issues or need assistance:

إذا واجهت أي مشاكل أو كنت بحاجة إلى مساعدة:

1. Check this user guide first
2. Contact your system administrator
3. Report bugs with detailed description

---

## 📚 Additional Resources / موارد إضافية

- **README.md** - Complete system documentation
- **Database Schema** - See database.py for table structures
- **ASTM Standards** - Refer to official ASTM publications for test procedures

---

**© 2024 CE-LIMS. All rights reserved. / جميع الحقوق محفوظة.**
