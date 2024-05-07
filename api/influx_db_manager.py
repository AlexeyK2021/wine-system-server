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
    param_name = ["Temperature", "Pressure"]
    param_values = {}
    for name in param_name:
        query = f"""from(bucket: "Ius")
  |> range(start: -30d, stop: -5s)
  |> filter(fn: (r) => r["_measurement"] == "Tank{tank_id}")
  |> filter(fn: (r) => r["Type"] == "Sensor")
  |> filter(fn: (r) => r["Name"] == "{name}")
  |> filter(fn: (r) => r["_field"] == "Value")
  |> aggregateWindow(every: 5s, fn: mean, createEmpty: false)
  |> last()"""
        table = query_api.query(query, org="Mirea")
        param_values[name] = table[0].records[0].get_value()

    #   query = f"""from(bucket: "Ius")
    # |> range(start: -30d, stop: -5s)
    # |> filter(fn: (r) => r["_measurement"] == "Tank{tank_id}")
    # |> filter(fn: (r) => r["Name"] == "Pressure")
    # |> filter(fn: (r) => r["_field"] == "Value")
    # |> aggregateWindow(every: 5s, fn: mean, createEmpty: false)
    # |> last()"""
    #   table = query_api.query(query, org="Mirea")
    #   pres = table[0].records[0].get_value()
    return param_values


def get_current_actuators(tank_id):
    actuator_name = ["Input_Valve", "HE_Input_Valve", "HE_Output_Valve", "CO2_Valve",
                     "Output_Valve", "HE_Pump", "Output_Pump"]
    actuator_values = {}
    for name in actuator_name:
        query = f"""from(bucket: "Ius")
  |> range(start: -30d, stop: -5s)
  |> filter(fn: (r) => r["_measurement"] == "Tank{tank_id}")
  |> filter(fn: (r) => r["Type"] == "Actuator")
  |> filter(fn: (r) => r["Name"] == "{name}")
  |> filter(fn: (r) => r["_field"] == "State")
  |> aggregateWindow(every: 5s, fn: mean, createEmpty: false)
  |> last()"""
        table = query_api.query(query, org="Mirea")
        actuator_values[name] = table[0].records[0].get_value()
        return actuator_values


def generate_data():
    for value in range(10):
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
        write_api.write(bucket=bucket, org="Mirea", record=temp)
        write_api.write(bucket=bucket, org="Mirea", record=pres)
        write_api.write(bucket=bucket, org="Mirea", record=input)
        # write_api.write(bucket=bucket, org="Mirea", record=heiv)
        # write_api.write(bucket=bucket, org="Mirea", record=heov)
        # write_api.write(bucket=bucket, org="Mirea", record=co2)
        # write_api.write(bucket=bucket, org="Mirea", record=ov)
        # write_api.write(bucket=bucket, org="Mirea", record=hep)
        # write_api.write(bucket=bucket, org="Mirea", record=op)
        time.sleep(1)


if __name__ == '__main__':
    # print(get_current_parameters(1))
    # print(get_current_actuators(1))
    # print(get_tank_state(1))
    generate_data()
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
