## This program contains the functions for pinning files to IPFS via Pinata


## The os and dotenv libraries are needed for loading our Pinata API keys.
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

# Pinata requires authentication headers for any request to the API. The headers include the 
# Pinata API keys that we loaded via the dotenv library.
# We need two types of headers: file and JSON

file_headers = {
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_SECRET_API_KEY"),
}

# We use these new headers to create a Python post request that can send files to Pinata via the 
# API. The 'r' code uses the pinFileToIPFS API endpoint to pin a file
# The helper function named pin_file_to_ipfs makes it easier for the requests.post to be used

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

# To use this function from our dApp, we use the Streamlit file uploader component. 
# The app.py file contains the code that uses Streamlit and Web3.py to allow users to interact 
# with the contract from a webpage, so this component will be added to that file. The uploader 
# component lets users upload files and send them to Pinata.

# An additional enhancement to the file upload to IPFS through dApp, is the ability to upload the 
# metadata for the file.

# The process for sending JSON data to Pinata slightly differs from the one for sending artwork 
# files.
# For this we
# a. Create headers for PINATA API
# b. Create a function that posts the metadata to Pinata
# c. specify the CID version

# CREATE HEDERS FOR PINATA API

headers = {
    "Content-Type": "application/json",
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_SECRET_API_KEY"),
}

# The dictionary contains the required values for our JSON headers. For the last two values, it 
# uses the API keys that we previously defined in our .env file.

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

# To confirm the endpoint for pinning json review https://docs.pinata.cloud/#PinJSONToIPFS 
# Pinata API, Pin JSON page

# SPECIFY CONTENT IDENTIFIER VERSION

# To use the Pinata API, we need to specify the content identifier (CID) version for the JSON 
# data that we send. This tells IPFS what kind of hash to generate.
# We convert python dictionary 'data' into a JSON string

def convert_data_to_json(content):
    data = {"pinataOptions": {"cidVersion": 1}, "pinataContent": content}
    return json.dumps(data)
