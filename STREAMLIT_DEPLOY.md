# 🚀 Deploy CE-LIMS to Streamlit Cloud / نشر CE-LIMS على Streamlit Cloud

## ✅ Quick Deployment Guide / دليل النشر السريع

Follow these simple steps to deploy CE-LIMS permanently on Streamlit Cloud for **FREE**!

اتبع هذه الخطوات البسيطة لنشر CE-LIMS بشكل دائم على Streamlit Cloud **مجاناً**!

---

## 📋 Prerequisites / المتطلبات

- ✅ GitHub account (already created)
- ✅ Repository is public (already done)
- ✅ All files are ready (already pushed)

---

## 🎯 Step-by-Step Deployment / خطوات النشر

### Step 1: Go to Streamlit Cloud / الخطوة 1: الذهاب إلى Streamlit Cloud

1. Open your browser / افتح المتصفح
2. Go to: **https://share.streamlit.io/**
3. Click **"Sign up"** or **"Sign in"** / انقر على "Sign up" أو "Sign in"

### Step 2: Sign in with GitHub / الخطوة 2: تسجيل الدخول بـ GitHub

1. Click **"Continue with GitHub"** / انقر على "Continue with GitHub"
2. Authorize Streamlit Cloud to access your GitHub account
3. Grant access to the repository

### Step 3: Create New App / الخطوة 3: إنشاء تطبيق جديد

1. Click **"New app"** button / انقر على زر "New app"
2. You'll see a form with three fields:

### Step 4: Configure Deployment / الخطوة 4: تكوين النشر

Fill in the following information:

| Field | Value |
|-------|-------|
| **Repository** | `Mohamed742406/ce-lims` |
| **Branch** | `main` |
| **Main file path** | `app.py` |

### Step 5: Advanced Settings (Optional) / الخطوة 5: الإعدادات المتقدمة (اختياري)

Click **"Advanced settings"** if you want to:
- Change the app URL
- Set Python version (already set to 3.11 in runtime.txt)
- Add secrets (not needed for this app)

### Step 6: Deploy! / الخطوة 6: النشر!

1. Click **"Deploy!"** button / انقر على زر "Deploy!"
2. Wait 2-5 minutes for deployment
3. You'll see the build logs in real-time

---

## 🎉 Your App is Live! / تطبيقك الآن مباشر!

Once deployment is complete, you'll get a URL like:

```
https://ce-lims-[random-id].streamlit.app
```

Or you can customize it to:

```
https://ce-lims.streamlit.app
```

---

## 🔗 Access Your App / الوصول إلى تطبيقك

### Public URL / الرابط العام

Your app will be accessible at the URL provided by Streamlit Cloud.

سيكون تطبيقك متاحاً على الرابط المقدم من Streamlit Cloud.

### Share with Users / مشاركة مع المستخدمين

Simply share the URL with your team members!

ببساطة شارك الرابط مع أعضاء فريقك!

---

## 🔑 Login Credentials / بيانات الدخول

**Default users / المستخدمون الافتراضيون:**

| Role | Username | Password |
|------|----------|----------|
| Field Tech | `ahmed` | `123456` |
| Supervisor | `sara` | `123456` |
| Lab Tech | `omar` | `123456` |
| Manager | `fatima` | `123456` |

⚠️ **IMPORTANT:** Change these passwords immediately after first login!

⚠️ **مهم:** قم بتغيير كلمات المرور هذه فوراً بعد أول تسجيل دخول!

---

## 🔄 Automatic Updates / التحديثات التلقائية

Any changes you push to GitHub will **automatically** update your Streamlit Cloud app!

أي تغييرات ترفعها إلى GitHub ستحدث تطبيق Streamlit Cloud **تلقائياً**!

```bash
# Make changes to your code
cd ce-lims
nano app.py

# Commit and push
git add .
git commit -m "Update feature"
git push origin main

# App will auto-update in 1-2 minutes!
```

---

## 📊 Monitoring Your App / مراقبة تطبيقك

### View Logs / عرض السجلات

1. Go to **https://share.streamlit.io/**
2. Click on your app
3. Click **"Manage app"**
4. View **"Logs"** tab

