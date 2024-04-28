import enum
from ius import opcua_manager, db_manager


class State(enum.Enum):
    START_STATE = 9
    EMPTY_TANK_STATE = 1

    # Состояния для бурного брожения
    # FILL_FF_TANK = 2
    PRE_FERMENTATION = 3
    FAST_FERMENTATION = 4
    # DRAIN_FF_TANK = 5

    # Состояния для тихого брожения
    # FILL_SF_TANK = 6
    SLOW_FERMENTATION = 7
    # DRAIN_SF_TANK = 8

    EMERGENCY_STOP = 10

    FILL_TANK = 11
    DRAIN_TANK = 12


def write_actuator_log(actuator, state):
    db_manager.write_actuator_log(actuator.id, state)


def write_sensor_log(sensor, value):
    db_manager.write_sensor_log(sensor.id, value)


def start_process_log(tank):
    db_manager.write_start_process_log(tank.id, tank.curr_state.value)


def end_process_log(tank, result):
    db_manager.write_end_process_log(tank.id, 1)


def check_sensor(sensor):
    value = opcua_manager.get_value(sensor.ip, sensor.port, sensor.node_id)
    write_sensor_log(sensor, value)
    return value


def check_actuator(actuator):
    return opcua_manager.get_value(actuator.ip, actuator.port, actuator.state_node_id)


def set_actuator(actuator, value):
    curr_state = check_actuator(actuator)
    if curr_state != value:
        opcua_manager.set_value(actuator.ip, actuator.port, actuator.cmnd_node_id, value)
        write_actuator_log(actuator, value)


def init_tank(tank):
    input_valve = tank.input_valve
    he_pump = tank.he_pump
    he_input_valve = tank.he_input_valve
    he_output_valve = tank.he_output_valve
    output_pump = tank.output_pump
    output_valve = tank.output_valve
    co2_valve = tank.co2_valve

    set_actuator(input_valve, False)
    set_actuator(he_pump, False)
    set_actuator(he_input_valve, False)
    set_actuator(he_output_valve, False)
    set_actuator(output_pump, False)
    set_actuator(output_valve, False)
    set_actuator(co2_valve, True)


def check_init(tank):
    input_valve_state = check_actuator(tank.input_valve)
    he_pump_state = check_actuator(tank.he_pump)
    he_input_valve_state = check_actuator(tank.he_input_valve)
    he_output_valve_state = check_actuator(tank.he_output_valve)
    output_pump_state = check_actuator(tank.output_pump)
    output_valve_state = check_actuator(tank.output_valve)
    co2_valve_state = check_actuator(tank.co2_valve)

    return (
            (not input_valve_state) and (not he_pump_state) and (not he_input_valve_state) and
            (not he_output_valve_state) and (not output_pump_state) and (not output_valve_state) and
            co2_valve_state
    )


def fill_tank(tank):
    set_actuator(tank.input_valve, True)


def end_fill_tank(tank):
    set_actuator(tank.input_valve, False)


def control_temp(tank):  ## при холодном открываем краны, при горячем открываем краны.
    temp = check_sensor(tank.temp_sensor)  ## Может их открыть с самого начала?
    min_temp, max_temp = db_manager.get_parameter_interval(tank.temp_sensor.param_id)
    avg = (min_temp + max_temp) / 2
    delta = 1.5

    if temp <= avg - delta or temp >= avg + delta:
        set_actuator(tank.he_input_valve, True)
        set_actuator(tank.he_output_valve, True)
        set_actuator(tank.he_pump, True)
    elif avg + delta > temp > avg - delta:
        set_actuator(tank.he_input_valve, False)
        set_actuator(tank.he_output_valve, False)
        set_actuator(tank.he_pump, False)


def control_pressure(tank):
    pres = check_sensor(tank.pres_sensor)
    min_pres, max_pres = db_manager.get_parameter_interval(tank.pres_sensor.param_id)

    if pres > max_pres:
        if not check_actuator(tank.co2_valve):
            set_actuator(tank.co2_valve, True)
        else:
            pass
            # TODO Тревога


