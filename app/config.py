from dotenv import load_dotenv
import os

BASE_DIR = os.curdir
load_dotenv()

class Config:
    SECRET_KEY=os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI=f"sqlite:///{BASE_DIR}/app.db"
    SQLALCHEMY_TRACKMODIFICATIONS=False
    