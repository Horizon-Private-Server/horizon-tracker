from typing import Dict, Any

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.utils.general import read_environment_variables


CREDENTIALS: Dict[str, Any] = read_environment_variables()

SQLALCHEMY_DATABASE_URL = f"postgresql://{CREDENTIALS['database_username']}:{CREDENTIALS['database_password']}" \
                          f"@{CREDENTIALS['database_host']}/{CREDENTIALS['database_name']}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.create_all(bind=engine)
