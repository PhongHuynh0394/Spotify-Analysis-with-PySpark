import requests
import pickle
from bs4 import BeautifulSoup

artists_name = []

# Send an HTTP GET request to the web page
urls = ("https://www.acclaimedmusic.net/061024/1948-09art.htm",
        "https://www.acclaimedmusic.net/061024/1948-09art2.htm",
        "https://www.acclaimedmusic.net/061024/1948-09art3.htm",
        "https://www.acclaimedmusic.net/061024/1948-09art4.htm",
        "https://www.acclaimedmusic.net/061024/1948-09art5.htm")

for url in urls:
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table
    table = soup.find('table')

    # Extract data from the table
    if table:
        rows = table.find_all('tr')  # Find all table rows
        for row in rows:
            # Find all cells in each row
            cells = row.find_all('td')
            # Extract text from the cells and remove leading/trailing spaces
            artist_name = cells[1].text.strip()
            artists_name.append(artist_name)

# Drop element "Album" in artists_name
artists_name = set(artists_name)
artists_name.remove("Albums")

# Write artists_name to file using pickle
with open('data/artists_name.pkl', 'wb') as f:
    pickle.dump(artists_name, f)
