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


# def write_user_log(login: str, actionId: int):
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
#     cur.execute("SELECT id FROM user WHERE login=?;", (login,))
#     userId = cur.fetchone()[0]
#     cur.execute("INSERT INTO user_log(user_id, action_id) VALUES (?, ?);", (userId, actionId))
#     con.commit()
#     con.close()


def emergency_stop(tank_id: int, login):
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


def init_tank(tank_id, login):
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


def get_current_tank_state(tank_id: int):
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
    cur.execute("CALL get_tank_last_state(?)", (tank_id,))
    result = cur.fetchone()
    con.close()
    process_name = result[3]
    if result[1] == 2:
        process_name += "\n(Экстренная остановка)"
    return {
        "process_id": result[2],
        "process_name": process_name
    }


if __name__ == '__main__':
    get_current_tank_state(1)
