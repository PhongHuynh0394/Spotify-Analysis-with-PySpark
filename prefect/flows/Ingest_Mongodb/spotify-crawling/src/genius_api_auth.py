from dotenv import load_dotenv
import os


load_dotenv()

CLIENT_ID = os.getenv("GENIUS_CLIENT_ID")
CLIENT_SECRET = os.getenv("GENIUS_CLIENT_SECRET")
TOKEN = os.getenv("GENIUS_TOKEN")
TOKEN_TYPE = 'Bearer'


def get_token():
    return TOKEN_TYPE, TOKEN


def get_auth_header(token_type, access_token):
    '''
    Returns a dictionary of the authorization header
    '''
    return {"Authorization": token_type + " " + access_token}
