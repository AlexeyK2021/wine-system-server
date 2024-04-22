from opcua import Server, ua
import random
import time

server = Server()
server.set_endpoint("opc.tcp://0.0.0.0:4841")

idx = server.register_namespace("OPC_TEST_SERVER")

objects = server.get_objects_node()
temp_sensor = objects.add_object(idx, "Temperature Sensor")
press_sensor = objects.add_object(idx, "Pressure Sensor")
up_sensor = objects.add_object(idx, "Up Level Sensor")
down_sensor = objects.add_object(idx, "Down Level Sensor")
input_valve = objects.add_object(idx, "Input Valve")
# valve_controller = objects.add_object(idx, "Valve Controller")

t_status = temp_sensor.add_variable(idx, "Status", True)
t_status.set_writable(writable=False)
t_temp = temp_sensor.add_variable(idx, "Temperature", 18)
t_temp.set_writable(writable=False)

p_status = press_sensor.add_variable(idx, "Status", True)
p_status.set_writable(writable=False)
p_pressure = press_sensor.add_variable(idx, "Pressure", 950)
p_pressure.set_writable(writable=False)

ul_status = up_sensor.add_variable(idx, "Status", True)
ul_status.set_writable(writable=False)
ul_value = up_sensor.add_variable(idx, "Value", False)
ul_value.set_writable(writable=False)

dl_status = down_sensor.add_variable(idx, "Status", True)
dl_status.set_writable(writable=False)
dl_value = down_sensor.add_variable(idx, "Value", False)
dl_value.set_writable(writable=False)

iv_state = input_valve.add_variable(idx, "Current State", False)
# iv_state.set_writable(writable=False)
iv_state.set_writable(writable=True)
iv_cmnd = input_valve.add_variable(idx, "Command", True)
iv_cmnd.set_writable(writable=True)

# valve1 = valve_controller.add_variable(idx, "Input valve", False)
# valve2 = valve_controller.add_variable(idx, "CO2 output valve", False)
# valve1.set_writable(writable=True)
# valve2.set_writable(writable=True)

# etype = server.create_custom_event_type(idx, 'TempEvent', ua.ObjectIds.BaseEventType, [('Value', ua.VariantType.Float)])
# myevgen = server.get_event_generator(etype, temp_sensor)
server.start()

if __name__ == '__main__':
    try:
        while True:
            value = random.randrange(18, 24)
            t_temp.set_value(value)
            p_pressure.set_value(random.randrange(95, 105))
            ul_value.set_value(random.randint(0, 1))
            dl_value.set_value(random.randint(0, 1))
            # myevgen.event.Value = value
            # myevgen.trigger()
            print(
                f"OPC UA Server Status: \n"
                f"Temp={t_temp.get_value()};\n"
                f"Pressure={p_pressure.get_value()};\n"
                f"Up={ul_value.get_value()};\n"
                f"Down={dl_value.get_value()}"
            )
            iv_state.set_value(iv_cmnd.get_value())
            time.sleep(2)
    except KeyboardInterrupt:
        server.stop()
