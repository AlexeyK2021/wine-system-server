import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

from config import INF_PORT, INF_IP, INF_ORG, INF_TOKEN, INF_BUCKET

url = f"http://{INF_IP}:{INF_PORT}"
client = influxdb_client.InfluxDBClient(url=url, token=INF_TOKEN, org=INF_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()


def get_tank_state(tank_id):
    return {
        "params": get_current_parameters(tank_id),
        "actuators": get_current_actuators(tank_id)
    }


def get_current_parameters(tank_id):
    param_name = ["Temperature", "Pressure", "High_Level_Sensor", "Low_Level_Sensor"]
    param_values = {}
    for name in param_name:
        query = f"""from(bucket: "{INF_BUCKET}")
  |> range(start: -10s, stop: now())
  |> filter(fn: (r) => r["_measurement"] == "Tank{tank_id}")
  |> filter(fn: (r) => r["Type"] == "Sensor")
  |> filter(fn: (r) => r["Name"] == "{name}")
  |> filter(fn: (r) => r["_field"] == "Value")
  |> last()"""
        table = query_api.query(query, org=INF_ORG)
        param_values[name] = table[0].records[0].get_value()
    return param_values


def get_current_actuators(tank_id):
    actuator_name = ["Input_Valve", "HE_Input_Valve", "HE_Output_Valve", "CO2_Valve",
                     "Output_Valve", "HE_Pump", "Output_Pump"]
    actuator_values = {}
    for name in actuator_name:
        query = f"""from(bucket: "{INF_BUCKET}")
  |> range(start: -30d, stop: now())
  |> filter(fn: (r) => r["_measurement"] == "Tank{tank_id}")
  |> filter(fn: (r) => r["Type"] == "Actuator")
  |> filter(fn: (r) => r["Name"] == "{name}")
  |> filter(fn: (r) => r["_field"] == "State")
  |> last()"""
        table = query_api.query(query, org=INF_ORG)
        actuator_values[name] = table[0].records[0].get_value()
    return actuator_values
