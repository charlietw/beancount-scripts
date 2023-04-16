from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import os
from dotenv import load_dotenv


def influx_client() -> InfluxDBClient:
    load_dotenv()
    token: str = os.environ["INFLUXDB_TOKEN"]
    host: str = os.environ["INFLUXDB_HOST"]
    org = "org"
    client = InfluxDBClient(url=host, token=token, org=org, debug=False)
    return client


def clear_bucket(measurement: str, bucket_name: str):
    """
    Removes all data in a given bucket
    """

    client: InfluxDBClient = influx_client()
    delete_api = client.delete_api()
    start = "2020-01-01T00:00:00Z"
    stop = "2030-01-01T00:00:00Z"
    delete_api.delete(
        start, stop, f'_measurement="{measurement}"', bucket=f"{bucket_name}", org="org"
    )
    client.close()


def write_to_influx(df, bucket, measurement):
    client: InfluxDBClient = influx_client()
    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket=bucket, record=df, data_frame_measurement_name=measurement)
    client.close()
