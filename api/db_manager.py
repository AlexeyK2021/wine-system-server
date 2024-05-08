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


def auth_user(login: str, passwd: str):
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
    cur.execute("SELECT check_auth(?, ?);", (login, passwd,))
    result = cur.fetchone()[0]
    con.commit()
    con.close()
    return result


# def get_status_by_login(login: str):
#     try:
#         con = mariadb.connect(
#             user=DB_USER,
#             password=DB_PASSWD,
#             host=DB_IP,
#             port=DB_PORT,
#             database=DB_NAME
#         )
#     except mariadb.Error as ex:
#         print(f"An error occurred while connecting to MariaDB: {ex}")
#         return None
#     cur = con.cursor()
#     cur.execute("select ut.is_admin FROM user JOIN user_type AS ut ON user.type_id=ut.id WHERE user.login=?;", (login,))
#     result = cur.fetchone()[0]
#     con.close()
#     return result


# def get_current_params(tank_id):
#     try:
#         con = mariadb.connect(
#             user=DB_USER,
#             password=DB_PASSWD,
#             host=DB_IP,
#             port=DB_PORT,
#             database=DB_NAME
#         )
#     except mariadb.Error as ex:
#         print(f"An error occurred while connecting to MariaDB: {ex}")
#         return None
#     cur = con.cursor()
#     cur.execute("CALL get_current_params(?)", (tank_id,))
#     result = cur.fetchall()
#     con.close()
#     return result[0][1], result[1][1], result[2][1], result[3][1]


# def get_current_actuators_state(tank_id):
#     try:
#         con = mariadb.connect(
#             user=DB_USER,
#             password=DB_PASSWD,
#             host=DB_IP,
#             port=DB_PORT,
#             database=DB_NAME
#         )
#     except mariadb.Error as ex:
#         print(f"An error occurred while connecting to MariaDB: {ex}")
#         return None
#     cur = con.cursor()
#     cur.execute("CALL get_current_actuators(?)", (tank_id,))
#     result = cur.fetchall()
#     con.close()
#     return result


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
    cur.execute("UPDATE process_log SET `end`=NOW(), result_id=2 WHERE tank_id=? AND `end` is NULL;", (tank_id,))
    con.commit()
    con.close()


def init_tank(tank_id, login: str):
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
    cur.execute("INSERT INTO user_log(user_id, action_id) VALUES (?, 4);", (user_id,))
    cur.execute("UPDATE process_log SET `end`=NOW() WHERE tank_id=? AND `end` is NULL;", (tank_id,))
    cur.execute("INSERT INTO process_log(tank_id, process_id) VALUES (?,1);", (tank_id,))
    con.commit()
    con.close()


def get_tanks():
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
    cur.execute("select * from tank;")
    res = cur.fetchall()
    data = []
    for tank in res:
        data.append({"id": tank[0], "name": tank[1], "type_id": tank[2]})
    return data


if __name__ == '__main__':
    # get_tanks()
    pass
    # print(auth_user("admin1", "c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"))
    # print(*get_current_params(1), sep="\n")
