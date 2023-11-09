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
