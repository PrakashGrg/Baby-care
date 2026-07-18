# Baby Care - Backend

Django REST + Channels backend for **Baby Care**, a smart baby monitoring system with real-time video-based motion detection, audio-based cry detection, sleep tracking, and environmental sensor simulation.

**Live API:** https://baby-care-8ewi.onrender.com

**Frontend Repository:** https://github.com/PrakashGrg/baby

---

## Tech Stack

- **Django 5.0** + **Django REST Framework** - REST API
- **Django Channels 4.1** + **Daphne** - WebSocket support (ASGI)
- **djangorestframework-simplejwt** - JWT authentication
- **OpenCV (headless)** - Motion detection using frame differencing
- **PostgreSQL** (production) / **SQLite** (local development) via `dj-database-url`
- **WhiteNoise** - Static file serving in production
- **Render** (Free Tier) - Cloud deployment

---

## Architecture

```
config/             Django project settings, ASGI/WSGI entry points

apps/
├── users/          Custom User model, JWT authentication, push token registration
├── monitoring/     WebSocket consumer - routes video/audio frames and broadcasts alerts
├── detection/      OpenCV motion detector, MotionEvent model
├── audio/          Energy-based cry detector, CryEvent model
├── sensors/        Simulated temperature/humidity, SensorReading model
├── sleep/          Sleep/wake inference from motion history, SleepLog model
├── activity/       Unified daily summary and activity timeline
└── baby/           Baby profile CRUD
```

---

## Real-time Flow

A single WebSocket endpoint

```
/ws/monitor/<room_name>/?token=<jwt>
```

handles the complete real-time monitoring pipeline.

1. The mobile application (Live tab or Child Mode) sends `video_frame` or `audio_chunk` messages.
2. The server performs OpenCV motion detection and energy-based cry detection.
3. When motion or crying is detected:
   - An event is stored in the database.
   - The event is broadcast to all connected clients in the same room.
4. Every 5 seconds, the backend generates and broadcasts a simulated environmental sensor reading.

---

## Local Setup

Clone the repository:

```powershell
git clone https://github.com/PrakashGrg/Baby-care.git
cd Baby-care
```

Create and activate a virtual environment:

```powershell
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create a `.env` file:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

Apply migrations:

```powershell
python manage.py migrate
```

Create an administrator account:

```powershell
python manage.py createsuperuser
```

Start the backend using Daphne:

```powershell
daphne -b 0.0.0.0 -p 8000 config.asgi:application
```

> **Note**
>
> Always start the backend using **Daphne** instead of `python manage.py runserver`, because WebSocket support requires ASGI.

---

## Deployment (Render)

### Build Command

```text
pip install -r requirements.txt
```

### Start Command

```text
python manage.py migrate && python manage.py collectstatic --noinput && daphne -b 0.0.0.0 -p $PORT config.asgi:application
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| SECRET_KEY | Django secret key |
| DEBUG | False |
| ALLOWED_HOSTS | `.onrender.com` |
| DATABASE_URL | Render PostgreSQL connection string |
| PYTHON_VERSION | 3.11.9 |

---

## Known Limitations

- Render free tier spins down after 15 minutes of inactivity. The first request after idle may take 30-60 seconds.
- Render free PostgreSQL databases expire after 30 days unless renewed.
- The project currently uses `InMemoryChannelLayer`, which is suitable only for a single Render instance. Production scaling would require Redis.
- Motion detection and cry detection use heuristic algorithms (frame differencing and RMS volume threshold) rather than machine learning models.

---

## API Overview

| Endpoint | Description |
|----------|-------------|
| `POST /api/auth/register/` | Register a new user |
| `POST /api/auth/login/` | User login |
| `POST /api/auth/login/refresh/` | Refresh JWT access token |
| `GET /api/auth/me/` | Current authenticated user |
| `POST /api/auth/push-token/` | Register Expo push notification token |
| `GET /api/baby/` | List baby profiles |
| `POST /api/baby/` | Create baby profile |
| `GET /api/sensors/history/` | Retrieve sensor history |
| `GET /api/sleep/status/` | Current sleep status |
| `GET /api/sleep/history/` | Sleep history |
| `GET /api/activity/daily-summary/` | Daily activity summary |
| `GET /api/activity/timeline/` | Activity timeline |
| `WS /ws/monitor/<room_name>/?token=<jwt>` | Real-time video, audio, motion, cry detection, and sensor streaming |

---

## Features

- JWT Authentication
- Baby Profile Management
- Real-time WebSocket Communication
- Live Motion Detection
- Cry Detection
- Sleep Tracking
- Simulated Environmental Sensors
- Activity Timeline
- Daily Activity Summary
- Push Token Registration
- PostgreSQL Production Database
- SQLite Local Development Database
- Render Cloud Deployment

---

## Author

**Prakash Gurung**

Final Year Project - Baby Care Smart Monitoring System