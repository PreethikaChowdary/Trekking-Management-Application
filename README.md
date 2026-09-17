#  Trekking Management Application

A full-stack **Trekking Management System** designed to manage treks, trekkers, staff, bookings, and administrative operations through a role-based web application.

The application provides separate dashboards and functionality for **Admins, Trekking Staff, and Trekkers**, with secure authentication, trek management, booking management, analytics, and automated email notifications.

---

##  Features

###  Trekker

* Create a new account and log in securely
* Browse available treks
* Filter treks by:

  * Location
  * Difficulty
  * Duration
* View trek details
* Book available treks
* View booking history
* Cancel active bookings
* View and update profile information
* Receive trek reminder notifications
* Export booking history

###  Staff

* Staff-specific dashboard
* View assigned treks
* View registered participants
* Update available trek slots
* Update trek status
* Mark treks as:

  * Open
  * Closed
  * Completed
* Automatically mark active bookings as completed when a trek is completed

###  Admin

* Admin dashboard with key statistics
* Create, update, and delete treks
* Manage trekking staff
* Assign staff members to treks
* Manage registered trekkers
* Activate/deactivate user accounts
* View and manage bookings
* Search users, staff, and treks
* View trekking statistics and analytics
* Monitor:

  * Total treks
  * Open treks
  * Completed treks
  * Total users
  * Total staff
  * Total bookings
  * Trek difficulty distribution
  * Trek status distribution
  * Popular treks

###  Automated Tasks

The application uses **Celery and Redis** for background jobs.

* Daily trek reminder emails
* Monthly trekking activity reports
* Booking history CSV export and email notification
* Scheduled tasks configured for the `Asia/Kolkata` timezone

---

##  Tech Stack

### Frontend

* **Vue.js 3**
* **Vue Router**
* **Axios**
* **Bootstrap 5**
* **Chart.js**
* **Vite**

### Backend

* **Python**
* **Flask**
* **Flask-SQLAlchemy**
* **Flask-JWT-Extended**
* **Flask-CORS**
* **Flask-Caching**
* **Flask-Mail**
* **Celery**
* **Redis**

### Database

* **SQLite**

### Authentication

* JWT-based authentication
* Role-based authorization
* Password hashing using Werkzeug

---

##  Project Architecture

```text
trekking-management-application/
│
├── backend/
│   ├── app.py
│   ├── create_db.py
│   ├── extensions.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── trek.py
│   │   ├── booking.py
│   │   └── staff_profile.py
│   │
│   ├── routes/
│   │   ├── auth.py
│   │   ├── admin.py
│   │   ├── staff.py
│   │   └── user.py
│   │
│   └── tasks/
│       ├── __init__.py
│       └── jobs.py
│
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   │
│   ├── public/
│   │
│   └── src/
│       ├── App.vue
│       ├── api.js
│       ├── main.js
│       ├── router/
│       │
│       ├── components/
│       │   └── Toast.vue
│       │
│       └── views/
│           ├── Landing.vue
│           ├── Login.vue
│           ├── Register.vue
│           │
│           ├── admin/
│           │   ├── Dashboard.vue
│           │   ├── Treks.vue
│           │   ├── Staff.vue
│           │   ├── Users.vue
│           │   ├── Bookings.vue
│           │   └── Stats.vue
│           │
│           ├── staff/
│           │   ├── Dashboard.vue
│           │   └── TrekDetail.vue
│           │
│           └── user/
│               ├── Dashboard.vue
│               ├── Treks.vue
│               ├── Bookings.vue
│               └── Profile.vue
│
└── README.md
```

---

##  User Roles

The system follows a role-based architecture:

```text
                    ┌────────────────────┐
                    │ Trekking Management│
                    │      System        │
                    └─────────┬──────────┘
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
        ┌─────────┐      ┌─────────┐      ┌─────────┐
        │  Admin  │      │  Staff  │      │ Trekker │
        └─────────┘      └─────────┘      └─────────┘
             │                │                │
             ▼                ▼                ▼
        Manage System    Manage Assigned    Book Treks
        & Analytics          Treks          & Bookings
```

---

##  Database Models

### User

Stores information about:

* Name
* Email
* Password
* Role
* Contact information
* Account status
* Account creation date

Supported roles:

```text
admin
staff
trekker
```

### Trek

Stores:

* Trek name
* Location
* Difficulty
* Duration
* Total slots
* Available slots
* Start date
* End date
* Trek status
* Assigned staff member

### Booking

Stores:

* Trekker
* Trek
* Booking date
* Booking status
* Payment status

### Staff Profile

Stores:

* Staff member
* Biography
* Years of experience
* Staff status

---

##  Trek Lifecycle

Treks follow a defined lifecycle:

```text
Pending
   │
   ▼
Approved
   │
   ▼
 Open
   │
   ├──────────────► Closed
   │
   ▼
Completed
```

When a trek is marked as **Completed**, active bookings associated with that trek are automatically marked as completed.

---

##  API Structure

The Flask backend exposes REST API endpoints under `/api`.

### Authentication

```text
POST   /api/auth/register
POST   /api/auth/login
GET    /api/auth/me
```

### Admin

