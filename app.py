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

if 'cart' not in st.session_state:
    st.session_state['cart'] = []

#
def pin_appraisal_report(report_content):
    json_report = convert_data_to_json(report_content)
    report_ipfs_hash = pin_json_to_ipfs(json_report)
    return report_ipfs_hash


# Function used to add the items the user wants into a cart
def add_to_cart(nft):
    st.session_state['cart'].append(nft)
    st.sidebar.write(f"You have added the **:blue[{nft['name']}]** NFT to your cart.")

# Calculates the total cost of the items in the cart
def calculate_total_cost(cart):
    total_cost = sum(nft['price'] for nft in st.session_state['cart'])
    return total_cost

# Initiates a purchase with ganache with the items in the cart
def buy_nfts(cart, user_address):
    total_cost = calculate_total_cost(cart)
    balance = w3.eth.get_balance(user_address)

    wei_per_ether = 10 ** 18
    total_cost_wei = int(total_cost * wei_per_ether)

    if balance < total_cost_wei:
         st.sidebar.write("Insufficient balance. Please add funds to your account.")
         return

    else:
        receiver_address = '0xD87fa28d30B2c1bDB140831fD2191aAFb3Bcb084'

        # Prepare the transaction
        transaction = {
            'from': user_address,
            'to': receiver_address,
            'value': total_cost_wei
        }

        # Send the transaction
        tx_hash = w3.eth.send_transaction(transaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        st.sidebar.write("Transaction receipt for NFTs:")
        st.sidebar.write(dict(receipt))

        st.sidebar.write("NFTs purchased successfully!")

model = load_model('Vinny/my_model.h5')
values = []

for image in os.listdir("NFT_images"):
  data = load_and_preprocess_single_image(f"NFT_images/{image}")
  prediction = model.predict(data)
  values.append(prediction[0][0])


# Define preset NFTs
preset_nfts = [
    {
        'name': 'Good Boy',
        'artist': 'Woofles',
        'image_path': 'NFT_Images/download-1.jpg',
        'price': round(values[0], 5),
        'token_id': 1
    },
    {
        'name': 'Heart Cat',
        'artist': 'Milton',
        'image_path': 'NFT_Images/download-2.png',
        'price': round(values[1], 5),
        'token_id': 2
    },
    {
        'name': 'Pixel Pizza',
        'artist': 'Chef Roonie',
        'image_path': 'NFT_Images/download-3.png',
        'price': round(values[2], 5),
        'token_id': 3
    },
    {
        'name': 'Golden',
        'artist': 'Dog Owner',
        'image_path': 'NFT_Images/download-4.jpg',
        'price': round(values[3], 5),
        'token_id': 4
    },
    {
        'name': 'Ninja Turtle',
        'artist': 'MichaelAngelo',
        'image_path': 'NFT_Images/download-5.png',
        'price': round(values[4], 5),
        'token_id': 5
    },
    {
        'name': 'Puppy Smile',
        'artist': 'Masashi Kishimoto',
        'image_path': 'NFT_Images/download-6.jpg',
        'price': round(values[5], 5),
        'token_id': 6
    },
    {
        'name': 'Halo Wolf',
        'artist': 'Jason Jones',
        'image_path': 'NFT_Images/download-7.png',
        'price': round(values[6], 5),
        'token_id': 7
    },
    {
        'name': 'Stick Dog',
        'artist': 'iDog',
        'image_path': 'NFT_Images/download-8.jpg',
        'price': round(values[7], 5),
        'token_id': 8
    },
    {
        'name': 'Small Car',
        'artist': 'Eric Cadena',
        'image_path': 'NFT_Images/download-9.png',
        'price': round(values[8], 5),
        'token_id': 9
    },
    {
        'name': 'TV Head',
        'artist': 'Philo Farnsworth',
        'image_path': 'NFT_Images/download-10.png',
        'price': round(values[9], 5),
        'token_id': 10
    },
    {
        'name': 'Patty Man',
        'artist': 'The Burger King',
        'image_path': 'NFT_Images/download-11.png',
        'price': round(values[10], 5),
        'token_id': 11
    },
    {
        'name': 'Rainbow Box',
        'artist': 'Clifrton',
        'image_path': 'NFT_Images/download-12.png',
        'price': round(values[11], 5),
        'token_id': 12
    },
    {
        'name': 'Slob Monster',
        'artist': 'Joe Joe',
        'image_path': 'NFT_Images/download-13.png',
        'price': round(values[12], 5),
        'token_id': 13
    },
    {
        'name': 'Happy Car',
        'artist': 'Henry Ford',
        'image_path': 'NFT_Images/download-14.png',
        'price': round(values[13], 5),
        'token_id': 14
    }]


with st.sidebar:
    st.title('Purchase NFT')

    # Select user account
    user_address = st.selectbox("Select the account you wish to use.", options=w3.eth.accounts)

    # Display NFTs in the cart and total cost
    st.title('Your Cart:')

tab1, tab2 = st.tabs(['Marketplace', 'Build Your Own NFT'])

with tab2:
    st.title("Art Registry Appraisal System")
    accounts = w3.eth.accounts
    address = st.selectbox("Choose an account to get started.", options=accounts)
    st.markdown("---")

    # Register New Artwork
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

        token_id = 234

        preset_nfts.append({
            'name': artwork_name,
            'artist': artist_name,
            'image_path': file,
            'price': round(initial_appraisal_value, 5),
            'token_id': token_id
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

with tab1:

    st.title('NFT Marketplace')
    with st.expander('Welcome to our NFT Marketplace!'):
        st.write("Explore a diverse collection of unique and valuable NFTs created by talented artists and creators from around the world. Immerse yourself in a world of digital art, collectibles, and more. Browse through our curated selection of NFTs, each with its own distinctive style and story. Discover rare and one-of-a-kind pieces that resonate with your taste and passion. With a seamless buying experience, you can securely purchase your favorite NFTs using cryptocurrency.")

    st.title('')

    dynamic_nfts = []

    all_nfts = preset_nfts + dynamic_nfts  # Combine preset and dynamic NFTs

    col_count = 4
    row_count = (len(all_nfts) // col_count) + 1


    # For loops to display the nessessary info on the NFT Marketplace
    for i in range(row_count):
        cols = st.columns(col_count, gap='large')
        for j in range(col_count):
            index = i * col_count + j
            if index < len(all_nfts):
                nft = all_nfts[index]
            else:
                break

            with cols[j]:
                image = Image.open(nft["image_path"])
                st.image(image, caption=nft["name"], use_column_width=True)
                st.write(f"Artist: {nft['artist']}")
                st.write(f"Price: {nft['price']} ETH")

                if "token_id" in preset_nfts[index]:
                    nft_id = preset_nfts[index]['token_id']
                    button_key = f"Add to Cart {nft_id}"
                    added_to_cart = nft_id in st.session_state['cart']

                    if added_to_cart:
                        st.text("Added to Cart")
                    elif st.button("Add to Cart", key=button_key):
                        add_to_cart(nft)


# Update the total cost in the sidebar
total_cost = calculate_total_cost(st.session_state['cart'])
st.sidebar.subheader(f"Total Cost: **:blue[{total_cost:.2f} ETH]**")

nft_names = []
for nft in st.session_state['cart']:
    nft_names.append(nft["name"])

 # Display the names of NFTs in the cart
if nft_names:
     st.sidebar.subheader("NFTs in Cart:")
     for name in nft_names:
         st.sidebar.markdown(f'**:blue[{name}]**')
else:
     st.sidebar.write("No NFTs in Cart")

st.sidebar.markdown('---')

st.sidebar.subheader('Initiate Puchase?')

if st.sidebar.button("Purchase"):

    # Initiates the purchase of the NFTS in the cart
    buy_nfts(st.session_state['cart'], user_address)
    st.session_state.clear()



