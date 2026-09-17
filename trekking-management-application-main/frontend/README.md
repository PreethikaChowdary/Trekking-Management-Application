# Trekking Management Application - V2

A full-stack web application for managing trekking activities built with Flask and Vue.js.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Flask, SQLAlchemy, SQLite |
| Authentication | Flask-JWT-Extended |
| Caching | Redis, Flask-Caching |
| Background Jobs | Celery, Redis |
| Email | Flask-Mail, Gmail SMTP |
| Frontend | Vue.js 3, Vite |
| UI | Bootstrap 5, Chart.js |

---

## Project Structure
trekking-management-application/
├── backend/
│   ├── app.py              - Flask app factory
│   ├── extensions.py       - db and cache instances
│   ├── create_db.py        - DB creation and admin seed
│   ├── celery_app.py       - Celery configuration
│   ├── requirements.txt    - Python dependencies
│   ├── models/             - SQLAlchemy models
│   │   ├── user.py
│   │   ├── trek.py
│   │   ├── booking.py
│   │   └── staff_profile.py
│   ├── routes/             - Flask Blueprints
│   │   ├── auth.py
│   │   ├── admin.py
│   │   ├── staff.py
│   │   └── user.py
│   └── tasks/
│       └── jobs.py         - Celery background tasks
└── frontend/
├── index.html
├── vite.config.js
├── package.json
└── src/
├── main.js
├── App.vue
├── api.js
├── router/
│   └── index.js
├── components/
│   └── Toast.vue
└── views/
├── Landing.vue
├── Login.vue
├── Register.vue
├── admin/
│   ├── Dashboard.vue
│   ├── Treks.vue
│   ├── Staff.vue
│   ├── Users.vue
│   ├── Bookings.vue
│   └── Stats.vue
├── staff/
│   ├── Dashboard.vue
│   └── TrekDetail.vue
└── user/
├── Dashboard.vue
├── Treks.vue
├── Bookings.vue
└── Profile.vue

---

## Prerequisites

- Python (Anaconda recommended)
- Node.js and npm
- Redis for Windows

---

## How to Run

### First Time Setup Only
cd backend
pip install -r requirements.txt
python create_db.py

### Every Time - Open 4 Terminals

Terminal 1 - Redis
& "C:\Program Files\Redis\redis-server.exe" "C:\Program Files\Redis\redis.windows.conf"

Terminal 2 - Flask Backend
cd backend
python app.py

Terminal 3 - Celery Worker
cd backend
celery -A tasks.jobs.celery worker --loglevel=info --pool=solo

Terminal 4 - Vue Frontend
cd frontend
npm install
npm run dev

### Open Browser
http://localhost:5173

---

## Default Login Credentials

Admin
Email:    admin@trekking.com
Password: admin123

Trek Staff
Created by Admin from the Admin Dashboard
Login only - no self registration allowed

Trekker
Self register at http://localhost:5173/register

---

## API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | /api/auth/register | Register trekker | No |
| POST | /api/auth/login | Login all roles | No |
| GET | /api/admin/dashboard | Admin stats | Admin |
| POST | /api/admin/treks | Create trek | Admin |
| GET | /api/admin/treks | Get all treks | Admin |
| PUT | /api/admin/treks/<id> | Update trek | Admin |
| DELETE | /api/admin/treks/<id> | Delete trek | Admin |
| PUT | /api/admin/treks/<id>/assign-staff | Assign staff | Admin |
| POST | /api/admin/staff | Create staff | Admin |
| GET | /api/admin/staff | Get all staff | Admin |
| DELETE | /api/admin/staff/<id> | Delete staff | Admin |
| GET | /api/admin/users | Get all users | Admin |
| PUT | /api/admin/users/<id>/deactivate | Blacklist user | Admin |
| DELETE | /api/admin/users/<id> | Delete user | Admin |
| GET | /api/admin/bookings | Get all bookings | Admin |
| GET | /api/admin/search | Search | Admin |
| GET | /api/admin/stats | Statistics | Admin |
| GET | /api/admin/public/stats | Public stats | No |
| GET | /api/staff/dashboard | Assigned treks | Staff |
| PUT | /api/staff/treks/<id> | Update slots | Staff |
| PUT | /api/staff/treks/<id>/status | Update status | Staff |
| GET | /api/staff/treks/<id>/participants | Participants | Staff |
| GET | /api/user/treks | Open treks | Trekker |
| GET | /api/user/treks/search | Search treks | Trekker |
| POST | /api/user/bookings | Book trek | Trekker |
| GET | /api/user/bookings | My bookings | Trekker |
| PUT | /api/user/bookings/<id>/cancel | Cancel booking | Trekker |
| POST | /api/user/export-history | Export CSV | Trekker |
| GET | /api/user/profile | Get profile | Trekker |
| PUT | /api/user/profile | Update profile | Trekker |

---

## Background Jobs (Celery)

| Job | Schedule | Description |
|-----|----------|-------------|
| Daily Reminders | Every day 8 AM | Email reminders for upcoming treks |
| Monthly Report | 1st of every month 6 AM | HTML activity report to admin |
| CSV Export | User triggered | Booking history CSV to user email |

---

## Roles

| Role | Access |
|------|--------|
| Admin | Full access - manage treks, staff, users, bookings |
| Trek Staff | Manage assigned treks and participants |
| Trekker | Browse, book and manage own bookings |

---

## Features

- JWT based authentication with role based access control
- Admin dashboard with stats and analytics
- Trek lifecycle management (Pending to Approved to Open to Closed to Completed)
- Booking system with overbooking prevention
- Redis caching for performance
- Celery background jobs for emails
- Chart.js analytics and charts
- Public landing page with live statistics
- Toast notifications
- PWA support (Add to Home Screen)
- Mobile responsive UI
- Earth colour theme