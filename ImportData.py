import pandas as pd
from pymongo import MongoClient
from bson.binary import Binary
#from PIL import Image
from bson.binary import Binary
#from PIL import Image

# connect to MongoDB server
# client = MongoClient('mongodb://localhost:27017/')

# # select database and collection
# db = client['mydatabase']
# collection = db['mycollection']

conn = MongoClient('mongodb+srv://Dimple_singh:Dimple%401197@drivenow01.v3vlstx.mongodb.net/')

db = conn.Termination_project
collection = db.CarData


# read data from Excel sheet
data = pd.read_excel('CarData.xls')

# # iterate over each row in the data
for index, row in data.iterrows():
#     # read image file
#     img = Image.open(row['car_image_path'])
#     # convert image to binary data
#     img_binary = Binary(img.tobytes())

    # create a document to insert into the collection
    doc = {
        'serial_number': row['serial_number'],
        'car_name': row['car_name'],
        'car_actual_name': row['car_actual_name'],
        'car_model_year': row['car_model_year'],
        'car_ignition': row['car_ignition'],
        'car_connectively': row['car_connectively'],
        'car_drive_mode': row['car_drive_mode'],
        'car_control_mode': row['car_control_mode'],
        'car_stereo': row['car_stereo'],
        'car_air_condition': row['car_air_condition'],
        'car_image_path': row['car_image_path'],
        'availability_start_date':row['availability_start_date'],
        'availability_end_date': row['availability_end_date'],
        'car_bag_count': row['car_bag_count'],
        'car_seat_count': row['car_seat_count'],
        'car_price_per_hour': row['car_price_per_hour'],
        'car_insurance_included': row['car_insurance_included']
    }
    print(doc)
    # insert document into collection
    collection.insert_one(doc)

    # if index==0:
    #     break

conn.close()