```text
GET    /api/admin/dashboard
GET    /api/admin/stats
GET    /api/admin/public/stats

POST   /api/admin/treks
GET    /api/admin/treks
PUT    /api/admin/treks/<trek_id>
DELETE /api/admin/treks/<trek_id>

POST   /api/admin/staff
GET    /api/admin/staff
DELETE /api/admin/staff/<staff_id>

PUT    /api/admin/treks/<trek_id>/assign-staff

GET    /api/admin/users
PUT    /api/admin/users/<user_id>/deactivate
DELETE /api/admin/users/<user_id>

GET    /api/admin/bookings
GET    /api/admin/search
```

### Staff

```text
GET    /api/staff/dashboard

PUT    /api/staff/treks/<trek_id>
GET    /api/staff/treks/<trek_id>/participants
PUT    /api/staff/treks/<trek_id>/status
```

### Trekker

```text
GET    /api/user/treks

POST   /api/user/bookings
GET    /api/user/bookings

PUT    /api/user/bookings/<booking_id>/cancel
```

---

#  Getting Started

## 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd trekking-management-application
```

---

#  Backend Setup

## 2. Create a Virtual Environment

```bash
cd backend

python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

---

## 3. Install Backend Dependencies

Install the required Python packages:

```bash
pip install flask flask-cors flask-sqlalchemy flask-jwt-extended flask-caching flask-mail celery redis werkzeug
```

---

## 4. Start Redis

Redis is required for caching and Celery background tasks.

Make sure Redis is running locally on:

```text
localhost:6379
```

---

## 5. Initialize the Database

Run:

```bash
python create_db.py
```

This creates the required SQLite database tables.

The development database initialization also creates an admin account.

>  Change the default development admin password before using the application in any real environment.

---

## 6. Start the Flask Backend

From the `backend` directory:

```bash
python app.py
```

The backend will run on:

```text
http://localhost:5000
```

You can verify the API by opening:

```text
http://localhost:5000/
```

Expected response:

```text
Trekking Management App API is running!
```

---

#  Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the Vite development server:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

The Vite development server is configured to proxy `/api` requests to:

```text
http://localhost:5000
```

---

#  Background Workers

Celery is used to execute scheduled background tasks.

Start a Celery worker from the `backend` directory.

### Windows

```bash
celery -A tasks.jobs worker --loglevel=info --pool=solo
```

### Linux/macOS

```bash
celery -A tasks.jobs worker --loglevel=info
```

Start Celery Beat separately for scheduled jobs:

```bash
celery -A tasks.jobs beat --loglevel=info
```

The application currently includes scheduled tasks such as:

```text
Daily trek reminders
        ↓
08:00 AM

Monthly activity report
        ↓
1st day of every month
        ↓
06:00 AM
```

---

#  Environment Variables & Security

Before pushing this project to GitHub, **remove all credentials and secrets from the source code**.

Use environment variables for sensitive configuration such as:

```text
JWT_SECRET_KEY
MAIL_USERNAME
MAIL_PASSWORD
```

For example:

```python
import os

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
```

Create a `.env` file locally:

```env
JWT_SECRET_KEY=your-secret-key
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-app-password
```

Make sure `.env` is included in `.gitignore`.

> **Important:** If credentials have already been committed to Git, simply deleting them from the latest file is not enough. Rotate/revoke the exposed credentials and remove the secrets from Git history before making the repository public.

---

#  Application Modules

### Landing Page

Provides an overview of the trekking platform and publicly available trekking statistics.

### Authentication

Users can register and log in. JWT tokens are stored on the frontend and attached automatically to authenticated API requests.

### Trek Management

Admins can create and manage trekking activities while assigning staff members to specific treks.

### Booking Management

Trekkers can browse available treks and make bookings based on available slots.

### Staff Management

Admins can create staff accounts and assign staff members to treks.

### Analytics Dashboard

The admin dashboard provides statistics related to:

* Treks
* Users
* Staff
* Bookings
* Trek popularity
* Difficulty distribution
* Trek status

### Notifications

Celery and Redis enable scheduled email notifications for upcoming treks and periodic activity reports.

---

#  Future Improvements

Potential improvements include:

* Online payment gateway integration
* PostgreSQL/MySQL support for production
* Docker and Docker Compose setup
* Cloud deployment
* Image uploads for treks
* Advanced search and filtering
* Real-time notifications
* Email verification
* Password reset functionality
* Improved API documentation with Swagger/OpenAPI
* Automated testing
* CI/CD pipeline
* Production-grade secret management

---

#  Project Information

**Project:** Trekking Management Application

**Course:** Modern Application Development II (MAD2)

**Program:** IIT Madras BS Degree

**Type:** Full-Stack Web Application

---

#  Technologies

```text
Frontend
   ├── Vue.js
   ├── Vue Router
   ├── Axios
   ├── Bootstrap
   ├── Chart.js
   └── Vite

Backend
   ├── Flask
   ├── SQLAlchemy
   ├── JWT
   ├── Flask-CORS
   └── Flask-Mail

Database
   └── SQLite

Background Processing
   ├── Redis
   ├── Celery
   └── Celery Beat
```

---

##  Acknowledgements

Built as part of the **IIT Madras BS Degree – Modern Application Development II (MAD2)** project.

