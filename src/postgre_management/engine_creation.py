import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

load_dotenv()

db_engine = create_engine(url = os.getenv('CONNECTION_URL'))
