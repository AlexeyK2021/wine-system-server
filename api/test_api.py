import random
import time

from influxdb_client import Point
from influxdb_client.client import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

from config import INF_IP, INF_TOKEN, INF_ORG, INF_PORT, INF_BUCKET

url = f"http://{INF_IP}:{INF_PORT}"
client = influxdb_client.InfluxDBClient(url=url, token=INF_TOKEN, org=INF_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()


def generate_data():
    for value in range(1000):
        temp = (
            Point("Tank1")
            .tag("Type", "Sensor")
            .tag("Name", "Temperature")
            .field("Value", random.randrange(18, 24))
        )
        pres = (
            Point("Tank1")
            .tag("Type", "Sensor")
            .tag("Name", "Pressure")
            .field("Value", random.randrange(95, 105))
        )
        hl = (
            Point("Tank1")
            .tag("Type", "Sensor")
            .tag("Name", "High_Level_Sensor")
            .field("Value", random.randrange(0, 2))
        )
        ll = (
            Point("Tank1")
            .tag("Type", "Sensor")
            .tag("Name", "Low_Level_Sensor")
            .field("Value", random.randrange(0, 2))
        )
        input = (
            Point("Tank1")
            .tag("Type", "Actuator")
            .tag("Name", "Input_Valve")
            .field("State", random.randrange(0, 2))
        )
        heiv = (
            Point("Tank1")
            .tag("Type", "Actuator")
            .tag("Name", "HE_Input_Valve")
            .field("State", random.randrange(0, 2))
        )
        heov = (
            Point("Tank1")
            .tag("Type", "Actuator")
            .tag("Name", "HE_Output_Valve")
            .field("State", random.randrange(0, 2))
        )
        co2 = (
            Point("Tank1")
            .tag("Type", "Actuator")
            .tag("Name", "CO2_Valve")
            .field("State", random.randrange(0, 2))
        )
        ov = (
            Point("Tank1")
            .tag("Type", "Actuator")
            .tag("Name", "Output_Valve")
            .field("State", random.randrange(0, 2))
        )
        hep = (
            Point("Tank1")
            .tag("Type", "Actuator")
            .tag("Name", "HE_Pump")
            .field("State", random.randrange(0, 2))
        )
        op = (
            Point("Tank1")
            .tag("Type", "Actuator")
            .tag("Name", "Output_Pump")
            .field("State", random.randrange(0, 2))
        )
        write_api.write(bucket=INF_BUCKET, org=INF_ORG, record=temp)
        write_api.write(bucket=INF_BUCKET, org=INF_ORG, record=pres)
        write_api.write(bucket=INF_BUCKET, org=INF_ORG, record=hl)
        write_api.write(bucket=INF_BUCKET, org=INF_ORG, record=ll)

        write_api.write(bucket=INF_BUCKET, org=INF_ORG, record=input)
        write_api.write(bucket=INF_BUCKET, org=INF_ORG, record=heiv)
        write_api.write(bucket=INF_BUCKET, org=INF_ORG, record=heov)
        write_api.write(bucket=INF_BUCKET, org=INF_ORG, record=co2)
        write_api.write(bucket=INF_BUCKET, org=INF_ORG, record=ov)
        write_api.write(bucket=INF_BUCKET, org=INF_ORG, record=hep)
        write_api.write(bucket=INF_BUCKET, org=INF_ORG, record=op)
        time.sleep(1)


if __name__ == '__main__':
    generate_data()
