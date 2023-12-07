# - "9047:9047"   # Web UI (HTTP)
# - "31010:31010" # ODBC/JDBC clients
# - "32010:32010" # Apache Arrow Flight clients
# from dremio_client import init, flight
# import pandas as pd
# host='dremio'
# user='dremio'
# password ='dremio123'
# port = 31010
# client = flight.connect(host, port, user, password) # initialise connectivity to Dremio via config file
# catalog = client.data # fetch catalog
# query = "select * from home.albums"
# df = client.query(query) # query the first 1000 rows of the dataset and return as a DataFrame
# print(df)
# # print(pd.DataFrame(df))
import pyodbc

cnxn = pyodbc.connect("DSN=Dremio ODBC 64-bit", autocommit=True)
cursor = cnxn.cursor()
sql = 'select * from home.albums'
cursor.execute(sql)
r = cursor.fetchall()
if r:
    print(r)
