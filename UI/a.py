# - "9047:9047"   # Web UI (HTTP)
# - "31010:31010" # ODBC/JDBC clients
# - "32010:32010" # Apache Arrow Flight clients

from dremio_client import init
import pandas as pd

query = "select * from home.tracks"
# client = init(simple_client=True) # initialise connectivity to Dremio via config file
client = init() # initialise connectivity to Dremio via config file
# catalog = client.data # fetch catalog
# home = catalog.home.get() # fetch a specific dataset
df = client.query(query) # query the first 1000 rows of the dataset and return as a DataFrame
df = pd.DataFrame(df)
print(df)
# pds = catalog.source.pds.get() # fetch a physical dataset
# pds.metadata_refresh() # refresh metadata on that dataset
