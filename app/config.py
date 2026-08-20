"""
Configuration Module for Student Academic Performance Analytics Platform.
Loads environment variables and sets up application configurations.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directory definition
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file
dotenv_path = BASE_DIR / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path)


class Config:
    """Base application configuration class."""
    SECRET_KEY = os.getenv("SECRET_KEY", "prod-default-secure-key-2026-dash-app")
    
    # Database configuration
    # Default to PostgreSQL, with flexible SQLite fallback for offline development
    DATABASE_URL = os.getenv(
        "DATABASE_URL", 
        f"sqlite:///{BASE_DIR / 'data' / 'student_tracker.db'}"
    )
    # Convert postgres:// to postgresql:// if needed for newer SQLAlchemy versions
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 3600,
    }

    # Flask Server & Networking
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8050))
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

    # ML Model directory
    MODEL_DIR = BASE_DIR / os.getenv("MODEL_DIR", "app/ml_models/models")
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    # Flask-Mail Configurations
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() in ("true", "1", "t")
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False").lower() in ("true", "1", "t")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "academic-alerts@university.edu")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "academic-alerts@university.edu")

    # Grading System Constants
    GRADE_POINTS = {
        "O": 10.0,
        "A+": 9.0,
        "A": 8.0,
        "B+": 7.0,
        "B": 6.0,
        "C": 5.0,
        "P": 4.0,
        "F": 0.0,
    }

    # Department List
    DEPARTMENTS = ["Computer Science", "Electronics & Comm", "Mechanical Eng", "Civil Eng"]
