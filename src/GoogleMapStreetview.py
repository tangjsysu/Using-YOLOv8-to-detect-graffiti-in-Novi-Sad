import requests
from PIL import Image
from io import BytesIO
import csv
from tqdm import tqdm
import pandas as pd
import os

# Read the csv file
df = pd.read_csv('../map/small_area2.csv', sep=',')
folder_path = '../streetview'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
index = df.iloc[:, 0]
latitude = df.iloc[:, -1]
longitude = df.iloc[:, -2]
headingminus = df.iloc[:, -4]
headingplus = df.iloc[:, -5]

# Download the images
for idx, lat, long, h in tqdm(zip(index, latitude, longitude, headingplus)):
    url = f'https://maps.googleapis.com/maps/api/streetview?size=600x300&location={lat}, {long}&heading={h}&fov=50&key=AIzaSyDpPmyazv9yBMHK9QONvvn6akjnYrreFmA'
    print(url)
    response = requests.get(url)
    try:
        image = Image.open(BytesIO(response.content))
        image_path = os.path.join(folder_path, f'plus-{idx}.png')
        image.save(image_path)
    except:
        print('Error')
        continue
