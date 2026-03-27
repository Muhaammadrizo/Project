# 🚀 Render Deployment Guide & Troubleshooting

Complete guide to deploy your Django backend to Render.com

---

## ✅ Fixed Issues

### Issue: Pillow Build Failure on Python 3.14
**Error**: `KeyError: '__version__'` during Pillow installation
**Status**: ✅ **FIXED**

**What was changed:**
- Updated `Pillow>=11.0.0` (was 10.3.0)
- Added `runtime.txt` specifying Python 3.11.8
- Updated `render.yaml` to use Python 3.11
- Added WhiteNoise for static files

---

## 🚀 Deploy to Render (Step-by-Step)

### Step 1: Connect GitHub Repository
1. Push your code to GitHub
   ```bash
   git add .
   git commit -m "Django backend with Render config"
   git push origin main
   ```

2. Go to [render.com](https://render.com)
3. Click "New +" → "Web Service"
4. Connect your GitHub account
5. Select your repository

### Step 2: Configure Service

1. **Service Settings**
   - Name: `catalog-backend` (or your choice)
   - Environment: `Python 3`
   - Region: `Frankfurt` (or nearest to you)
   - Branch: `main`

2. **Build Command**
   ```
   pip install -r requirements.txt && python manage.py collectstatic --noinput
   ```

3. **Start Command**
   ```
   gunicorn catalog_project.wsgi:application --bind 0.0.0.0:$PORT --workers 3
   ```

### Step 3: Set Environment Variables

Click "Environment" and add:

| Key | Value | Example |
|-----|-------|---------|
| `SECRET_KEY` | Generate random string | `your-secret-key-here` |
| `DEBUG` | `False` | `False` |
| `ALLOWED_HOSTS` | Your domain | `your-app.render.com` |
| `DATABASE_URL` | PostgreSQL URL | (see Step 4) |
| `CORS_ALLOWED_ORIGINS` | Frontend domain | `https://your-frontend.com` |

### Step 4: Database (PostgreSQL)

**Option A: Use Render PostgreSQL**
1. Go to [render.com](https://render.com)
2. Click "New +" → "PostgreSQL"
3. Create database
4. Copy connection string
5. Add as `DATABASE_URL` environment variable

**Option B: Keep SQLite** (not recommended for production)
- SQLite will work but will reset on each deploy

### Step 5: Deploy

1. Click "Create Web Service"
2. Render will build and deploy automatically
3. Monitor the build logs
4. Once deployed, you'll get a URL like: `https://catalog-backend.render.com`

### Step 6: Initialize Database

After first deploy, run:
```bash
# SSH into Render console
python manage.py migrate
python manage.py createsuperuser
```

Or use Render's Shell feature in dashboard.

---

## ✅ Verification Checklist

After deployment:

- [ ] Access admin: `https://your-app.render.com/admin`
- [ ] Get products: `https://your-app.render.com/api/products/`
- [ ] API docs respond
- [ ] Can upload images
- [ ] Can create leads
- [ ] Database is connected
- [ ] Static files load

---

## 📝 What We Fixed

### 1. **Python Compatibility**
   - ❌ Python 3.14.3 (not stable)
   - ✅ Python 3.11.8 (stable & recommended)

### 2. **Pillow Issue**
   - ❌ Pillow==10.3.0 (incompatible with 3.14)
   - ✅ Pillow>=11.0.0 (compatible)

### 3. **Production Dependencies**
   - ✅ Added `gunicorn` (production server)
   - ✅ Added `whitenoise` (static files)
   - ✅ Added `psycopg2-binary` (PostgreSQL)

### 4. **Configuration**
   - ✅ Created `render.yaml` (Render-specific config)
   - ✅ Created `Procfile` (server process)
   - ✅ Created `runtime.txt` (Python version)
   - ✅ Updated `settings.py` (production security)

---

## 🐛 Troubleshooting

### Build Fails: "No module named 'django'"
**Solution:**
```bash
# In build command, run:
pip install --upgrade pip
pip install -r requirements.txt
```

### 404 Static Files
**Solution:**
1. Ensure `whitenoise` is installed
2. Run `python manage.py collectstatic` locally to test
3. Check `STATICFILES_STORAGE` in settings.py

### Database Connection Error
**Solution:**
1. Check `DATABASE_URL` is set correctly
2. Run migrations: `python manage.py migrate`
3. Verify PostgreSQL is ready (may take time)

### Admin not working after deploy
**Solution:**
1. Create superuser: `python manage.py createsuperuser`
2. Or use Render Shell to SSH and run commands

### CORS errors from frontend
**Solution:**
1. Add frontend URL to `CORS_ALLOWED_ORIGINS` env var
2. Format: `https://frontend-domain.com` (with https)
3. Separate multiple URLs with commas

---

## 🔄 Deployment Workflow

### First Deploy (Full Setup)
1. Push to GitHub
2. Create Render service
3. Set environment variables
4. Deploy (automatic)
5. Run migrations
6. Create superuser

### Subsequent Deploys (Updates)
1. Make changes locally
2. Push to GitHub: `git push origin main`
3. Render automatically redeploys
4. No manual steps needed

---

## 📊 Environment Variables Explained

### Required
```
SECRET_KEY        # Django secret (use strong random string)
DEBUG             # Set to False in production
ALLOWED_HOSTS     # Comma-separated list: your-app.render.com,www.your-app.com
```

### Database (if using PostgreSQL)
```
DATABASE_URL      # postgresql://user:password@host/database
```

### Frontend Integration
```
CORS_ALLOWED_ORIGINS  # https://your-frontend.com,https://www.your-frontend.com
```

### Optional
```
STATIC_ROOT       # /var/task/staticfiles (Render specific)
MEDIA_ROOT        # /var/task/media (Render specific)
```

---

## 🎯 Common Deployment Scenarios

### Scenario 1: Django + React Frontend
1. Deploy backend to Render
2. Deploy React to Render (or Netlify/Vercel)
3. Update `CORS_ALLOWED_ORIGINS` with React URL
4. Connect from React to backend API

### Scenario 2: Django + PostgreSQL
1. Create PostgreSQL database on Render
2. Set `DATABASE_URL` env var
3. Run migrations
4. Use admin panel to add data

### Scenario 3: Custom Domain
1. Buy domain (GoDaddy, Namecheap, etc.)
2. Add DNS records pointing to Render
3. Update `ALLOWED_HOSTS` with your domain
4. Enable SSL (automatic)

---

## 🔒 Security Checklist

Before deploying to production:

- [ ] `SECRET_KEY` is strong and random
- [ ] `DEBUG = False`
- [ ] `ALLOWED_HOSTS` set correctly
- [ ] `CORS_ALLOWED_ORIGINS` configured
- [ ] SSL/HTTPS enabled (automatic on Render)
- [ ] Database password is strong
- [ ] Admin user created
- [ ] Backups configured

---

## 📚 Useful Render Resources

- [Render Docs](https://render.com/docs)
- [Django on Render](https://render.com/docs/deploy-django)
- [Environment Variables](https://render.com/docs/environment-variables)
- [Database Connections](https://render.com/docs/databases)

---

## 🎬 Next Steps After Deploy

1. **Test API**
   ```bash
   curl https://your-app.render.com/api/products/
   ```

2. **Create Admin**
   - Access: https://your-app.render.com/admin
   - Use superuser credentials

3. **Add Products**
   - Use admin panel
   - Or create via API

4. **Connect Frontend**
   - Point to: https://your-app.render.com/api

5. **Monitor**
   - Check Render dashboard regularly
   - Review logs for errors

---

## 💰 Cost on Render

| Service | Free Plan | Paid Plan |
|---------|-----------|-----------|
| Web Service | 0.50 USD/month (with auto-sleep) | 7 USD/month+ |
| PostgreSQL | 15 GB free | 0.25/GB after free tier |
| Status | Great for dev/test | Good for production |

---

## 🎉 Success Indicators

After deployment:

✅ Backend running: `https://your-app.render.com`
✅ Admin accessible: Login with superuser
✅ API working: `/api/products/` returns JSON
✅ Database connected: Can view products
✅ Images upload: Can add products with images
✅ CORS working: Frontend can connect

---

## 📞 Deployment Support

### If Build Fails:
1. Check build logs in Render dashboard
2. Read error message carefully
3. Reference troubleshooting section above

### If App Crashes After Deploy:
1. Check "Logs" tab in Render
2. Search for error messages
3. Run migrations if needed

### If Frontend Can't Connect:
1. Check CORS_ALLOWED_ORIGINS
2. Verify frontend is calling correct URL
3. Check browser console for errors

---

## ✅ Files Updated for Deployment

| File | Change | Purpose |
|------|--------|---------|
| `requirements.txt` | Updated Pillow to 11.0.0+ | Fix build error |
| `settings.py` | Added production settings | Security & WhiteNoise |
| `runtime.txt` | Specify Python 3.11.8 | Compatibility |
| `render.yaml` | Added Render config | Render deployment |
| `Procfile` | Added Gunicorn config | Process management |

---

**Status: ✅ Ready for Production Deployment**

**Your next step: Push to GitHub and deploy on Render!**
