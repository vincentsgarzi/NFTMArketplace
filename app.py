import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
#from Vinny.app import load_and_preprocess_single_image
#from keras.models import load_model
from Kunal.pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json
import uuid

load_dotenv()

st.set_page_config(page_title="NFT Marketplace")

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

@st.cache(allow_output_mutation=True, suppress_st_warning=True)
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

def pin_artwork(artwork_name, artwork_file):

    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(artwork_file.getvalue())

    # Build a token metadata file for the artwork
    token_json = {
        "name": artwork_name,
        "image": ipfs_file_hash
    }

    json_data = convert_data_to_json(token_json)

    # Pin the json to IPFS with Pinata
    json_ipfs_hash = pin_json_to_ipfs(json_data)

    return json_ipfs_hash

#
def pin_appraisal_report(report_content):
    json_report = convert_data_to_json(report_content)
    report_ipfs_hash = pin_json_to_ipfs(json_report)
    return report_ipfs_hash


#
def add_to_cart(token_id, user_address, cart):
    if token_id not in cart:
        cart.append(token_id)
        nft_name = preset_nfts[index]['name']
        st.sidebar.write(f"You have added the **:blue[{nft_name}]** NFT to your cart.")

#
def buy_nfts(cart, user_address):
    for token_id in cart:
        # Get the price of the NFT based on the token_id
        price = next(nft['price'] for nft in preset_nfts if nft['token_id'] == token_id)
        tx_hash = contract.functions.purchaseArtwork(token_id).transact({'from': user_address, 'value': w3.toWei(price, 'ether')})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        st.sidebar.write("Transaction receipt for NFT", token_id)
        st.sidebar.write(dict(receipt))
    cart.clear()



# Define preset NFTs
preset_nfts = [
    {
        'name': 'Acorn Head',
        'artist': 'DoVhichi',
        'image_path': 'NFT_Images/download-1.png',
        'price': 3.4,
        'token_id': 1
    },
    {
        'name': 'Heart Cat',
        'artist': 'Milton',
        'image_path': 'NFT_Images/download-2.png',
        'price': 2.0,
        'token_id': 2
    },
    {
        'name': 'Pixel Pizza',
        'artist': 'Chef Roonie',
        'image_path': 'NFT_Images/download-3.png',
        'price': 8.2,
        'token_id': 3
    },
    {
        'name': 'Slob Monster',
        'artist': 'Joe Joe',
        'image_path': 'NFT_Images/download-4.png',
        'price': 1.7,
        'token_id': 4
    },
    {
        'name': 'Ninja Turtle',
        'artist': 'MichaelAngelo',
        'image_path': 'NFT_Images/download-5.png',
        'price': 5.3,
        'token_id': 5
    },
    {
        'name': 'Naruto',
        'artist': 'Masashi Kishimoto',
        'image_path': 'NFT_Images/download-6.png',
        'price': 9.3,
        'token_id': 6
    },
    {
        'name': 'Halo Wolf',
        'artist': 'Jason Jones',
        'image_path': 'NFT_Images/download-7.png',
        'price': 7.4,
        'token_id': 7
    },
    {
        'name': 'Happy Car',
        'artist': 'Henry Ford',
        'image_path': 'NFT_Images/download-9.png',
        'price': 4.0,
        'token_id': 8
    },
    {
        'name': 'TV Head',
        'artist': 'Philo Farnsworth',
        'image_path': 'NFT_Images/download-10.png',
        'price': 5.9,
        'token_id': 9
    },
    {
        'name': 'Rainbow Box',
        'artist': 'Clifrton',
        'image_path': 'NFT_Images/download-12.png',
        'price': 4.7,
        'token_id': 10
    },
    {
        'name': 'Patty Man',
        'artist': 'The Burger King',
        'image_path': 'NFT_Images/download-11.png',
        'price': 2.7,
        'token_id': 11
        }]


with st.sidebar:
    st.title('Purchase NFT')

    # Select user account
    user_address = st.selectbox("Select the account you wish to use.", options=w3.eth.accounts)

    # Cart
    cart = []

    # Function to calculate total cost
    def calculate_total_cost():
        total_cost = sum(nft['price'] for nft in preset_nfts if nft['token_id'] in cart)
        return total_cost

    # Display NFTs in the cart and total cost
    st.title('Your Cart:')

tab1, tab2 = st.tabs(['Marketplace', 'Build Your Own NFT'])

cart_placeholder = st.sidebar.empty()


