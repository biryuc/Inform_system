# temperature/tasks.py

from influxdb_client import InfluxDBClient
from .models import Temperature
import datetime

def fetch_temperature_data():
    url = "http://localhost:8086"
    token = "IAqkdbzq-c0WHBVbkwQGPAHlltrtCtd_zkaMlqMvJ89rFeihEdZgsSaLDZdY9Zw3p9VTEZYjzHwf_PCXPJlqrg=="
    org = "smarthome"
    bucket = "devices"

    client = InfluxDBClient(url=url, token=token, org=org)
    query_api = client.query_api()

    query = f'from(bucket: "{bucket}") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "temperature")'
    
    result = query_api.query(org=org, query=query)
    
    print(result)

    for table in result:
        for record in table.records:
            temp_value = record.get_value()
            timestamp = record.get_time()
           
            Temperature.objects.create(value=temp_value, timestamp=timestamp)
            
            
    


