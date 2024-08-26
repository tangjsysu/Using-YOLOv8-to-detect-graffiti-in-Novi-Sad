from inference_sdk import InferenceHTTPClient
from PIL import Image
import os
from tqdm import tqdm
import csv

# Initialize the client
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="1pf40uMIYBGW6fNDaym7"
)

# Path to the folder containing the images
csv_file_path = '../data/pred_minus.csv'
imgpath = "D:/UZH/24spring/gisproject/streetview_minus"
imgs = os.listdir("D:/UZH/24spring/gisproject/streetview_minus")
graffiti_name = []

# Write the header of the csv file
for imgName in tqdm(imgs,desc="Processing"):
    img_path = imgpath + '/' + imgName
    img= Image.open(img_path)
    try:
        # Perform inference
        result = CLIENT.infer(img, model_id="graffiti-5sa0t/1")
        if len(result['predictions']) != 0:
            with open(csv_file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([imgName])
            graffiti_name.append(imgName)
    except Exception as e:
        print(f"An error occurred while getting location for photo {imgName}: {e}")


print("CSV file has already been written:", csv_file_path)