def drain_tank(tank):
    set_actuator(tank.input_valve, False)
    set_actuator(tank.he_pump, False)
    set_actuator(tank.he_input_valve, False)
    set_actuator(tank.he_output_valve, False)
    set_actuator(tank.output_pump, True)
    set_actuator(tank.output_valve, True)
    set_actuator(tank.co2_valve, True)


def end_drain_tank(tank):
    set_actuator(tank.output_valve, False)
    set_actuator(tank.output_pump, False)


def emergency_stop(tank):
    set_actuator(tank.input_valve, False)
    set_actuator(tank.he_pump, False)
    set_actuator(tank.he_input_valve, False)
    set_actuator(tank.he_output_valve, False)
    set_actuator(tank.output_pump, True)
    set_actuator(tank.output_valve, True)
    set_actuator(tank.co2_valve, True)


def check_emergency_stop(tank):
    input_valve_state = check_actuator(tank.input_valve)
    he_pump_state = check_actuator(tank.he_pump)
    he_input_valve_state = check_actuator(tank.he_input_valve)
    he_output_valve_state = check_actuator(tank.he_output_valve)
    output_pump_state = check_actuator(tank.output_pump)
    output_valve_state = check_actuator(tank.output_valve)
    co2_valve_state = check_actuator(tank.co2_valve)

    return (
            (not input_valve_state) and (not he_pump_state) and (not he_input_valve_state) and
            (not he_output_valve_state) and output_pump_state and output_valve_state and co2_valve_state
    )


def print_curr_state(tank):
    print(
        f"Tank {tank.name}({tank.curr_state.name})\n"
        f"Sensors:\n"
        f"\t Temp: {check_sensor(tank.temp_sensor)}\n"
        f"\t Pressure: {check_sensor(tank.pres_sensor)}\n"
        f"\t Up Level: {check_sensor(tank.up_level_sensor)}\n"
        f"\t Down Level: {check_sensor(tank.down_level_sensor)}\n"
        f"Actuators:\n"
        f"\t Input Valve:{check_actuator(tank.input_valve)}\n"
        f"\t HE Pump:{check_actuator(tank.he_pump)}\n"
        f"\t HE Input:{check_actuator(tank.he_input_valve)}\n"
        f"\t HE Output:{check_actuator(tank.he_output_valve)}\n"
        f"\t Output Pump:{check_actuator(tank.output_pump)}\n"
        f"\t Output Valve:{check_actuator(tank.output_valve)}\n"
        f"\t CO2 Valve: {check_actuator(tank.co2_valve)}\n"
    )


