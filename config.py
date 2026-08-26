import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "abdelfatah_secret_key")
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # On Vercel the filesystem is read-only (except /tmp), so a local
    # sqlite file only works for local development. In production set
    # DATABASE_URL to your Supabase connection string
    # (Project Settings -> Database -> Connection string -> URI).
    _database_url = os.getenv(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'database.db')}"
    )

    # SQLAlchemy 1.4+/2.x needs "postgresql://", but Supabase (and most
    # providers) hand out "postgres://" -- normalize it here.
    if _database_url.startswith("postgres://"):
        _database_url = _database_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = _database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
