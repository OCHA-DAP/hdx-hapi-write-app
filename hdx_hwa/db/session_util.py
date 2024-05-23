from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from hdx_hwa.config.config import get_config

SESSION = None


def session_creator() -> sessionmaker[Session]:
    engine = create_engine(
        get_config().SQL_ALCHEMY_PSYCOPG2_DB_URI,
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal


def db_session() -> Session:
    global SESSION
    if SESSION is None:
        SessionLocal = session_creator()
        SESSION = SessionLocal()
    return SESSION


def end_session():
    global SESSION
    if SESSION:
        SESSION.rollback()
        SESSION.flush()
        SESSION.close()
    SESSION = None
