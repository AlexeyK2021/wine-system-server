import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from config import DB_USER, DB_PASSWD, DB_IP, DB_NAME
from db.models.BaseModelClass import BaseModelClass
from db.models.User import User

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWD}@{DB_IP}/{DB_NAME}")
BaseModelClass.metadata.create_all(bind=engine)


def get_user_by_login(login: str):
    with (Session(autoflush=False, bind=engine)) as db:
        user = db.query(User).filter(User.login == login)[0]
        return user


if __name__ == '__main__':
    pass
