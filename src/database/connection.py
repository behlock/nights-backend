import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

# DATABASE CREDENTIALS
USER = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DATABASE = os.getenv("DATABASE")

# CONNECTION_STRING = f"mysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
CONNECTION_STRING = "sqlite:///src/database/nightsretrieval.db"


def init_engine() -> create_engine:
    try:
        engine = create_engine(url=CONNECTION_STRING, echo=True)
        return engine

    except Exception as ex:
        print("Connection could not be made due to the following error: \n", ex)
