import random

import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = "qiSS9A069E3vdfWZFNL3UXR8KVNDaoE4VvywvW3ToDBQKXAnKoscNwfXizJ3hAT_u5PEwzS8Qkj_G4AbG-v0ug=="
org = "Mirea"
url = "http://localhost:8086"
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
bucket = "Ius"
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

if __name__ == '__main__':

    # for value in range(50):
    #     temp = (
    #         Point("Ebb1")
    #         .tag("Param", "Temperature")
    #         .field("Value", random.randrange(18, 25))
    #     )
    #     pres = (
    #         Point("Ebb1")
    #         .tag("Param", "Pressure")
    #         .field("Value", random.randrange(95, 105))
    #     )
    #
    #     write_api.write(bucket=bucket, org="Mirea", record=temp)
    #     write_api.write(bucket=bucket, org="Mirea", record=pres)
    #     time.sleep(1)  # separate points by 1 second
    for value in range(60):
        temp = (
            Point("EBB1")
            .tag("Type", "Sensor")
            .tag("Name", "Temperature")
            .field("Value", random.randrange(18, 24))
        )
        pres = (
            Point("EBB1")
            .tag("Type", "Sensor")
            .tag("Name", "Pressure")
            .field("Value", random.randrange(95, 105))
        )
        input = (
            Point("EBB1")
            .tag("Type", "Actuator")
            .tag("Name", "Input Valve")
            .field("State", random.randrange(0, 2))
        )
        write_api.write(bucket=bucket, org="Mirea", record=temp)
        write_api.write(bucket=bucket, org="Mirea", record=pres)
        write_api.write(bucket=bucket, org="Mirea", record=input)

        # query = """from(bucket: "Ius")
        #  |> range(start: -10m)
        #  |> filter(fn: (r) => r["_measurement"] == "EBB1")
        #  |> filter(fn: (r) => r["Name"] == "Pressure")
        #  |> filter(fn: (r) => r["Type"] == "Sensor")
        # |> filter(fn: (r) => r["_field"] == "Value")"""
        # tables = query_api.query(query, org="Mirea")
        #
        # for table in tables:
        #     for record in table.records:
        #         print(record)
        time.sleep(1)
