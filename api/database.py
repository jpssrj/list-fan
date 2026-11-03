from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool

from api.config import DATABASE_URL

is_sqlite = DATABASE_URL.startswith("sqlite")

if is_sqlite:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    # Para ambientes serverless (Vercel + Neon PostgreSQL), usa NullPool
    # para evitar exaustão de conexões compartilhadas entre instâncias efêmeras.
    connect_args = {}
    if "sslmode" not in DATABASE_URL:
        connect_args["sslmode"] = "require"

    engine = create_engine(
        DATABASE_URL,
        poolclass=NullPool,
        connect_args=connect_args
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
