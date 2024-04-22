import enum

from db.models.Tank import Tank
from ius import opcua_manager


class State(enum.Enum):
    EMPTY_TANK_STATE = 0
    # Состояния для бурного брожения
    FILL_FF_TANK = 1
    PRE_FERMENTATION = 2
    FAST_FERMENTATION = 3
    DRAIN_FF_TANK = 4

    # Состояния для тихого брожения
    FILL_SF_TANK = 1
    SLOW_FERMENTATION = 2
    DRAIN_SF_TANK = 3


def write_actuator_log(actuator, new_state):
    pass


def init_tank(tank: Tank):
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


def check_init(tank: Tank):
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


def fill_tank(tank: Tank):
    opcua_manager.set_value(tank.input_valve.ip, tank.input_valve.port, tank.input_valve.cmnd_node_id, True)
    write_actuator_log(tank.input_valve, True)


def end_fill_tank(tank: Tank):
    opcua_manager.set_value(tank.input_valve.ip, tank.input_valve.port, tank.input_valve.cmnd_node_id, False)
    write_actuator_log(tank.input_valve, False)


def check_sensor(sensor):
    return opcua_manager.get_value(sensor.ip, sensor.port, sensor.cmnd_node_id)


def control(self, tank):
    if tank.type_id == 1:
        if tank.curr_state == State.EMPTY_TANK_STATE:
            init_tank(tank)
            if check_init(tank):
                tank.curr_state = State.FILL_FF_TANK

        elif tank.curr_state == State.FILL_FF_TANK:
            fill_tank(tank)
            if check_sensor(tank.down_level_sensor) and check_sensor(tank.up_level_sensor):
                end_fill_tank(tank)
                tank.curr_state = State.PRE_FERMENTATION

        elif tank.curr_state == State.PRE_FERMENTATION:
            # TODO
            tank.curr_state = State.FAST_FERMENTATION

        elif tank.curr_state == State.FAST_FERMENTATION:
            # TODO
            tank.curr_state = State.DRAIN_FF_TANK

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
