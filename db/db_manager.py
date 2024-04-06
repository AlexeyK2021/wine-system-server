import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from config import DB_USER, DB_PASSWD, DB_IP, DB_NAME
from db.models.BaseModelClass import BaseModelClass
from db.models.User import User
from db.models.UserAction import UserAction
from db.models.UserLog import UserLog
from db.models.UserType import UserType

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWD}@{DB_IP}/{DB_NAME}")

if __name__ == '__main__':
    BaseModelClass.metadata.create_all(bind=engine)
    with Session(autoflush=False, bind=engine) as db:
        # engineer = UserType(name="Инженер", description="ИнженерИнженер")
        # operator = UserType(name="Оператор", description="ОператорОператор")
        # db.add_all([engineer, operator])
        # db.commit()
        #
        # admin = User(name="Admin Admin", login="admin",
        #              password="8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918", type=engineer)
        # alexey = User(name="Alexey K", login="alexey",
        #               password="d217e1716cb7b36f8be65117f625a1e39d22fd585528632391bb74310a4f255d", type=operator)
        #
        # db.add_all([admin, alexey])
        # db.commit()

        # enter = UserAction(name="Вход в систему")
        # db.add(enter)
        # db.commit()

        admin = db.query(User).filter(User.login=="admin")[0]
        admin_login_log = UserLog(datetime=datetime.datetime.now(), action_id=1, user=admin)
        db.add(admin_login_log)
        db.commit()


