from bing_image_downloader import downloader
import pandas as pd
import os

# Define your sports and non-sports keywords
good_keywords = ["dog", "cute dog", "puppy", "small dog", "pet dog", "big dog"]
bad_keywords = ["house", "sports", "travel", "art", "money", "tree", "food", "computer", "code"]

# Initialize an empty DataFrame to store file paths and labels
df = pd.DataFrame(columns=['file_path', 'label'])

# Function to download images and assign labels
def download_and_label_images(keywords, label):
    global df
    for keyword in keywords:
        output_dir = f'valuationEstimator/images'  # unique output directory for each keyword
        downloader.download(keyword, limit=100, output_dir=output_dir, adult_filter_off=True, force_replace=False, timeout=60)
        # iterate through downloaded images and add them to DataFrame
        for image_file in os.listdir(f"{output_dir}/{keyword}"):
            df = df.append({'file_path': os.path.abspath(f"{output_dir}/{keyword}/{image_file}"), 'label': label}, ignore_index=True)

# Download sports-related images
download_and_label_images(good_keywords, 1)

# Download non-sports-related images
download_and_label_images(bad_keywords, 0)

# Save the DataFrame to a CSV file
df.to_csv('image_data.csv', index=False)
