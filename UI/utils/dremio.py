import pyarrow
from pyarrow import flight
import pandas as pd

class DremioClient:
    def __init__(self, host, port, uid, pwd) -> None:
        self._host = host
        self._port = port
        self._uid = uid
        self._pwd = pwd

    def connect(self):
        self._client = flight.FlightClient(f"grpc://{self._host}:{self._port}")

    def authenticate(self):
        bearer_token = self._client.authenticate_basic_token(
            self._uid, self._pwd)
        options = flight.FlightCallOptions(headers=[bearer_token])
        return options

    def query(self, sql, options):
        info = self._client.get_flight_info(
            flight.FlightDescriptor.for_command(sql), options=options)
        reader = self._client.do_get(info.endpoints[0].ticket, options=options)
        df = reader.read_all().to_pandas()
        return df


if __name__ == "__main__":
    client = DremioClient()
    client.connect()
    options = client.authenticate()
    location = "home.tracks"
    df = client.query(
        f"SELECT * FROM {location}", options)
    print(df.head())