def control_process(tank):
    tank.curr_state = State(db_manager.get_current_tank_state(tank.id))
    print_curr_state(tank)

    # if tank.type_id == 1:
    #     if tank.curr_state == State.EMPTY_TANK_STATE:
    #         init_tank(tank)
    #         if check_init(tank):
    #             end_process_log(tank, True)
    #             tank.curr_state = State.FILL_FF_TANK
    #             start_process_log(tank)
    #
    #     elif tank.curr_state == State.FILL_FF_TANK:
    #         fill_tank(tank)
    #         if check_sensor(tank.down_level_sensor) and check_sensor(tank.up_level_sensor):
    #             end_fill_tank(tank)
    #             end_process_log(tank, True)
    #             tank.curr_state = State.PRE_FERMENTATION
    #             start_process_log(tank)
    #
    #     elif tank.curr_state == State.PRE_FERMENTATION:
    #         control_temp(tank)
    #         control_pressure(tank)
    #         if db_manager.get_remaining_time_of_process(tank.id) <= 0:
    #             end_process_log(tank, True)
    #             tank.curr_state = State.FAST_FERMENTATION
    #             start_process_log(tank)
    #
    #     elif tank.curr_state == State.FAST_FERMENTATION:
    #         control_temp(tank)
    #         control_pressure(tank)
    #         if db_manager.get_remaining_time_of_process(tank.id) <= 0:
    #             end_process_log(tank, True)
    #             tank.curr_state = State.DRAIN_FF_TANK
    #             start_process_log(tank)
    #
    #     elif tank.curr_state == State.DRAIN_FF_TANK:
    #         drain_tank(tank)
    #         if not check_sensor(tank.up_level_sensor) and not check_sensor(tank.down_level_sensor):
    #             end_drain_tank(tank)
    #             end_process_log(tank, True)
    #             tank.curr_state = State.START_STATE
    #             start_process_log(tank)
    #
    #     elif tank.curr_state == State.EMERGENCY_STOP:
    #         emergency_stop(tank)
    #         #TODO
    #
    # elif tank.type_id == 2:
    #     if tank.curr_state == State.EMPTY_TANK_STATE:
    #         init_tank(tank)
    #         if check_init(tank):
    #             end_process_log(tank, True)
    #             tank.curr_state = State.FILL_SF_TANK
    #             start_process_log(tank)
    #
    #     elif tank.curr_state == State.FILL_SF_TANK:
    #         fill_tank(tank)
    #         if check_sensor(tank.down_level_sensor) and check_sensor(tank.up_level_sensor):
    #             end_fill_tank(tank)
    #             end_process_log(tank, True)
    #             tank.curr_state = State.SLOW_FERMENTATION
    #             start_process_log(tank)
    #
    #     elif tank.curr_state == State.SLOW_FERMENTATION:
    #         control_temp(tank)
    #         control_pressure(tank)
    #         if db_manager.get_remaining_time_of_process(tank.id) <= 0:
    #             end_process_log(tank, True)
    #             tank.curr_state = State.DRAIN_SF_TANK
    #             start_process_log(tank)
    #
    #     elif tank.curr_state == State.DRAIN_SF_TANK:
    #         drain_tank(tank)
    #         if not check_sensor(tank.up_level_sensor) and not check_sensor(tank.down_level_sensor):
    #             end_drain_tank(tank)
    #             end_process_log(tank, True)
    #             tank.curr_state = State.START_STATE
    #             start_process_log(tank)
    #
    #     elif tank.curr_state == State.EMERGENCY_STOP:
    #         emergency_stop(tank)
    #         # TODO

    if tank.curr_state == State.EMPTY_TANK_STATE:
        init_tank(tank)
        if check_init(tank):
            end_process_log(tank, True)
            tank.curr_state = State.FILL_TANK
            start_process_log(tank)

    elif tank.curr_state == State.FILL_TANK:
        fill_tank(tank)
        if check_sensor(tank.down_level_sensor) and check_sensor(tank.up_level_sensor):
            end_fill_tank(tank)
            end_process_log(tank, True)
            if tank.type_id == 1:
                tank.curr_state = State.PRE_FERMENTATION
            elif tank.type_id == 2:
                tank.curr_state = State.SLOW_FERMENTATION
            start_process_log(tank)

    elif tank.curr_state == State.PRE_FERMENTATION:
        control_temp(tank)
        control_pressure(tank)
        if db_manager.get_remaining_time_of_process(tank.id) <= 0:
            end_process_log(tank, True)
            tank.curr_state = State.FAST_FERMENTATION
            start_process_log(tank)

    elif tank.curr_state == State.FAST_FERMENTATION:
        control_temp(tank)
        control_pressure(tank)
        if db_manager.get_remaining_time_of_process(tank.id) <= 0:
            end_process_log(tank, True)
            tank.curr_state = State.DRAIN_TANK
            start_process_log(tank)

    elif tank.curr_state == State.SLOW_FERMENTATION:
        control_temp(tank)
        control_pressure(tank)
        if db_manager.get_remaining_time_of_process(tank.id) <= 0:
            end_process_log(tank, True)
            tank.curr_state = State.DRAIN_TANK
            start_process_log(tank)

    elif tank.curr_state == State.DRAIN_TANK:
        drain_tank(tank)
        if not check_sensor(tank.up_level_sensor) and not check_sensor(tank.down_level_sensor):
            end_drain_tank(tank)
            end_process_log(tank, True)
            tank.curr_state = State.START_STATE
            start_process_log(tank)

    elif tank.curr_state == State.EMERGENCY_STOP:
        emergency_stop(tank)
        # TODO
