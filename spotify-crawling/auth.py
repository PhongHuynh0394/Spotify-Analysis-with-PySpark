from dotenv import load_dotenv
from requests import post, get
import os
import base64
import json
import csv

load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")


def get_token():
    '''
    Returns a tuple of the access token and token type
    '''
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
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
    '''
    Returns a dictionary of the authorization header
    '''
    return {"Authorization": token_type + " " + access_token}
