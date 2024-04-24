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
            port=DB_PORT,
            database=DB_NAME
        )
    except mariadb.Error as ex:
        print(f"An error occurred while connecting to MariaDB: {ex}")
        return None
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
            port=DB_PORT,
            database=DB_NAME
        )
    except mariadb.Error as ex:
        print(f"An error occurred while connecting to MariaDB: {ex}")
        return None
    cur = con.cursor()
    cur.execute("select ut.is_admin FROM user JOIN user_type AS ut ON user.type_id=ut.id WHERE user.login=?;", (login,))
    result = cur.fetchone()[0]
    con.close()
    return result


def get_current_temp(tank_id):
    try:
        con = mariadb.connect(
            user=DB_USER,
            password=DB_PASSWD,
            host=DB_IP,
            port=DB_PORT,
            database=DB_NAME
        )
    except mariadb.Error as ex:
        print(f"An error occurred while connecting to MariaDB: {ex}")
        return None
    cur = con.cursor()
    cur.execute("\
    SELECT sl.value, sl.`datetime` FROM tank AS t \
    JOIN sensor AS s ON s.type_id = t.id\
    JOIN `parameter` AS p ON s.parameter_id = p.id\
    JOIN param_type AS pt ON p.type_id = pt.id\
    JOIN sensor_log AS sl ON sl.sensor_id = s.id\
    WHERE t.id = ? AND pt.name = 'Температура'\
    ORDER BY sl.`datetime` DESC LIMIT 1;", (tank_id,))
    result = cur.fetchone()
    con.close()
    return result


def write_user_log(login: str, actionId: int):
    try:
        con = mariadb.connect(
            user=DB_USER,
            password=DB_PASSWD,
            host=DB_IP,
            port=DB_PORT,
            database=DB_NAME
        )
    except mariadb.Error as ex:
        print(f"An error occurred while connecting to MariaDB: {ex}")
        return None
    cur = con.cursor()
    cur.execute("SELECT id FROM user WHERE login=?;", (login,))
    userId = cur.fetchone()[0]
    cur.execute("INSERT INTO user_log(user_id, action_id) VALUES (?, ?);", (userId, actionId))
    con.commit()
    con.close()


def emergency_stop(tank_id: int, login: str):
    try:
        con = mariadb.connect(
            user=DB_USER,
            password=DB_PASSWD,
            host=DB_IP,
            port=DB_PORT,
            database=DB_NAME
        )
    except mariadb.Error as ex:
        print(f"An error occurred while connecting to MariaDB: {ex}")
        return None
    cur = con.cursor()
    cur.execute("SELECT id FROM user WHERE login=?;", (login,))
    user_id = cur.fetchone()[0]
    cur.execute("INSERT INTO user_log(user_id, action_id) VALUES (?, 3);", (user_id,))
    cur.execute("UPDATE process_log SET `end`=NOW(), result_id=2 WHERE tank_id=? AND `end`=NULL;", (tank_id,))
    con.commit()
    con.close()


if __name__ == '__main__':
    temp, datetime = get_current_temp(1)
    print(datetime.isoformat())
