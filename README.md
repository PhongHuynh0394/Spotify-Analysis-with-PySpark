# Prefect Branch !!

New features added:
- Makefile (alias command)
- prefect-compose.yml (docker compose for prefect)
- pyspark installed (Updated Dockerfile)

=> Newest: Added connecting mongodb flow

## To Test Prefect

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

# PySpark

# Spotify Crawl Data

## Introduction

Crawl songs information of artists from [The Top 1000 Artists of All Time](https://www.acclaimedmusic.net/061024/1948-09art.htm).

For each artist name, we will use Spotify Api to extract all albums of him/her. In each album, all songs is going to be scraped to extract features such as `id`, `name`, ...

## Usage

Run the code:

```python=
python main.py -s <index_start> -e <index_end> -ts <number_of_artists_in_each_thread>
```

For example:

```python=
python main.py -s 0 -e 4 -ts 1
```

## Result

The artist, album, song and genre data will be stored in MongoDB Cloud.
