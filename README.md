# Mini-grup_14

## Setup Instructions

### 1. Prerequisites
- Python 3.10+
- pip

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your configuration (optional for local development)
# Default settings in .env work for local SQLite development
```

### 6. Run Migrations
```bash
cd src
python manage.py migrate
```

### 7. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 8. Run Development Server
```bash
cd src
python manage.py runserver
```

**Quick Start (Windows):**
```bash
run_server.bat
```

**Quick Start (macOS/Linux):**
```bash
./run_server.sh
```

The server will be available at `http://127.0.0.1:8000`

## Docker Setup

If you prefer to use Docker:

```bash
docker-compose up -d
```

## Environment Variables

All configuration is managed through environment variables defined in `.env`. See `.env.example` for all available options.

Key variables:
- `SECRET_KEY` - Django secret key (change in production)
- `DEBUG` - Enable debug mode (set to `False` in production)
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts
- `DATABASE_URL` - Database connection URL (SQLite or PostgreSQL)
- `CORS_ALLOWED_ORIGINS` - Allowed CORS origins
- `CSRF_TRUSTED_ORIGINS` - Trusted CSRF origins
- `EMAIL_HOST` - SMTP server for email
   