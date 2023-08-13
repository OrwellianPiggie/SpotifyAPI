from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()
client_id=os.getenv("CLIENT_ID")
client_secret=os.getenv("CLIENT_SECRET")


def get_token():
    auth_string= client_id+ ":" +client_secret
    auth_bytes=  auth_string.encode("utf-8")
    auth_base64= str(base64.b64encode(auth_bytes),"utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization" : "Basic " + auth_base64,
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    data = { "grant_type":"client_credentials" }
    result = post(url,headers=headers, data=data)
    json_result= json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query
    result = get(query_url,headers=headers)
    json_result= json.loads(result.content)["artists"]["items"]
    if len(json_result)==0:
        print("No Result Found.")
        return None
    return json_result[0]
    
def everything_artist(token,artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query
    result = get(query_url,headers=headers)
    json_result= json.loads(result.content)["artists"]["items"]
    uri = result["uri"]
    return uri


token = get_token()
name = input("Enter the artist you need to search: ")
print("Searching for: ",name)
result = search_artist(token,name)
print("Name:",result["name"])
print("Popularity:",result["popularity"])
print("Type:",result["type"])
print("URI:",result["uri"])
print("Genre:",result["genres"])
result2 = everything_artist(token,name)
