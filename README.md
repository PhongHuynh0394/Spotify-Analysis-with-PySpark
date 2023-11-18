# Prefect Branch !!

## Set up

### Environment

Firstly, you need to create a .env file base on env_template file by the following command:
```bash
cp env_template .env
```

make sure you fill all your API key and MongoDB user in this blank:
```bash
# Mongodb
MONGODB_USER=root
MONGODB_PASSWORD=123
MONGODB_DATABASE=crawling-data

# Spotify
SPOTIFY_CLIENT_ID = "54f4b6f05cdb44b592f89654412d3a39"
SPOTIFY_CLIENT_SECRET = "b9acf2b35cf44ee982efa8c05efc7d45"
```
## Building services
To build all services, run:
```bash
make build
```
Then just take a cup of coffee and wait Docker do the rest. After building, now you can 
easily run the system by typing `make up` in your terminal.

## To Test Prefect ONLY

`This note is for testing Prefect Only`

To make sure you have newest updated, please pull (or clone) this branch, then remove the old prefect image in your Docker Desktop (if you already had one)

But if you don't use Docker Desktop, you can follow these commandline instead to remove your old Prefect image:
```bash
docker images | grep prefect | awk '{print $3}' | xargs docker rmi
```
Then re-build the new prefect image

Run the following command:
```bash
make prefect-build
```
This will build a prefect images with requirements.txt in prefect folder

Wait for a second for everything build up, then start services: `make prefect-up`

Reversely, run `make prefect-down` to turn off services

Check [**localhost:4200**](http://localhost:4200) to visit Prefect UI. You will see there is a flow already in `flows run` or `Deployments` section. 

**To Run pipeline:** Just trigger the `Run` button on prefect UI, there is 1 sample basic flow and 1 schedule flow for auto run

**Pipeline Structure Files:**
- Sample flow: [main_flow.py](./prefect/flows/main_flow.py) (This file has 2 flows)
- Sample tasks: [sample_task.py](./prefect/flows/sample_task.py) (this file also has 2 tasks)
- Mongodb connection task: [mongodb_task.py](./prefect/flows/Ingest_Mongodb/mongodb_task.py)
- ELT Ingest data from MongoDB to Hadoop: [bronze_layer.py](./prefect/flows/ELT_pipeline/bronze_layer.py)


Checkout the data from Mongodb Atlas Cloud
