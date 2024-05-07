import datetime
import json
import random

import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = "enu1mls7VsdMIyOzVz43qIAfgmGrHyCP2rqZebU0Z7n4HqLT1CWpNwBUjccwxcdoe8wEOOwdkCkHksNUbfBp4g=="
org = "Mirea"
url = "http://192.168.1.112:8086"
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
bucket = "Ius"
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()


def get_tank_state(tank_id):
    data = {"tank_id": tank_id,
            "params": get_current_parameters(tank_id),
            "actuators": get_current_actuators(tank_id)
            }
    json_object = json.dumps(data, indent=4)
    return json_object


def get_current_parameters(tank_id):
    query = f"""from(bucket: "Ius")
  |> range(start: -30d, stop: -5s)
  |> filter(fn: (r) => r["_measurement"] == "Tank{tank_id}")
  |> filter(fn: (r) => r["Name"] == "Temperature")
  |> filter(fn: (r) => r["_field"] == "Value")
  |> aggregateWindow(every: 5s, fn: mean, createEmpty: false)
  |> last()"""
    table = query_api.query(query, org="Mirea")
    print(table[0].records[0].get_value())



def get_current_actuators(tank_id):
    pass


def generate_data():
    for value in range(300):
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
        input = (
            Point("Tank1")
            .tag("Type", "Actuator")
            .tag("Name", "Input Valve")
            .field("State", random.randrange(0, 2))
        )
        write_api.write(bucket=bucket, org="Mirea", record=temp)
        write_api.write(bucket=bucket, org="Mirea", record=pres)
        write_api.write(bucket=bucket, org="Mirea", record=input)
        time.sleep(1)


if __name__ == '__main__':
    get_current_parameters(1)
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
