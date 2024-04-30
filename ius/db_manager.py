import datetime

import mariadb

from config import DB_PASSWD, DB_USER, DB_IP, DB_PORT, DB_NAME
from models.Actuator import Actuator
from models.Sensor import Sensor
from models.State import State
from models.Tank import Tank


def get_sensors(sensors_text):
    sensors = list()
    for s in sensors_text:
        sensors.append(Sensor(id=s[0], name=s[1], model=s[2], paramId=s[5], ip=s[6], port=s[7], nodeId=s[8]))
    return sensors


def get_actuators(actuators_text):
    actuators = list()
    for a in actuators_text:
        actuators.append(
            Actuator(id=a[0], name=a[1], model=a[2], ip=a[5], port=a[6], state_node_id=a[7], cmnd_node_id=a[8]))
    return actuators


def write_sensor_log(sensor_id, value):
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
    cur.execute("INSERT INTO sensor_log(value, sensor_id) VALUES (?, ?);", (value, sensor_id))
    con.commit()
    con.close()


def write_actuator_log(actuator_id, state):
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
    cur.execute("INSERT INTO actuator_log(state, actuator_id) VALUES (?, ?);", (state, actuator_id))
    con.commit()
    con.close()


def write_start_process_log(tank_id, process_id):
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
    # cur.execute("SELECT id FROM process WHERE name = ?;", (curr_state,))
    # process_id = cur.fetchone()[0]
    cur.execute("INSERT INTO process_log (process_id, tank_id) VALUES (?, ?);", (process_id, tank_id))
    con.commit()
    con.close()


def write_end_process_log(tank_id, result):
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
    cur.execute("UPDATE process_log SET `end`=NOW(), result_id=? WHERE tank_id=? AND `end` is NULL;",
                (result, tank_id,))
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
    cur.execute("SELECT * FROM tank;")
    result = cur.fetchall()

    tanks = list()
    for t in result:
        cur.execute("SELECT * FROM sensor WHERE sensor.tank_id=? ORDER BY type_id;", (t[0],))
        sensors = get_sensors(cur.fetchall())
        # print(*sensors)
        cur.execute("SELECT * FROM actuator WHERE actuator.tank_id = ? ORDER BY type_id;", (t[0],))
        actuators = get_actuators(cur.fetchall())
        # print(*actuators)
        tanks.append(Tank(
            id=t[0], name=t[1], type_id=t[2],
            temp_sensor=sensors[0], pres_sensor=sensors[1], up_level_sensor=sensors[2], down_level_sensor=sensors[3],
            input_valve=actuators[0], he_input_valve=actuators[6], he_output_valve=actuators[1], co2_valve=actuators[2],
            output_valve=actuators[3], he_pump=actuators[4], output_pump=actuators[5]
        ))
    con.close()
    # print(*tanks)
    return tanks


def get_tank_type_by_id(id):
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
    cur.execute("select name from tank_type WHERE id = ?;", (id,))
    result = cur.fetchone()[0]
    con.close()
    return result


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
    # print(result)
    if result is None:
        return 0
    if result[5] is None or result[5] == 1:
        return result[6]
    elif result[5] == 2:
        return State.EMERGENCY_STOP


def get_remaining_time_of_process(tank_id):  # получение прошедшего времени с начала процесса в секундах
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
    start_time = result[1]
    cur.execute("SELECT execution_time FROM process WHERE id = ?", (result[6],))
    exec_time = cur.fetchone()[0]
    con.close()
    # print(exec_time)
    remain_time = exec_time - datetime.datetime.now().timestamp() + start_time.timestamp()
    print(remain_time)
    if exec_time is None:
        return 0
    return remain_time


def get_parameter_interval(param_id):
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
    cur.execute("SELECT min_value, max_value FROM `parameter` WHERE id = ?;", (param_id,))
    result = cur.fetchone()
    con.close()
    # print(result)
    return result


def check_db():
    try:
        con = mariadb.connect(
            user=DB_USER,
            password=DB_PASSWD,
            host=DB_IP,
            port=DB_PORT,
            database=DB_NAME
        )
        return True
    except mariadb.Error:
        return False
