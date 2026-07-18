# Baby Care — Backend

Django REST + Channels backend for **Baby Care**, a smart baby monitoring system with real-time video-based motion detection, audio-based cry detection, sleep tracking, and environmental sensor simulation.

**Live API:** https://baby-care-8ewi.onrender.com
**Frontend repo:** https://github.com/PrakashGrg/baby

## Tech Stack

- **Django 5.0** + **Django REST Framework** — REST API
- **Django Channels 4.1** + **Daphne** — WebSocket support (ASGI)
- **djangorestframework-simplejwt** — JWT authentication
- **OpenCV (headless)** — motion detection via frame differencing
- **PostgreSQL** (production) / **SQLite** (local dev) — via `dj-database-url`
- **Whitenoise** — static file serving in production
- **Deployed on Render** (free tier)

## Architecture