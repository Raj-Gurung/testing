# Project Progress & Status Log

## Project Summary
**Nexsus Logistics & Warehousing Safety Training Platform** — An enterprise web platform featuring user authentication, mandatory safety knowledge assessments, interactive 3D crane & forklift training simulators built with Three.js, DRF API persistence, a custom Admin Dashboard with Trainees CRUD and Leaderboard views, and full mobile responsive design with touch controls.

---

## Completed Stages (1 through 5 & Quality Improvements)

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

### Stage 5: Custom Dark Admin Dashboard, Trainees CRUD & Leaderboard
- **Functionality**:
  - Custom dark-themed 2-column sidebar layout matching site CSS variables (`admin_dashboard.html`).
  - Server-side role check (`Profile.role == 'admin'`) enforcing 403 Forbidden / redirect for non-admin users across views and API endpoints.
  - Trainees Table: displays username, role, latest quiz score & status, crane sim time, forklift sim time, and overall training status.
  - Interactive Filter Controls: real-time search by username/email, status filter (unlocked/passed/failed/pending), and simulator completion filter.
  - Full Trainees CRUD Actions:
    - View Detail: Modal displaying user's complete history of quiz attempts and simulation runs.
    - Edit User: Modal allowing role changes (`user`/`admin`) and username updates.
    - Delete User: Confirmation modal that deletes the user and automatically cascade-deletes linked `QuizResult` and `SimulationResult` rows.
  - Simulation Leaderboard: Ranked list of users by simulation completion time (fastest first) with simulator type filter buttons (All / Crane / Forklift).
- **Files Touched/Created**:
  - `Backend/templates/admin_dashboard.html`
  - `Backend/training/views.py`
  - `Backend/training/urls.py`
  - `PROGRESS.md`

---

### Quality Improvement: Mobile Responsiveness & Touch Controls
- **Functionality**:
  - **Desktop Preservation Guarantee**: All screen sizes > 880px retain 100% untouched desktop styling, layout, and keyboard controls.
  - **Collapsible Hamburger Navbar**: On mobile screens (`<= 880px`), navbar transforms into a toggle button (`☰` / `✕`) with high z-index overlay (`z-index: 10000`), smooth sublink expansion, and click-outside closing.
  - **Crane Simulator Mobile HUD**: Scoped mobile CSS (`@media (max-width: 880px)`), compact semi-transparent touch pads, and a floating `👁️ Controls` toggle button to minimize HUD overlays and maximize 3D canvas visibility.
  - **Forklift Simulator Touch Overlay**: Complete touch UI for phone/tablet screens (`#mobile-forklift-controls`) including Drive D-Pad (W/A/S/D), Seatbelt Toggle (B), Horn (H), Interact (E), Fork Lift/Lower (Arrows), Mast Tilt (Z/X), and a floating `👁️ Controls` toggle button.
- **Files Touched/Created**:
  - `Frontend/html/css/style.css`
  - `Frontend/html/javascript/main.js`
  - `Backend/templates/crane.html`
  - `Backend/templates/forklift.html`
  - `Frontend/html/crane.html`
  - `Frontend/html/forklift.html`
  - `PROGRESS.md`

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
- **Admin Dashboard**: `http://127.0.0.1:8000/admin-dashboard/`
- **Django Standard Admin Interface**: `http://127.0.0.1:8000/admin/`

---

## Known Issues & Unfinished Items

### ⚠️ WIP — Mobile Responsiveness: Forklift Bug (NOT YET COMMITTED)

**Status**: Work-in-progress. **Not committed or pushed to Git.**

**What works (verified)**:
- Navbar hamburger menu on mobile (`<= 880px`) — fully working.
- Crane simulator mobile HUD (`<= 880px`) — compact controls and `👁️ Controls` toggle verified working.

**What is broken**:
- **Forklift simulator (`forklift.html`) — broken on both desktop AND mobile** due to the mobile touch controls insertion during this session.
- **Error**: `Uncaught TypeError: Cannot set properties of null (setting 'textContent') at updateForklift (forklift.html:1184:31)` — fires on every animation frame inside `animate()`, preventing all forklift movement.
- **Root cause**: The mobile touch overlay HTML (`#mobile-forklift-controls`) was accidentally inserted inside the `#dash` HUD `<div>`, breaking the closing tags and removing `<div id="tilt-indicator">MAST: LEVEL</div>` from the DOM. The JS variable `tiltIndicator = document.getElementById('tilt-indicator')` therefore resolves to `null`, crashing `updateForklift()` on line 1184: `tiltIndicator.textContent = ...`.

**Fix required (next session)**:
1. In `Backend/templates/forklift.html` and `Frontend/html/forklift.html`, inspect lines ~478–483 (around the `#dash` div closing tag).
2. Restore `<div id="tilt-indicator">MAST: LEVEL</div>` inside `#dash`, close all parent divs properly, and place `#mobile-forklift-controls` **outside and after** the `#dash` div.
3. Or alternatively, add a null-check in `updateForklift`: `if (tiltIndicator) tiltIndicator.textContent = ...;` as a defensive fix.
4. Apply the same fix to both `Backend/templates/forklift.html` and `Frontend/html/forklift.html`.
5. Verify both desktop keyboard controls (WASD, B, E, H, Z, X) and mobile touch buttons work correctly after fix.
6. Then commit the full mobile responsiveness work as a completed stage.

