import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

# DATABASE CREDENTIALS
conf = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USERNAME"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_DATABASE_NAME"),
    "port": os.getenv("DB_PORT"),
}

CONNECTION_STRING_PSQL = "postgresql://{user}:{password}@{host}:{port}/{database}".format(**conf)
CONNECTION_STRING_SQLITE = "sqlite:///src/database/nightsretrieval.db"


def init_engine(is_local: bool) -> create_engine:
    connection_string = CONNECTION_STRING_SQLITE if is_local else CONNECTION_STRING_PSQL
    try:
        engine = create_engine(url=connection_string, echo=True)
        return engine

    except Exception as ex:
        print("Connection could not be made due to the following error: \n", ex)
