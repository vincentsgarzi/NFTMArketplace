## This program contains the functions for pinning files to IPFS via Pinata


## The os and dotenv libraries are needed for loading our Pinata API keys.
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

file_headers = {
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_SECRET_API_KEY"),
}

def pin_file_to_ipfs(data):
    r = requests.post(
        "https://api.pinata.cloud/pinning/pinFileToIPFS",
        files={'file': data},
        headers=file_headers
    )
    # print(r.json())
    ipfs_hash = r.json()["IpfsHash"]
    # ipfs_hash = r.json()
    return ipfs_hash

# CREATE HEDERS FOR PINATA API

headers = {
    "Content-Type": "application/json",
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_SECRET_API_KEY"),
}

# CREATE FUNCTION THAT POSTS METADATA TO PINATA

def pin_json_to_ipfs(json):
    r = requests.post(
        "https://api.pinata.cloud/pinning/pinJSONToIPFS",
        data=json,
        headers=headers
    )
    # print(r.json())
    ipfs_hash = r.json()["IpfsHash"]
    # ipfs_hash = r.json()
    return ipfs_hash

# SPECIFY CONTENT IDENTIFIER VERSION

def convert_data_to_json(content):
    data = {"pinataOptions": {"cidVersion": 1}, "pinataContent": content}
    return json.dumps(data)