### View Analytics / عرض التحليلات

1. In the app management page
2. Click **"Analytics"** tab
3. See:
   - Number of visitors
   - Usage statistics
   - Performance metrics

---

## 🛠️ Troubleshooting / استكشاف الأخطاء

### Issue 1: App Won't Start / المشكلة 1: التطبيق لا يبدأ

**Solution:**
- Check the logs in Streamlit Cloud dashboard
- Verify all dependencies are in `requirements.txt`
- Ensure `app.py` is in the root directory

### Issue 2: Database Not Found / المشكلة 2: قاعدة البيانات غير موجودة

**Solution:**
The database is included in the repository and will be deployed automatically.

قاعدة البيانات مضمنة في المستودع وسيتم نشرها تلقائياً.

### Issue 3: Slow Performance / المشكلة 3: أداء بطيء

**Solution:**
- Streamlit Cloud free tier has resource limits
- Consider upgrading to paid tier for better performance
- Or deploy to a VPS (see DEPLOYMENT.md)

---

## 💰 Pricing / الأسعار

### Free Tier (Current) / الطبقة المجانية (الحالية)

✅ **FREE forever for public apps!**
- 1 GB RAM
- 1 CPU core
- Unlimited users
- Unlimited views
- Community support

مجاني للأبد للتطبيقات العامة!

### Paid Tiers / الطبقات المدفوعة

If you need more resources:
- **Starter:** $20/month (private apps, more resources)
- **Team:** $250/month (team collaboration)
- **Enterprise:** Custom pricing

---

## 🔒 Making Your App Private / جعل تطبيقك خاصاً

If you want to make the app private (paid feature):

1. Go to **https://share.streamlit.io/**
2. Click on your app
3. Click **"Settings"**
4. Under **"Sharing"**, select **"Private"**
5. Add email addresses of allowed users

---

## 📱 Custom Domain / نطاق مخصص

To use your own domain (e.g., lims.yourcompany.com):

1. Upgrade to paid tier
2. Go to app settings
3. Add custom domain
4. Update DNS records as instructed

---

## 🎯 Alternative: Deploy to Render.com / البديل: النشر على Render.com

If you prefer Render.com (also free):

1. Go to **https://render.com/**
2. Sign up with GitHub
3. Click **"New +"** → **"Web Service"**
4. Select `Mohamed742406/ce-lims`
5. Configure:
   - **Name:** `ce-lims`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
6. Click **"Create Web Service"**

---

## 📞 Need Help? / تحتاج مساعدة؟

### Streamlit Community / مجتمع Streamlit

- **Forum:** https://discuss.streamlit.io/
- **Documentation:** https://docs.streamlit.io/
- **GitHub:** https://github.com/streamlit/streamlit

### CE-LIMS Documentation / توثيق CE-LIMS

- **README.md** - Complete system documentation
- **USER_GUIDE.md** - User guide for all roles
- **DEPLOYMENT.md** - Full deployment guide

---

## ✅ Deployment Checklist / قائمة النشر

Before going live, ensure:

- [ ] Repository is public on GitHub
- [ ] All files are committed and pushed
- [ ] Database is included (ce_lims.db)
- [ ] requirements.txt is up to date
- [ ] app.py is in root directory
- [ ] Streamlit Cloud account is created
- [ ] App is deployed and running
- [ ] All 4 user roles tested
- [ ] Default passwords documented
- [ ] Users are trained

---

## 🎉 Congratulations! / تهانينا!

Your CE-LIMS is now **permanently deployed** and accessible from anywhere in the world!

نظام CE-LIMS الخاص بك الآن **منشور بشكل دائم** ويمكن الوصول إليه من أي مكان في العالم!

### Share Your Success! / شارك نجاحك!

Share your deployment URL with:
- Team members
- Stakeholders
- Laboratory staff
- Project managers

---

**© 2024 CE-LIMS. All rights reserved. / جميع الحقوق محفوظة.**

**Deployed with ❤️ on Streamlit Cloud**  
**منشور بـ ❤️ على Streamlit Cloud**
