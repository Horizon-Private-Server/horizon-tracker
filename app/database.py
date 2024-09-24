from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.utils.general import read_environment_variables


CREDENTIALS: dict[str, any] = read_environment_variables()

SQLALCHEMY_DATABASE_URL = f"postgresql://{CREDENTIALS['database_username']}:{CREDENTIALS['database_password']}" \
                          f"@{CREDENTIALS['database_host']}/{CREDENTIALS['database_name']}"
SQLALCHEMY_DATABASE_URL_ASYNC = f"postgresql+asyncpg://{CREDENTIALS['database_username']}:{CREDENTIALS['database_password']}" \
                          f"@{CREDENTIALS['database_host']}/{CREDENTIALS['database_name']}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
engine_async = create_async_engine(SQLALCHEMY_DATABASE_URL_ASYNC)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocalAsync = sessionmaker(
    bind=engine_async,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)


Base = declarative_base()
Base.metadata.create_all(bind=engine)
