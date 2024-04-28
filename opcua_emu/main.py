from opcua import Server
import time

OPC_IP = "0.0.0.0"
OPC_PORT = 4840
OPC_NAMESPACE = "OPC_TEST_SERVER"

server = Server()
server.set_endpoint(f"opc.tcp://{OPC_IP}:{OPC_PORT}")
idx = server.register_namespace(OPC_NAMESPACE)
objects = server.get_objects_node()

temp_sensor = objects.add_object(idx, "Temperature Sensor")
press_sensor = objects.add_object(idx, "Pressure Sensor")
up_sensor = objects.add_object(idx, "Up Level Sensor")
down_sensor = objects.add_object(idx, "Down Level Sensor")

input_valve = objects.add_object(idx, "Input Valve")
output_pump = objects.add_object(idx, "Output Pump")
he_pump = objects.add_object(idx, "HE Pump")
output_valve = objects.add_object(idx, "Output Valve")
co2_valve = objects.add_object(idx, "CO2 Valve")
he_input_valve = objects.add_object(idx, "HE Input Valve")
he_output_valve = objects.add_object(idx, "HE Output Valve")
# valve_controller = objects.add_object(idx, "Valve Controller")
# init_state_button = objects.add_object(idx, "INIT")
# init_btn = init_state_button.add_variable(idx, "Init", False)
##########################SENSORS##################################
t_status = temp_sensor.add_variable(idx, "Status", True)
t_status.set_writable(writable=False)
t_temp = temp_sensor.add_variable(idx, "Value", 18)
t_temp.set_writable(writable=True)

p_status = press_sensor.add_variable(idx, "Status", True)
p_status.set_writable(writable=False)
p_pressure = press_sensor.add_variable(idx, "Value", 950)
p_pressure.set_writable(writable=True)

ul_status = up_sensor.add_variable(idx, "Status", True)
ul_status.set_writable(writable=False)
ul_value = up_sensor.add_variable(idx, "Value", False)
ul_value.set_writable(writable=True)

dl_status = down_sensor.add_variable(idx, "Status", True)
dl_status.set_writable(writable=False)
dl_value = down_sensor.add_variable(idx, "Value", False)
dl_value.set_writable(writable=True)

##########################ACTUATORS##################################
iv_state = input_valve.add_variable(idx, "Current State", False)
# iv_state.set_writable(writable=False)
iv_state.set_writable(writable=False)
iv_cmnd = input_valve.add_variable(idx, "Command", False)
iv_cmnd.set_writable(writable=True)

op_state = output_pump.add_variable(idx, "Current State", False)
# iv_state.set_writable(writable=False)
op_state.set_writable(writable=False)
op_cmnd = output_pump.add_variable(idx, "Command", False)
op_cmnd.set_writable(writable=True)

he_pump_state = he_pump.add_variable(idx, "Current State", False)
# iv_state.set_writable(writable=False)
he_pump_state.set_writable(writable=False)
he_pump_cmnd = he_pump.add_variable(idx, "Command", False)
he_pump_cmnd.set_writable(writable=True)

ov_state = output_valve.add_variable(idx, "Current State", False)
# iv_state.set_writable(writable=False)
ov_state.set_writable(writable=False)
ov_cmnd = output_valve.add_variable(idx, "Command", False)
ov_cmnd.set_writable(writable=True)

co2_state = co2_valve.add_variable(idx, "Current State", False)
# iv_state.set_writable(writable=False)
co2_state.set_writable(writable=False)
co2_cmnd = co2_valve.add_variable(idx, "Command", False)
co2_cmnd.set_writable(writable=True)

he_iv_state = he_input_valve.add_variable(idx, "Current State", False)
# iv_state.set_writable(writable=False)
he_iv_state.set_writable(writable=False)
he_iv_cmnd = he_input_valve.add_variable(idx, "Command", False)
he_iv_cmnd.set_writable(writable=True)

he_ov_state = he_output_valve.add_variable(idx, "Current State", False)
# iv_state.set_writable(writable=False)
he_ov_state.set_writable(writable=False)
he_ov_cmnd = he_output_valve.add_variable(idx, "Command", False)
he_ov_cmnd.set_writable(writable=True)

server.start()
if __name__ == '__main__':
    try:
        while True:
            # t_temp.set_value(random.randrange(18, 24))
            # p_pressure.set_value(random.randrange(95, 105))
            # ul_value.set_value(random.randint(0, 1))
            # dl_value.set_value(random.randint(0, 1))

            iv_state.set_value(iv_cmnd.get_value())
            op_state.set_value(op_cmnd.get_value())
            he_pump_state.set_value(he_pump_cmnd.get_value())
            ov_state.set_value(ov_cmnd.get_value())
            co2_state.set_value(co2_cmnd.get_value())
            he_iv_state.set_value(he_iv_cmnd.get_value())
            he_ov_state.set_value(he_ov_cmnd.get_value())
            # print(
            #     f"OPC UA Server Status: \n"
            #     f"Temp={t_temp.get_value()};\n"
            #     f"Pressure={p_pressure.get_value()};\n"
            #     f"Up={ul_value.get_value()};\n"
            #     f"Down={dl_value.get_value()}"
            # )
            # if init_btn.get_value():
            #     iv_state.set_value(False)
            #     op_state.set_value(False)
            #     he_pump_state.set_value(False)
            #     ov_state.set_value(False)
            #     co2_state.set_value(False)
            #     he_iv_state.set_value(False)
            #     he_ov_state.set_value(False)
            #     ul_value.set_value(False)
            #     dl_value.set_value(False)
            #     init_btn.set_value(False)
            time.sleep(0.5)
    except KeyboardInterrupt:
        server.stop()
