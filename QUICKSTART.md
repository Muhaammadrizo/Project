# ⚡ Quick Start Guide

Get the backend running in 5 minutes!

## 🚀 5-Minute Setup

### 1. Activate Virtual Environment
```bash
cd c:\Beckend\Project
venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Database
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. Load Sample Data
```bash
python manage.py populate_sample_data
```

### 5. Run Server
```bash
python manage.py runserver
```

✅ **Done!** Server running at http://localhost:8000

---

## 📍 Quick Links

| Link | Purpose |
|------|---------|
| http://localhost:8000/admin | Admin Dashboard |
| http://localhost:8000/api/products/ | Products API |
| http://localhost:8000/api/leads/ | Leads API |
| http://localhost:8000/api/dashboard/ | Dashboard Stats |

---

## 🔑 Key Commands

```bash
# Start server
python manage.py runserver

# Django shell
python manage.py shell

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Run tests
python manage.py test

# Load sample data
python manage.py populate_sample_data
```

---

## 🧪 Test an Endpoint

```bash
# Get all products
curl http://localhost:8000/api/products/

# Submit a lead
curl -X POST http://localhost:8000/api/leads/ \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "phone": "+998901234567",
    "product": 1
  }'

# Get dashboard stats
curl http://localhost:8000/api/dashboard/
```

---

## 📚 Full Documentation

- **Setup:** See [INSTALLATION.md](INSTALLATION.md)
- **API Docs:** See [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **Project Info:** See [README.md](README.md)

---

## ❓ Common Issues

| Issue | Solution |
|-------|----------|
| `virtual environment not activated` | Run `venv\Scripts\activate` |
| `port 8000 already in use` | Run `python manage.py runserver 8080` |
| `ModuleNotFoundError` | Install dependencies: `pip install -r requirements.txt` |
| `database error` | Run migrations: `python manage.py migrate` |

---

**Ready to develop? Start the server and check the admin panel! 🎉**
