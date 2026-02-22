from collections.abc import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

connect_args: dict = {}
if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    future=True,
    pool_pre_ping=True,  # CW1 polish: avoids weird stale-connection issues if the DB gets reloaded
)

# CW1 polish (actually important for correctness):
# SQLite does NOT enforce foreign keys (and therefore ON DELETE CASCADE) unless this PRAGMA is enabled.
if settings.database_url.startswith("sqlite"):

    @event.listens_for(Engine, "connect")
    def _set_sqlite_pragma(dbapi_connection, _connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
    expire_on_commit=False,  # CW1 polish: lets us return objects after commit without surprise lazy reloads
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    except Exception:
        # CW1 polish: if anything blows up mid-request, don’t leave a half-open transaction hanging
        db.rollback()
        raise
    finally:
        db.close()