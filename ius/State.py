import enum
from ius import opcua_manager, db_manager


class State(enum.Enum):
    START_STATE = 0
    EMPTY_TANK_STATE = 1
    # Состояния для бурного брожения
    FILL_FF_TANK = 2
    PRE_FERMENTATION = 3
    FAST_FERMENTATION = 4
    DRAIN_FF_TANK = 5

    # Состояния для тихого брожения
    FILL_SF_TANK = 6
    SLOW_FERMENTATION = 7
    DRAIN_SF_TANK = 8


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


def init_tank(tank):
    input_valve = tank.input_valve
    he_pump = tank.he_pump
    he_input_valve = tank.he_input_valve
    he_output_valve = tank.he_output_valve
    output_pump = tank.output_pump
    output_valve = tank.output_valve
    co2_valve = tank.co2_valve

    opcua_manager.set_value(input_valve.ip, input_valve.port, input_valve.cmnd_node_id, False)
    opcua_manager.set_value(he_pump.ip, he_pump.port, he_pump.cmnd_node_id, False)
    opcua_manager.set_value(he_input_valve.ip, he_input_valve.port, he_input_valve.cmnd_node_id, False)
    opcua_manager.set_value(he_output_valve.ip, he_output_valve.port, he_output_valve.cmnd_node_id, False)
    opcua_manager.set_value(output_pump.ip, output_pump.port, output_pump.cmnd_node_id, False)
    opcua_manager.set_value(output_valve.ip, tank.output_valve.port, tank.output_valve.cmnd_node_id, False)
    opcua_manager.set_value(co2_valve.ip, co2_valve.port, co2_valve.cmnd_node_id, True)

    write_actuator_log(input_valve, False)
    write_actuator_log(he_pump, False)
    write_actuator_log(he_input_valve, False)
    write_actuator_log(he_output_valve, False)
    write_actuator_log(output_pump, False)
    write_actuator_log(output_valve, False)
    write_actuator_log(co2_valve, True)


def check_init(tank):
    input_valve_state = opcua_manager.get_value(tank.input_valve.ip, tank.input_valve.port,
                                                tank.input_valve.state_node_id)
    he_pump_state = opcua_manager.get_value(tank.he_pump.ip, tank.he_pump.port, tank.he_pump.state_node_id)
    he_input_valve_state = opcua_manager.get_value(tank.he_input_valve.ip, tank.he_input_valve.port,
                                                   tank.he_input_valve.state_node_id)
    he_output_valve_state = opcua_manager.get_value(tank.he_output_valve.ip, tank.he_output_valve.port,
                                                    tank.he_output_valve.state_node_id)
    output_pump_state = opcua_manager.get_value(tank.output_pump.ip, tank.output_pump.port,
                                                tank.output_pump.state_node_id)
    output_valve_state = opcua_manager.get_value(tank.output_valve.ip, tank.output_valve.port,
                                                 tank.output_valve.state_node_id)
    co2_valve_state = opcua_manager.get_value(tank.co2_valve.ip, tank.co2_valve.port, tank.co2_valve.state_node_id)

    return (
            (not input_valve_state) and (not he_pump_state) and (not he_input_valve_state) and
            (not he_output_valve_state) and (not output_pump_state) and (not output_valve_state) and
            co2_valve_state
    )


def fill_tank(tank):
    opcua_manager.set_value(tank.input_valve.ip, tank.input_valve.port, tank.input_valve.cmnd_node_id, True)
    write_actuator_log(tank.input_valve, True)


def end_fill_tank(tank):
    opcua_manager.set_value(tank.input_valve.ip, tank.input_valve.port, tank.input_valve.cmnd_node_id, False)
    write_actuator_log(tank.input_valve, False)


def control(tank):
    tank.curr_state = State(db_manager.get_current_tank_state(tank.id))
    if tank.type_id == 1:
        if tank.curr_state == State.EMPTY_TANK_STATE:
            start_process_log(tank)
            init_tank(tank)
            if check_init(tank):
                end_process_log(tank, True)
                tank.curr_state = State.FILL_FF_TANK

        elif tank.curr_state == State.FILL_FF_TANK:
            start_process_log(tank)
            fill_tank(tank)
            if check_sensor(tank.down_level_sensor) and check_sensor(tank.up_level_sensor):
                end_fill_tank(tank)
                end_process_log(tank, True)
                tank.curr_state = State.PRE_FERMENTATION

        elif tank.curr_state == State.PRE_FERMENTATION:
            # TODO
            tank.curr_state = State.FAST_FERMENTATION

        elif tank.curr_state == State.FAST_FERMENTATION:
            # TODO
            tank.curr_state = State.DRAIN_FF_TANK
        elif tank.curr_state == State.DRAIN_FF_TANK:
            # TODO
            tank.curr_state = State.START_STATE

    elif tank.type_id == 2:
        if tank.curr_state == State.EMPTY_TANK_STATE:
            # TODO
            tank.curr_state = State.FILL_SF_TANK

        elif tank.curr_state == State.FILL_SF_TANK:
            # TODO
            tank.curr_state = State.SLOW_FERMENTATION

        elif tank.curr_state == State.SLOW_FERMENTATION:
            # TODO
            tank.curr_state = State.DRAIN_SF_TANK

        elif tank.curr_state == State.DRAIN_SF_TANK:
            # TODO
            tank.curr_state = State.START_STATE
