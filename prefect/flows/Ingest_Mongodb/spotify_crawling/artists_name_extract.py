from alive_progress import alive_bar
import requests
from bs4 import BeautifulSoup


# Define URLs
URLS = ("https://www.acclaimedmusic.net/061024/1948-09art.htm",
        "https://www.acclaimedmusic.net/061024/1948-09art2.htm",
        "https://www.acclaimedmusic.net/061024/1948-09art3.htm",
        "https://www.acclaimedmusic.net/061024/1948-09art4.htm",
        "https://www.acclaimedmusic.net/061024/1948-09art5.htm")

# Define path to store list of artists name
FILE_PATH = "data/artists_names.txt"


def get_artists_name(urls):
    """_summary_:
    Get artists name from URLs

    Args:
        urls (tuple): Tuple of URLs

    Returns:
        artists_name (list): List of artists name
    """
    artists_name = []
    # Send an HTTP GET request to the web page
    with alive_bar(len(urls)) as bar:
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
            bar()

    # Drop element "Album" in artists_name
    artists_name = set(artists_name)
    artists_name.remove("Albums")
    return artists_name


def store_artists_name(artists_name, file_name = FILE_PATH):
    """_summary_

    Args:
        artists_name (list): List of artists name
    """
    # Write artists_name to file using pickle
    with open(file_name, 'w') as f:
        for artist_name in artists_name:
            f.write(artist_name + "\n")



def artists_crawler(path = FILE_PATH):
    """_summary_:
    Main function
    """
    artists_name = get_artists_name(URLS)
    store_artists_name(artists_name, path)


if __name__ == "__main__":
    print("Start")
    artists_crawler()
    print("Success")
