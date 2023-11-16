# from dotenv import load_dotenv
from requests import post
import os
import base64
import json

# load_dotenv()

# Spotify
# CLIENT_ID = "54f4b6f05cdb44b592f89654412d3a39"
# CLIENT_SECRET = "b9acf2b35cf44ee982efa8c05efc7d45"

# # Genius
# GENIUS_CLIENT_ID = "4XQ6vd3S1wTQ3_zoZOejO_fo2myvIz7nRM9pUHvqRB4Vmf-EeuayDkyJJn_9D7T2"
# GENIUS_CLIENT_SECRET = "bwEMPaI8Jw7wfqcJ_dtZZEy3kEX7Drj9BwG06ZVNyDksSlYBk36Chang1XZEQCqwrN7mV5U2pbZulFO5uMU-qA"
# GENIUS_TOKEN = '13-EEK9WwSQqHOrp4AfqsefgJHQDuSZ7LfroH4hsG6odlu0N2msk9jc6QHHM47p1'

# Define Client ID and Client Secret
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# Define base URL
BASE_URL = 'https://accounts.spotify.com/api/token'


def get_token():
    """_summary_

    Returns:
        tuple: (access_token, token_type)
    """
    auth_string = CLIENT_ID + ":" + CLIENT_SECRET
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = BASE_URL
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    access_token, token_type = json_result["access_token"], json_result["token_type"]
    return access_token, token_type


def get_auth_header(token_type, access_token):
    """_summary_

    Args:
        token_type (str): Token type
        access_token (str): Access token

    Returns:
        str: Authorization header
    """
    return {"Authorization": token_type + " " + access_token}

if __name__ == "__main__":
    access, type_tk = get_token()
    a = get_auth_header(type_tk, access)
    print(a)
