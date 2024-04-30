from opcua import Client


def get_value(ip, port, node_id, name):
    client = Client(f"opc.tcp://{ip}:{port}")
    try:
        client.connect()
        # root = client.get_root_node()
        sensor = client.get_node(node_id)
        value = sensor.get_value()
        client.disconnect()
        return value
    except ConnectionRefusedError:
        print(f"{name} ({ip}:{port}) недоступен")
        return None


def set_value(ip, port, node_id, value, name):
    client = Client(f"opc.tcp://{ip}:{port}")
    try:
        client.connect()
        # root = client.get_root_node()
        sensor = client.get_node(node_id)
        sensor.set_value(value)
        client.disconnect()
    except ConnectionRefusedError:
        print(f"{name} ({ip}:{port}) недоступен")


def check_sensor(sensor):
    if get_value(sensor.ip, sensor.port, sensor.node_id, sensor.name) is not None:
        return True
    return False


def check_actuator(actuator):
    if get_value(actuator.ip, actuator.port, actuator.state_node_id, actuator.name) is not None:
        return True
    return False

# def set_value(actuator, value):
#     # set_value(actuator.ip, actuator.port, actuator.cmnd_node_id, value)
#     ip = actuator.ip
#     port = actuator.port
#     node_id = actuator.cmnd_node_id
#     client = Client(f"opc.tcp://{ip}:{port}")
#     try:
#         client.connect()
#         # root = client.get_root_node()
#         sensor = client.get_node(node_id)
#         sensor.set_value(value)
#         client.disconnect()
#     except ConnectionRefusedError:
#         print("Cant connect to sensor")


# if __name__ == '__main__':
#     ip = "127.0.0.1"
#     port = 4841
#     node_id = "ns=2;i=6"
#     last_val = 0
#     while 1:
#         new_val = get_value(ip, port, node_id)
#         if last_val != new_val:
#             print(new_val)
#             last_val = new_val
# client = Client("opc.tcp://127.0.0.1:4841")
# # client = Client("opc.tcp://admin@localhost:4840/freeopcua/server/") #connect using a user
# while True:
#     try:
#         client.connect()
#
#         root = client.get_root_node()
#         # print("Objects node is: ", root)
#         # print("Children of root are: ", root.get_children())
#         temp_sensor = client.get_node("ns=2;i=6")
#         print(f"Temp={temp_sensor.get_value()}")
#         client.disconnect()
#
#     except ConnectionRefusedError:
#         print("Can't connect to OPC server")
#     sleep(5)
