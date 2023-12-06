# - "9047:9047"   # Web UI (HTTP)
# - "31010:31010" # ODBC/JDBC clients
# - "32010:32010" # Apache Arrow Flight clients

from dremio_client import init
import pandas as pd

query = "select * from home.tracks limit 1"
client = init() # initialise connectivity to Dremio via config file
df = client.query(query) # query the first 1000 rows of the dataset and return as a DataFrame
df = pd.DataFrame(df)
print(df)
