import os
from datetime import timedelta


def _database_uri() -> str:
    """Build the SQLAlchemy URI.

    Aiven gives you a `mysql://` URL. SQLAlchemy needs the `pymysql` driver
    named explicitly, and Aiven requires TLS, so we normalize both here.
    Falls back to a local SQLite file when DATABASE_URL isn't set, so the
    app runs out of the box for local development without a real database.
    """
    url = os.environ.get("DATABASE_URL")
    if not url:
        return "sqlite:///dev.db"

    if url.startswith("mysql://"):
        url = url.replace("mysql://", "mysql+pymysql://", 1)

    return url


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")

    SQLALCHEMY_DATABASE_URI = _database_uri()
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True, "pool_recycle": 280}
    if SQLALCHEMY_DATABASE_URI.startswith("mysql+pymysql://"):
        SQLALCHEMY_ENGINE_OPTIONS["connect_args"] = {"ssl": {"ssl_mode": "REQUIRED"}}
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-jwt-secret-change-me")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)

    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD_HASH = os.environ.get("ADMIN_PASSWORD_HASH", "")

    CLOUDINARY_CLOUD_NAME = os.environ.get("CLOUDINARY_CLOUD_NAME", "")
    CLOUDINARY_API_KEY = os.environ.get("CLOUDINARY_API_KEY", "")
    CLOUDINARY_API_SECRET = os.environ.get("CLOUDINARY_API_SECRET", "")

    FRONTEND_ORIGINS = [
        origin.strip()
        for origin in os.environ.get("FRONTEND_ORIGINS", "http://localhost:5173").split(",")
        if origin.strip()
    ]
