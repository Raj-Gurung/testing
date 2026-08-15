# Nexsus Logistics Backend

Django + DRF Backend for Nexsus Logistics Workplace Health & Safety Training Platform.

## Setup Instructions

### 1. Install Dependencies
Make sure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

### 2. Run Database Migrations
Initialize SQLite3 database and apply model migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Seed Admin User
Create the initial administrator account (`username: admin`, `password: admin`):
```bash
python manage.py seed_admin
```

### 4. Start Development Server
Run the local Django development server:
```bash
python manage.py runserver
```

Access the Django Admin panel at: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
Log in using:
- **Username**: `admin`
- **Password**: `admin`
