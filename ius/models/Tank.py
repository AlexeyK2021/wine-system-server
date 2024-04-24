from ius.models.Actuator import Actuator
from ius.models.Sensor import Sensor
from ius.State import State


class Tank:
    def __init__(self, id: int, name: str, type_id: int,
                 temp_sensor: Sensor, pres_sensor: Sensor, up_level_sensor: Sensor, down_level_sensor: Sensor,
                 input_valve: Actuator, he_input_valve: Actuator, he_output_valve: Actuator, co2_valve: Actuator,
                 output_valve: Actuator, he_pump: Actuator, output_pump: Actuator):
        self.id = id
        self.name = name
        self.type_id = type_id
        self.curr_state = State.START_STATE

        self.temp_sensor = temp_sensor
        self.pres_sensor = pres_sensor
        self.up_level_sensor = up_level_sensor
        self.down_level_sensor = down_level_sensor

        self.input_valve = input_valve
        self.output_pump = output_pump
        self.he_pump = he_pump
        self.output_valve = output_valve
        self.co2_valve = co2_valve
        self.he_input_valve = he_input_valve
        self.he_output_valve = he_output_valve

    def __str__(self):
        return (f"Id={self.id}; name={self.name};\n"
                f"\ttemp_sensor=[{self.temp_sensor.__str__()}]\n"
                f"\tpres_sensor=[{self.pres_sensor.__str__()}]\n"
                f"\tup_level_sensor=[{self.up_level_sensor.__str__()}]\n"
                f"\tdown_level_sensor=[{self.down_level_sensor.__str__()}]\n"
                f"\tinput_valve=[{self.input_valve.__str__()}]\n"
                f"\toutput_pump=[{self.output_pump.__str__()}]\n"
                f"\the_pump=[{self.he_pump.__str__()}]\n"
                f"\toutput_valve=[{self.output_valve.__str__()}]\n"
                f"\tco2_valve=[{self.co2_valve.__str__()}]\n"
                f"\the_output_valve=[{self.he_output_valve.__str__()}]\n"
                f"\the_input_valve=[{self.he_input_valve.__str__()}]\n"
                )
