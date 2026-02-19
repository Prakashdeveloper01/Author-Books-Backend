import os
import time
from collections.abc import Generator
from contextlib import contextmanager
from urllib.parse import quote_plus

from pymysql import OperationalError
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from app.config import CONFIG_SETTINGS


def build_sqlalchemy_database_url_from_settings():
    """
    Build a SQLAlchemy URL based on the provided settings.

    Parameters
    ----------
        CONFIG_SETTINGS (Settings): An instance of the Settings class
        containing the PostgreSQL connection details.

    Returns
    -------
        str: The generated SQLAlchemy URL.
    """
    db_host = CONFIG_SETTINGS.SQL_HOST
    db_port = CONFIG_SETTINGS.SQL_PORT
    db_name = CONFIG_SETTINGS.SQL_DB
    db_user = CONFIG_SETTINGS.SQL_ADMIN_USER
    db_pass = CONFIG_SETTINGS.SQL_ADMIN_PASS
    ssl_ca_value = CONFIG_SETTINGS.SQL_SSL_CA
    encoded_password = quote_plus(db_pass)
    if not db_pass:
        database_url = f"mysql+pymysql://{db_user}@{db_host}:{db_port}/{db_name}"
    else:
        database_url = f"mysql+pymysql://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}"
    connect_args: dict = {}

    if ssl_ca_value:
        connect_args["ssl"] = {"ca": ssl_ca_value, "check_hostname": False}

    return database_url, connect_args



SQLALCHEMY_DATABASE_URL,CONNECT_ARGS = build_sqlalchemy_database_url_from_settings()
_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=CONNECT_ARGS,
    future=True,
    pool_recycle=3600,
)
@event.listens_for(_engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    context._query_start_time = time.perf_counter()  # start timer

    # print("\n===== SQL START =====")
    # print("STATEMENT:", statement)
    # print("PARAMS:", parameters)
    # print("=====================\n")


@event.listens_for(_engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = (time.perf_counter() - context._query_start_time) * 1000  # ms

    # print("\n===== SQL END =====")
    # print("TIME (ms):", round(total, 2))
    # print("===================\n")
_session_local = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


def get_db() -> Generator[Session, None, None]:
    """
    Get the database session.

    Returns
    -------
        db: The database session.

    Raises
    ------
        OperationalError: If an error occurs while accessing the database.
    """
    db = _session_local()
    try:
        yield db
    except OperationalError as e:
        error_message = f"An error occurred while getting the database session. Error: {e!s}"
        raise  # Re-raise the exception for proper error handling outside the context manager
    finally:
        db.close()


@contextmanager
def get_ctx_db() -> Generator[Session, None, None]:
    """Get the database session within a context manager."""
    db = _session_local()  # Assuming _session_local() creates a new session
    try:
        yield db
    except Exception as e:
        raise  # Re-raise the exception for proper error handling outside the context manager
    finally:
        db.close()  # Close the database session
