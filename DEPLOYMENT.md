# CE-LIMS Deployment Guide / دليل نشر CE-LIMS

## 🚀 Deployment Options / خيارات النشر

This guide provides step-by-step instructions for deploying CE-LIMS to various platforms.

يوفر هذا الدليل تعليمات خطوة بخطوة لنشر CE-LIMS على منصات مختلفة.

---

## Option 1: Streamlit Cloud (Recommended) / الخيار 1: Streamlit Cloud (موصى به)

### ✅ Advantages / المميزات
- **Free** for public repositories / مجاني للمستودعات العامة
- **Easy setup** / إعداد سهل
- **Automatic updates** from GitHub / تحديثات تلقائية من GitHub
- **Built-in SSL** / SSL مدمج
- **No server management** / لا حاجة لإدارة الخادم

### 📋 Prerequisites / المتطلبات الأساسية
- GitHub account / حساب GitHub
- Streamlit Cloud account (free) / حساب Streamlit Cloud (مجاني)

### 🔧 Deployment Steps / خطوات النشر

#### 1. Push to GitHub / رفع الكود إلى GitHub

```bash
cd ce-lims
git init
git add .
git commit -m "Initial commit - CE-LIMS v1.0"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ce-lims.git
git push -u origin main
```

#### 2. Deploy to Streamlit Cloud / النشر على Streamlit Cloud

1. Go to **https://share.streamlit.io/**
2. Click **"New app"**
3. Connect your **GitHub account**
4. Select:
   - **Repository:** `YOUR_USERNAME/ce-lims`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Click **"Deploy"**

#### 3. Wait for Deployment / انتظر النشر

- Deployment takes 2-5 minutes
- You'll get a URL like: `https://your-app-name.streamlit.app`

#### 4. Access Your App / الوصول إلى التطبيق

Your app will be live at: `https://[your-app-name].streamlit.app`

---

## Option 2: Render.com (Alternative) / الخيار 2: Render.com (بديل)

### ✅ Advantages / المميزات
- **Free tier available** / طبقة مجانية متاحة
- **Custom domains** / نطاقات مخصصة
- **Automatic SSL** / SSL تلقائي
- **Good performance** / أداء جيد

### 🔧 Deployment Steps / خطوات النشر

#### 1. Create `render.yaml`

Already included in the repository.

#### 2. Deploy to Render

1. Go to **https://render.com/**
2. Sign up / Log in
3. Click **"New +"** → **"Web Service"**
4. Connect your **GitHub repository**
5. Configure:
   - **Name:** `ce-lims`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
6. Click **"Create Web Service"**

---

## Option 3: Railway.app / الخيار 3: Railway.app

### ✅ Advantages / المميزات
- **$5 free credit monthly** / رصيد مجاني 5 دولار شهرياً
- **Easy deployment** / نشر سهل
- **Good for small apps** / جيد للتطبيقات الصغيرة

### 🔧 Deployment Steps / خطوات النشر

1. Go to **https://railway.app/**
2. Sign up with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select your repository
5. Railway will auto-detect Streamlit and deploy

---

## Option 4: Heroku / الخيار 4: Heroku

### 📋 Prerequisites / المتطلبات

Create `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
```

### 🔧 Deployment Steps / خطوات النشر

```bash
heroku login
heroku create ce-lims-app
git push heroku main
heroku open
```

---

## Option 5: Docker Deployment / الخيار 5: النشر باستخدام Docker

### Create `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run / البناء والتشغيل

```bash
# Build image
docker build -t ce-lims .

# Run container
docker run -p 8501:8501 ce-lims

# Access at http://localhost:8501
```

### Deploy to Docker Hub

```bash
docker tag ce-lims YOUR_USERNAME/ce-lims:latest
docker push YOUR_USERNAME/ce-lims:latest
```

---

## Option 6: VPS Deployment (Ubuntu) / الخيار 6: النشر على VPS

### 🔧 Server Setup / إعداد الخادم

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip -y

# 3. Clone repository
git clone https://github.com/YOUR_USERNAME/ce-lims.git
cd ce-lims

# 4. Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# 5. Install dependencies
pip install -r requirements.txt

# 6. Initialize database
python database.py

# 7. Run with systemd (production)
sudo nano /etc/systemd/system/ce-lims.service
```

### Systemd Service File

```ini
[Unit]
Description=CE-LIMS Streamlit Application
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/ce-lims
Environment="PATH=/home/ubuntu/ce-lims/venv/bin"
ExecStart=/home/ubuntu/ce-lims/venv/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

### Start Service / تشغيل الخدمة

```bash
sudo systemctl daemon-reload
sudo systemctl enable ce-lims
sudo systemctl start ce-lims
sudo systemctl status ce-lims
```

### Setup Nginx Reverse Proxy / إعداد Nginx

```bash
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/ce-lims
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/ce-lims /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Setup SSL with Let's Encrypt / إعداد SSL

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

---

## 🔒 Security Considerations / اعتبارات الأمان

### 1. Change Default Passwords / تغيير كلمات المرور الافتراضية

**IMPORTANT:** Before deploying to production, change all default passwords!

```python
# In database.py, update the seed_initial_data() function
# Or use the application to change passwords after first login
```

### 2. Environment Variables / متغيرات البيئة

For production, use environment variables for sensitive data:

```python
import os

DB_PATH = os.getenv('DB_PATH', 'ce_lims.db')
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
```

### 3. Database Backup / النسخ الاحتياطي لقاعدة البيانات

Set up automatic backups:

```bash
# Cron job for daily backup
0 2 * * * cd /home/ubuntu/ce-lims && cp ce_lims.db backups/ce_lims_$(date +\%Y\%m\%d).db
```

### 4. HTTPS Only / HTTPS فقط

Always use HTTPS in production (handled automatically by Streamlit Cloud, Render, etc.)

---

## 📊 Monitoring & Maintenance / المراقبة والصيانة

### Health Check / فحص الصحة

```bash
# Check if app is running
curl http://localhost:8501/_stcore/health

# Check database size
ls -lh ce_lims.db

# Check logs (systemd)
sudo journalctl -u ce-lims -f
```

### Performance Optimization / تحسين الأداء

1. **Database Optimization**
   ```sql
   VACUUM;
   ANALYZE;
   ```

2. **Enable Caching** (already implemented in components)

3. **Limit File Upload Size** (configured in Streamlit)

---

## 🆘 Troubleshooting / استكشاف الأخطاء

### Common Issues / المشاكل الشائعة

#### 1. Database Locked Error

```bash
# Stop all instances
pkill -f streamlit

# Restart
streamlit run app.py
```

#### 2. Port Already in Use

```bash
# Find process using port 8501
lsof -i :8501

# Kill process
kill -9 <PID>
```

#### 3. Module Not Found

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## 📞 Support / الدعم

For deployment issues:
1. Check application logs
2. Verify all dependencies are installed
3. Ensure database is initialized
4. Check file permissions

---

## 🎯 Recommended Deployment / النشر الموصى به

**For Quick Demo:** Streamlit Cloud (Free, Easy)  
**For Production:** VPS with Nginx + SSL (Full Control)  
**For Scalability:** Docker + Kubernetes (Enterprise)

---

## 📝 Post-Deployment Checklist / قائمة ما بعد النشر

- [ ] Change all default passwords
- [ ] Test all user roles
- [ ] Verify file uploads work
- [ ] Test report generation
- [ ] Set up database backups
- [ ] Configure monitoring
- [ ] Update documentation with live URL
- [ ] Train users on the system

---

**© 2024 CE-LIMS. All rights reserved. / جميع الحقوق محفوظة.**
