import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./app.db"
)

# Render and other providers often expose a generic PostgreSQL URL.
# Specifying psycopg explicitly makes the selected driver predictable.
for postgres_prefix in ("postgresql://", "postgres://"):
    if DATABASE_URL.startswith(postgres_prefix):
        DATABASE_URL = DATABASE_URL.replace(
            postgres_prefix,
            "postgresql+psycopg://",
            1
        )
        break

engine_options = {
    "pool_pre_ping": True
}

if DATABASE_URL.startswith("sqlite"):
    engine_options["connect_args"] = {
        "check_same_thread": False
    }
else:
    engine_options["pool_recycle"] = 300

engine = create_engine(DATABASE_URL, **engine_options)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
