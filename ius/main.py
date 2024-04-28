from time import sleep

import db_manager
from control import control_process

if __name__ == '__main__':
    pass
    # db_manager.write_actuator_log(2,False)
    # db_manager.write_start_process_log(1, State.EMPTY_TANK_STATE.value)
    # sleep(1)
    # db_manager.write_end_process_log(1, 1)
    tanks = db_manager.get_tanks()
    tanks.pop(1)
    while True:
        for tank in tanks:
            control_process(tank)
            sleep(5)
    # db_manager.get_remaining_time_of_process(1)
    # exec_time = 72000
    # start_time = datetime.datetime(2024, 4, 27, 17, 0, 48, 0)
    # remain_time = exec_time - datetime.datetime.now().timestamp() + start_time.timestamp()
    # print(remain_time)
