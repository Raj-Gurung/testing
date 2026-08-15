# Project Progress & Status Log

## Project Summary
**Nexsus Logistics & Warehousing Safety Training Platform** — An enterprise web platform featuring user authentication, mandatory safety knowledge assessments, interactive 3D crane & forklift training simulators built with Three.js, and Django REST Framework API persistence.

---

## Completed Stages (1 through 4)

### Stage 1: Core Project Setup & User Authentication
- **Functionality**:
  - User registration, login, and logout workflows using Django session authentication.
  - User roles (`user`, `admin`) attached via `Profile` model with `OneToOneField` to Django `User` and post-save signal.
  - Server-side route protection and access control.
  - Command line admin seeding script (`seed_admin`).
- **Files Touched/Created**:
  - `Backend/training/models.py`
  - `Backend/training/views.py`
  - `Backend/training/urls.py`
  - `Backend/nexsus_backend/settings.py`
  - `Backend/nexsus_backend/urls.py`
  - `Backend/templates/login.html`
  - `Backend/templates/signup.html`
  - `Backend/templates/home.html`
  - `Backend/templates/about.html`
  - `Backend/templates/contact.html`
  - `Backend/templates/guidelines.html`
  - `Backend/training/management/commands/seed_admin.py`

---

### Stage 2: Training Gating & 3D Machinery Simulators
- **Functionality**:
  - Interactive 3D Overhead Crane Operator and 3D Forklift Operator simulators built with Three.js.
  - Training gating mechanism (`NexsusState` in `main.js`) restricting simulator access until safety guidelines are read and the safety quiz is passed with >60%.
  - Real-time physics, safety warnings, seatbelt interlocks, and objective tracking in simulators.
- **Files Touched/Created**:
  - `Backend/templates/quiz.html`
  - `Backend/templates/crane.html`
  - `Backend/templates/forklift.html`
  - `Frontend/html/quiz.html`
  - `Frontend/html/crane.html`
  - `Frontend/html/forklift.html`
  - `Frontend/html/javascript/main.js`

---

### Stage 3: Quiz Results Database Persistence
- **Functionality**:
  - `QuizResult` database model and DRF serializer `QuizResultSerializer`.
  - `@api_view(['POST'])` authenticated API endpoint `submit_quiz_api`.
  - Wired API route `/api/quiz/submit/` in `training/urls.py`.
  - Updated quiz submit handler to save results via `fetch` POST request with CSRF token while keeping instant `localStorage` updates for local UI state.
- **Files Touched/Created**:
  - `Backend/training/models.py`
  - `Backend/training/serializers.py`
  - `Backend/training/views.py`
  - `Backend/training/urls.py`
  - `Backend/templates/quiz.html`
  - `Frontend/html/javascript/main.js`

---

### Stage 4: Simulation Results Database Persistence
- **Functionality**:
  - `SimulationResult` database model and DRF serializer `SimulationResultSerializer`.
  - `@api_view(['POST'])` authenticated API endpoint `submit_simulation_api`.
  - Wired API route `/api/simulation/submit/` in `training/urls.py`.
  - Registered `QuizResult` and `SimulationResult` models in `training/admin.py`.
  - Updated `finishSim()` in `crane.html` and `finishSession()` in `forklift.html` to post `simulator_type`, `time_taken_seconds`, `score`, and `passed` to the API.
- **Files Touched/Created**:
  - `Backend/training/models.py`
  - `Backend/training/serializers.py`
  - `Backend/training/views.py`
  - `Backend/training/urls.py`
  - `Backend/training/admin.py`
  - `Backend/templates/crane.html`
  - `Backend/templates/forklift.html`
  - `Frontend/html/crane.html`
  - `Frontend/html/forklift.html`
  - `Frontend/html/javascript/main.js`

---

## How to Run the Project

### 1. Start the Development Server
```powershell
cd Backend
python manage.py runserver
```
The server will start at `http://127.0.0.1:8000/`.

### 2. Admin Credentials
- **Username**: `admin`
- **Password**: `admin`
- **Django Admin Interface**: `http://127.0.0.1:8000/admin/`


---

## Stage 5 Specifications (Verbatim Instructions)

```markdown
STAGE 5: Build the admin dashboard.
- Create a custom admin.html page/view, reachable only by users with Profile.role == 'admin' — enforce this server-side.
- Match the site's existing dark theme (reuse CSS variables from quiz.html/style.css) — do NOT use a light theme.
- Layout: a left sidebar with nav items (Dashboard/Trainees, Leaderboard, Log out), and a main content area on the right.
- Main content area, "Trainees" view: a table of all users with columns — username, latest quiz score, quiz pass/fail, crane sim time (if any), forklift sim time (if any), overall status.
- CRUD actions on that table: view full detail, edit a user's record, delete a user (cascade-delete their QuizResult and SimulationResult rows).
- Add filter controls above the table: show all / passed only / failed only, and optionally filter by simulator completion.
- Add a separate "Leaderboard" view/tab: all users ranked by simulation completion time (fastest first), showing username, simulator_type, time, score. Admin-only.
- Keep it clean and functional — no stat cards or activity feeds needed.
```

---

## Known Issues & Unfinished Items
- **None**: System check (`python manage.py check`) passes with 0 issues. Database migrations are fully applied (`0001_initial`). Stages 1 through 4 are fully functional, tested, and persisted end-to-end.
