from sqlalchemy_utils import drop_database, create_database

from app.database import CREDENTIALS

if __name__ == "__main__":

    fully_qualified_db_path: str = f"postgresql://{CREDENTIALS['database_username']}:{CREDENTIALS['database_password']}" \
                                   f"@{CREDENTIALS['database_host']}/{CREDENTIALS['database_name']}"

    drop_database(fully_qualified_db_path)
    create_database(fully_qualified_db_path)
