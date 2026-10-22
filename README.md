# TradeSwap

TradeSwap is a skill-exchange platform where users can teach skills to each
other instead of exchanging money.

## Architecture

```text
React + TypeScript
        ↓
Django + DRF
        ↓
PostgreSQL
```

Django will communicate with a separate FastAPI service for matching and AI
functionality.

## Getting Started

### Backend

```bash
cd backend
source venv/bin/activate
python manage.py migrate
python manage.py seed_skills
python manage.py runserver
```

The API is available at `http://localhost:8000/api`. Week 1 provides registration, login,
the protected profile endpoint, the shared skills catalogue, and user skill CRUD.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. To point it at another backend, set `VITE_API_URL`.

## Current Status

Day 1:

- Django backend initialized
- DRF configured
- CORS configured for `http://localhost:5173`
- Users and skills apps created
- PostgreSQL configuration prepared
- User, Skill and UserSkill models with Django Admin and a 50-skill seed command
- JWT-based signup/login, protected profile, and teach/learn skill APIs
- React + TypeScript login, signup, and protected profile/skill-management flow
