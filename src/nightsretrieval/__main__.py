from dotenv import load_dotenv
import os

from sqlalchemy import create_engine

from version_control_system.model import Base

load_dotenv()

# DATABASE CREDENTIALS
USER = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DATABASE = os.getenv("DATABASE")


def create_db() -> None:
    try:
        # connection_string = f"mysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
        connection_string = "sqlite:///nightsretrieval.db"
        engine = create_engine(url=connection_string, echo=True)

        Base.metadata.create_all(engine)

    except Exception as ex:
        print("Connection could not be made due to the following error: \n", ex)
