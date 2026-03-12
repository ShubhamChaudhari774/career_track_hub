# Career Track Hub

A full-stack Django web application for managing internship and job applications. Built by **Shubham Chaudhari** as a term project.

---

## Features

- **User Authentication** — Register, login, logout with per-user data isolation
- **Add Applications** — Company, position, job type, location, salary, deadline, recruiter info
- **Track Status** — 10 status stages from Applied → Offer Accepted
- **Priority Flags** — High / Medium / Low priority with visual indicators
- **Dashboard** — Live stats: total apps, active pipeline, offer count, response rate, upcoming interviews
- **Search** — Full-text search by company, title, notes + filter by status/type/location
- **Sort & Filter** — Filter by any combination of status, job type, work location
- **Interview Tracking** — Log next interview date/time, surfaced on dashboard
- **Recruiter Contact** — Store name, email, phone with mailto link
- **Admin Panel** — Django admin for full database management

---

## Project Structure

```
career_track_hub/
├── career_track_hub/       # Django project config
│   ├── settings.py         # App settings
│   ├── urls.py             # URL routing
│   └── wsgi.py             # WSGI entrypoint
├── tracker/                # Main application
│   ├── models.py           # Application database model
│   ├── views.py            # All view logic
│   ├── forms.py            # Django forms (register, application, search)
│   ├── admin.py            # Admin panel config
│   ├── migrations/         # Database migrations
│   ├── templates/tracker/  # All HTML templates
│   └── static/tracker/     # CSS & JavaScript
├── templates/              # Global templates (login, register, base)
├── manage.py
├── requirements.txt
├── Procfile                # For cloud deployment
└── README.md
```

---

## Local Setup (Step-by-Step)

### Prerequisites
- Python 3.10+
- pip

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/career-track-hub.git
cd career-track-hub
```

### 2. Create & Activate Virtual Environment
```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations
```bash
python manage.py migrate
```

### 5. Create a Superuser (Admin)
```bash
python manage.py createsuperuser
```
Follow the prompts to set username, email, and password.

### 6. Collect Static Files (optional for dev)
```bash
python manage.py collectstatic
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

Open your browser to: **http://127.0.0.1:8000/**

---

## 📱 Pages & URLs

| URL | Page |
|-----|------|
| `/` | Landing page |
| `/register/` | Create account |
| `/login/` | Sign in |
| `/dashboard/` | Main dashboard |
| `/applications/` | All applications list |
| `/applications/add/` | Add new application |
| `/applications/<id>/` | Application detail |
| `/applications/<id>/edit/` | Edit application |
| `/applications/<id>/delete/` | Delete application |
| `/search/` | Search & filter |
| `/admin/` | Django admin panel |

---

## ☁️ Deployment Guide

### Option A — AWS Elastic Beanstalk

**Prerequisites:** AWS CLI installed, EB CLI installed (`pip install awsebcli`)

```bash
# 1. Initialize EB application
eb init career-track-hub --platform python-3.11 --region us-east-1

# 2. Create environment
eb create career-track-hub-prod

# 3. Set environment variables (IMPORTANT)
eb setenv SECRET_KEY='your-strong-secret-key-here' \
           DEBUG='False' \
           ALLOWED_HOSTS='.elasticbeanstalk.com'

# 4. Deploy
eb deploy

# 5. Open in browser
eb open
```

**Production settings to update in `settings.py`:**
```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.elasticbeanstalk.com', 'yourdomain.com']
```

---

### Option B — Google Cloud Run (Recommended for free tier)

```bash
# 1. Build and submit Docker image
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/career-track-hub

# 2. Deploy to Cloud Run
gcloud run deploy career-track-hub \
  --image gcr.io/YOUR_PROJECT_ID/career-track-hub \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars SECRET_KEY=your-secret,DEBUG=False
```

**Dockerfile** (create this if deploying to Cloud):
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate
EXPOSE 8080
CMD ["gunicorn", "career_track_hub.wsgi", "--bind", "0.0.0.0:8080"]
```

---

### Option C — Heroku (Easiest)

```bash
# 1. Install Heroku CLI, login
heroku login

# 2. Create app
heroku create career-track-hub-shubham

# 3. Set config vars
heroku config:set SECRET_KEY='your-strong-key'
heroku config:set DEBUG='False'

# 4. Deploy
git push heroku main

# 5. Run migrations on Heroku
heroku run python manage.py migrate

# 6. Create superuser
heroku run python manage.py createsuperuser

# 7. Open
heroku open
```

---

## Production Security Checklist

- [ ] Change `SECRET_KEY` to a long random string (50+ chars)
- [ ] Set `DEBUG = False`
- [ ] Set `ALLOWED_HOSTS` to your actual domain
- [ ] Use PostgreSQL instead of SQLite for production (`pip install psycopg2-binary`)
- [ ] Enable HTTPS (most cloud platforms handle this automatically)
- [ ] Set strong admin password

**Generate a secure SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

---

## Database — Switching to PostgreSQL (Production)

```bash
pip install psycopg2-binary
```

In `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

---

## GitHub Setup

```bash
git init
git add .
git commit -m "Initial commit: Career Track Hub"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/career-track-hub.git
git push -u origin main
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11, Django 4.2 |
| Database | SQLite (dev), PostgreSQL (prod) |
| Frontend | HTML5, CSS3 (custom), Vanilla JS |
| Auth | Django built-in authentication |
| Static Files | WhiteNoise |
| Server | Gunicorn |
| Version Control | Git + GitHub |
| Deployment | AWS EB / Google Cloud Run / Heroku |

---

## Author

**Shubham Chaudhari**  
Career Track Hub — Term Project
