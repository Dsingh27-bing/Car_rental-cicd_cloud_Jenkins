import os
from PIL import Image
import pandas as pd

# set the path to your image folder
path = r"D:\University Information\Binghamton\Cloud Computing\Cloud Project\webpage\CarImages"

# create an empty list to store the image data
image_data = []

# loop through each file in the folder
for file in os.listdir(path):
    # check if the file is an image
    if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
        # get the image name and path
        image_name = os.path.splitext(file)[0]
        image_path = os.path.join(path, file)

        # open the image using Pillow
        with Image.open(image_path) as img:
            # get the image size
            width, height = img.size

        # add the image data to the list
        image_data.append({"Name": image_name, "Path": image_path, "Width": width, "Height": height})

# create a Pandas dataframe from the image data
df = pd.DataFrame(image_data)

# save the dataframe to an Excel file
df.to_excel("image_data.xlsx", index=False)
