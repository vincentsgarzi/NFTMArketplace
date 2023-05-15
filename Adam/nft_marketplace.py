import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
from Vinny.app import load_and_preprocess_single_image
from keras.models import load_model
from Kunal.pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

@st.cache(allow_output_mutation=True)
def load_contract():
    # Load the contract ABI
    with open(Path('./Kunal/contracts/compiled/artregistry_abi.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract

# Load the contract
contract = load_contract()

# Define preset NFTs
preset_nfts = [
    {
        'name': 'Acorn Head',
        'artist': 'DoVhichi',
        'image_path': 'download-1.png',
        'price': 3.4,
        'token_id': 1
    },
    {
        'name': 'Heart Cat',
        'artist': 'Milton',
        'image_path': 'download-2.png',
        'price': 2.0,
        'token_id': 2
    },
    {
        'name': 'NFT 2',
        'artist': 'Artist 2',
        'image_path': 'download-3.png',
        'price': 8.2,
        'token_id': 4
    },
    {
        'name': 'NFT 2',
        'artist': 'Artist 2',
        'image_path': 'download-4.png',
        'price': 1.7,
        'token_id': 5
    },
    {
        'name': 'NFT 2',
        'artist': 'Artist 2',
        'image_path': 'download-5.png',
        'price': 5.3,
        'token_id': 6
    },
    {
        'name': 'NFT 2',
        'artist': 'Artist 2',
        'image_path': 'download-6.png',
        'price': 9.3,
        'token_id': 7
    },
    {
        'name': 'NFT 2',
        'artist': 'Artist 2',
        'image_path': 'download-7.png',
        'price': 7.4,
        'token_id': 8
    },
    {
        'name': 'NFT 2',
        'artist': 'Artist 2',
        'image_path': 'download-8.png',
        'price': 6.1,
        'token_id': 9
    },
    {
        'name': 'NFT 2',
        'artist': 'Artist 2',
        'image_path': 'download-9.png',
        'price': 4.0,
        'token_id': 10
    },
    {
        'name': 'Mountains',
        'artist': 'Clifrton',
        'image_path': 'download-10.png',
        'price': 2.7,
        'token_id': 3
    }
]

# Sidebar - NFT Purchase
st.sidebar.markdown("## NFT Purchase")
user_address = st.sidebar.selectbox("Select Account", options=w3.eth.accounts)
selected_nft = st.sidebar.selectbox("Select NFT to Purchase", preset_nfts)

if st.sidebar.button("Purchase"):
    token_id = selected_nft['token_id']
    tx_hash = contract.functions.purchaseArtwork(token_id).transact({'from': user_address})

    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.sidebar.write("Transaction receipt")
    st.sidebar.write(dict(receipt))

    # Update user's balance of owned tokens
    tokens = contract.functions.balanceOf(user_address).call()
    st.sidebar.write(f"Updated balance: {tokens} tokens")

# NFT Marketplace tab
st.title("NFT Marketplace")
for nft in preset_nfts:
    nft_image = Image.open(nft['image_path'])
    st.image(nft_image, caption=nft['name'], use_column_width=True)
    st.write(f"Artist: {nft['artist']}")
    st.write(f"Price: {nft['price']} Ether")
    # Hidden input element to store the token ID
    st.write(f"Token ID: {nft['token_id']}", key=f"token_id_{nft['token_id']}", visible=False)
