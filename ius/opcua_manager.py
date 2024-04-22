import time
from time import sleep

from opcua import Client


class TempHandler(object):
    def datachange_notification(self, node, val, data):
        print("Python: New data change event", node, val)

    def event_notification(self, event):
        print("Python: New event", event)


if __name__ == '__main__':
    client = Client("opc.tcp://127.0.0.1:4841")
    # client = Client("opc.tcp://admin@localhost:4840/freeopcua/server/") #connect using a user
    while True:
        try:
            client.connect()

            root = client.get_root_node()
            # print("Objects node is: ", root)
            # print("Children of root are: ", root.get_children())
            temp_sensor = client.get_node("ns=2;i=6")
            print(f"Temp={temp_sensor.get_value()}")
            client.disconnect()

        except ConnectionRefusedError:
            print("Can't connect to OPC server")
        sleep(5)
