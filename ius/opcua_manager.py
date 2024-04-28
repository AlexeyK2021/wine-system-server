from time import sleep
from opcua import Client

from ius.models.Actuator import Actuator


def get_value(ip, port, node_id):
    client = Client(f"opc.tcp://{ip}:{port}")
    try:
        client.connect()
        # root = client.get_root_node()
        sensor = client.get_node(node_id)
        value = sensor.get_value()
        client.disconnect()
        return value
    except ConnectionRefusedError:
        print("Cant connect to sensor")
        return None


def set_value(ip, port, node_id, value):
    client = Client(f"opc.tcp://{ip}:{port}")
    try:
        client.connect()
        # root = client.get_root_node()
        sensor = client.get_node(node_id)
        sensor.set_value(value)
        client.disconnect()
    except ConnectionRefusedError:
        print("Cant connect to sensor")


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


if __name__ == '__main__':
    ip = "127.0.0.1"
    port = 4841
    node_id = "ns=2;i=6"
    last_val = 0
    while 1:
        new_val = get_value(ip, port, node_id)
        if last_val != new_val:
            print(new_val)
            last_val = new_val
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
