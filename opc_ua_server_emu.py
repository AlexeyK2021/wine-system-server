import opcua
import random
import time

server = opcua.Server()
server.set_endpoint("opc.tcp://192.168.1.101:4841")

idx = server.register_namespace("opc.tcp://192.168.1.101:4841")
server.start()

objects = server.get_objects_node()
temp_sensor = objects.add_object(idx, "Temperature Sensor")

status = temp_sensor.add_variable(idx, "Status", True)
status.set_writable(writable=True)

temp = temp_sensor.add_variable(idx, "Temperature", 18)
temp.set_writable(writable=True)

if __name__ == '__main__':
    try:
        while True:
            temp.set_value(random.randrange(18, 24))
            time.sleep(5)
    except KeyboardInterrupt:
        server.stop()
