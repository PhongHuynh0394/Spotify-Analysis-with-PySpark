from requests import post
import os
import base64
import json


class SpotifyAuth:
    def __init__(self, client_id, client_secret):
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__base_url = 'https://accounts.spotify.com/api/token'

    def __make_request(self, url, headers, data):
        result = post(url, headers=headers, data=data)
        if result.status_code == 200:
            return json.loads(result.content)
        else:
            raise Exception(f"Error: {result.status_code}")

    def __get_token(self):
        auth_string = self.__client_id + ":" + self.__client_secret
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

        url = self.__base_url
        headers = {
            "Authorization": "Basic " + auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        json_result = self.__make_request(url, headers, data)
        access_token, token_type = json_result["access_token"], json_result["token_type"]
        self.__access_token, self.__token_type = access_token, token_type

    def get_auth_header(self):
        self.__get_token()
        return {"Authorization": self.__token_type + " " + self.__access_token}


if __name__ == "__main__":
    # For testing
    sa = SpotifyAuth("65a6dc669c774dfb816832d3918bfa7c",
                     "daf49b177cfc466cbed98a4b61e66a53")
    print(sa.get_auth_header())
