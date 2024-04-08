# from sqlalchemy import create_engine
# from sqlalchemy.orm import Session
# from config import DB_USER, DB_PASSWD, DB_IP, DB_NAME
# from db.models.BaseModelClass import BaseModelClass
# from db.models.User import User
#
# engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWD}@{DB_IP}/{DB_NAME}")
# BaseModelClass.metadata.create_all(bind=engine)
#
#
# def get_user_by_login(login: str):
#     with (Session(autoflush=False, bind=engine)) as db:
#         user = db.query(User).filter(User.login == login)[0]
#         return user
import sys

import mariadb

from config import DB_PASSWD, DB_USER, DB_IP, DB_PORT, DB_NAME


def get_passwd_by_login(login: str):
    try:
        con = mariadb.connect(
            user=DB_USER,
            password=DB_PASSWD,
            host=DB_IP,
            port=int(DB_PORT),
            database=DB_NAME
        )

    except mariadb.Error as ex:
        print(f"An error occurred while connecting to MariaDB: {ex}")
        sys.exit(1)
    cur = con.cursor()
    cur.execute("SELECT password FROM user WHERE login=?", (login,))
    result = cur.fetchone()[0]
    con.close()
    return result


def get_status_by_login(login: str):
    try:
        con = mariadb.connect(
            user=DB_USER,
            password=DB_PASSWD,
            host=DB_IP,
            port=int(DB_PORT),
            database=DB_NAME
        )

    except mariadb.Error as ex:
        print(f"An error occurred while connecting to MariaDB: {ex}")
        sys.exit(1)
    cur = con.cursor()
    cur.execute("select ut.is_admin FROM user JOIN user_type AS ut ON user.type_id=ut.id WHERE user.login=?;", (login,))
    result = cur.fetchone()[0]
    con.close()
    return result


if __name__ == '__main__':
    print(get_passwd_by_login("admin"))
