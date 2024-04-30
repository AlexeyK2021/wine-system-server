from time import sleep

import db_manager
from control import control_process
from ius import opcua_manager


def check_sensors(tank):
    temp_sensor = opcua_manager.check_sensor(tank.temp_sensor)
    pres_sensor = opcua_manager.check_sensor(tank.pres_sensor)
    up_level_sensor = opcua_manager.check_sensor(tank.up_level_sensor)
    down_level_sensor = opcua_manager.check_sensor(tank.down_level_sensor)
    return temp_sensor and pres_sensor and up_level_sensor and down_level_sensor


def check_actuators(tank):
    input_valve_state = opcua_manager.check_actuator(tank.input_valve)
    he_pump_state = opcua_manager.check_actuator(tank.he_pump)
    he_input_valve_state = opcua_manager.check_actuator(tank.he_input_valve)
    he_output_valve_state = opcua_manager.check_actuator(tank.he_output_valve)
    output_pump_state = opcua_manager.check_actuator(tank.output_pump)
    output_valve_state = opcua_manager.check_actuator(tank.output_valve)
    co2_valve_state = opcua_manager.check_actuator(tank.co2_valve)
    return input_valve_state and he_pump_state and he_input_valve_state and he_output_valve_state and output_pump_state and output_valve_state and co2_valve_state


def main():
    # TODO check sensors and actuators availability and check db
    while not db_manager.check_db():
        print("Can't connect to DB!!!")

    tanks = db_manager.get_tanks()
    all_work = False
    while not all_work:
        for tank in tanks:
            print(f"Ёмкость {tank.name}:")
            all_work = check_sensors(tank) * check_actuators(tank)
    print("OK")

    while True:
        for tank in tanks:
            control_process(tank)
            sleep(2)


if __name__ == '__main__':
    main()
    pass
    # db_manager.write_actuator_log(2,False)
    # db_manager.write_start_process_log(1, State.EMPTY_TANK_STATE.value)
    # sleep(1)
    # db_manager.write_end_process_log(1, 1)

    # db_manager.get_remaining_time_of_process(1)
    # exec_time = 72000
    # start_time = datetime.datetime(2024, 4, 27, 17, 0, 48, 0)
    # remain_time = exec_time - datetime.datetime.now().timestamp() + start_time.timestamp()
    # print(remain_time)
