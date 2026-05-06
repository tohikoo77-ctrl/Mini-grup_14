# Mini-grup_14

## Setup Instructions

### 1. Prerequisites
- Python 3.10+
- PostgreSQL (optional, SQLite is default)
- pip or pip3

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
# or
source venv/bin/activate  # On macOS/Linux
```

### 3. Install Dependencies
```bash
pip install -r src/requirements.txt
```

### 4. Configure Environment Variables
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your configuration (optional for local development)
# Default settings in .env work for local SQLite development
```

### 5. Run Migrations
```bash
cd src
python manage.py migrate
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
cd src
python manage.py runserver
```

The server will be available at `http://localhost:8000`

## Docker Setup

If you prefer to use Docker:

```bash
docker-compose up -d
```

## Environment Variables

All configuration is managed through environment variables defined in `.env`. See `.env.example` for all available options.

Key variables:
- `DJANGO_DEBUG` - Enable debug mode (set to `False` in production)
- `DJANGO_SECRET_KEY` - Django secret key (change in production)
- `DJANGO_ALLOWED_HOSTS` - Comma-separated list of allowed hosts
- `DB_*` - Database configuration (PostgreSQL)
- `DJANGO_EMAIL_*` - Email service configuration