with tab1:

    st.title('NFT Marketplace')
    with st.expander('Welcome to our NFT Marketplace!'):
        st.write("Explore a diverse collection of unique and valuable NFTs created by talented artists and creators from around the world. Immerse yourself in a world of digital art, collectibles, and more. Browse through our curated selection of NFTs, each with its own distinctive style and story. Discover rare and one-of-a-kind pieces that resonate with your taste and passion. With a seamless buying experience, you can securely purchase your favorite NFTs using cryptocurrency.")   

    st.title('')

    user_nfts = []

    col_count = 4
    row_count = (len(preset_nfts) // col_count) + 1

    for i in range(row_count):
        cols = st.columns(col_count, gap='large')
        for j in range(col_count):
            index = i * col_count + j
            if index < len(preset_nfts):
                nft = preset_nfts[index]
            else:
                break

            with cols[j]:
                image = Image.open(nft["image_path"])
                st.image(image, caption=nft["name"], use_column_width=True)
                st.write(f"Artist: {nft['artist']}")
                st.write(f"Price: {nft['price']} ETH")

                nft_id = nft['token_id']
                button_key = f"Add to Cart {nft_id}"
                added_to_cart = nft_id in cart

                if added_to_cart:
                    st.text("Added to Cart")
                elif st.button("Add to Cart", key=button_key):
                    add_to_cart(nft_id, user_address, cart)
                    cart.append(nft_id)


# Update the total cost in the sidebar
total_cost = calculate_total_cost()
st.sidebar.write(f"Total Cost: {total_cost} ETH")

st.sidebar.write(f'**Do you wish to purchase the selected NFT?**')

if st.sidebar.button("Purchase"):
    buy_nfts(cart, user_address)
    st.sidebar.write("NFTs purchased successfully!")
    cart.clear()



with tab2:
    st.title("Art Registry Appraisal System")
    accounts = w3.eth.accounts
    address = st.selectbox("Choose an account to get started.", options=accounts)
    st.markdown("---")

    ################################################################################
    # Register New Artwork
    ################################################################################
    st.markdown("## Register a New Artwork")

    artwork_name = st.text_input("Enter the name of the artwork.")
    artist_name = st.text_input("Enter the artist's name.")

    file = st.file_uploader("Upload Artwork", type=["jpg", "jpeg", "png"])

    if file is not None:
        image = Image.open(file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)
        st.write("")
        st.write("Classifying...")

        # Preprocess the uploaded image
        data = load_and_preprocess_single_image(file)

        # Make a prediction
        model = load_model('Vinny/my_model.h5')
        prediction = model.predict(data)
        prediction = prediction.item(0)*10
        st.write("The estimated value of your NFT is: %.2f Ether" % prediction)
        st.write("You may list your NFT for sale at +/- ten percent of the estimate")
        initial_appraisal_value = st.slider(label="Listing Price, in Ether", min_value=(prediction*.9), max_value=(prediction*1.1))

    if st.button("Register Artwork"):
        artwork_ipfs_hash =  pin_artwork(artwork_name,file)
        artwork_uri = f"ipfs://{artwork_ipfs_hash}"
        tx_hash =contract.functions.registerArtwork(
            address,
            artwork_name,
            artist_name,
            initial_appraisal_value,
            artwork_uri
        ).transact({'from': address, 'gas': 1000000})

        receipt=w3.eth.wait_for_transaction_receipt(tx_hash)
        st.write("Transaction receipt")
        st.write(dict(receipt))

        st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
        st.markdown(f"[Artwork IPFS Gateway Link](https://ipfs.io/ipfs/{artwork_ipfs_hash})")

        preset_nfts.append({
            'name': artist_name,
            'artist': artist_name,
            'image_path': file.name,
            'price': 2
        })

    st.markdown("---")

    st.markdown("## Display an Art Token")
    st.write(address)
    tokens = contract.functions.balanceOf(address).call()
    st.write(f"This address owns {tokens} tokens.")
    token_id = st.selectbox("Artwork Tokens", list(range(tokens)))
    if st.button("Display"):
        # Use the contract's `ownerOf` function to get the art token owner
        owner = contract.functions.ownerOf(token_id).call()
        st.markdown("**The token address is**")
        st.write(f"{owner}")
        # Use the contract's `tokenURI` function to get the art token's URI
        token_uri = contract.functions.tokenURI(token_id).call()
        st.write(f"The tokenURI is {token_uri}")
        st.image(file)
