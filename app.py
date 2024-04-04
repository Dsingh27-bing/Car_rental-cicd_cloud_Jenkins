import base64
import io
from flask import Flask, render_template, request, redirect, session, url_for

from pymongo import MongoClient
import random
from datetime import datetime
from bson.binary import Binary
#from PIL import Image
app = Flask(__name__)
app.secret_key = 'DriveNow'
client = MongoClient('mongodb+srv://Dimple_singh:Dimple%401197@drivenow01.v3vlstx.mongodb.net/')
db = client['Termination_project']

car_doc=[]
Car_collection = db.CarData
Booking_collection=db.BookingData

@app.route('/')
def home():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    else:
        return render_template('index.html')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    if request.method=='POST':
        return login_post()
    
def login_post():
    username = request.form['username']
    print("username: ",username)
    
    password = request.form['password']
    print('password: ',password)
    
    # Assuming you have already created the MongoDB connection
    user = db.Users.find_one({'username': username, 'password': password})
    if user:
        print("Successful validation")
        session['username'] = username
        return redirect('/cars')
    else:
        print("Error")
        return render_template('login.html', error='Invalid username or password.')

@app.route('/createaccount', methods=['GET','POST'])
def create_account():
    if request.method=='GET':
        return render_template('CreateAccount.html')
    if request.method=='POST':
        return create_account_post()

def create_account_post():
    name = request.form['name']
    email = request.form['email']
    contact_num= request.form['Contact Number']
    dob = request.form['Date Of Birth']
    address= request.form['Address']
    dl= request.form['Driving license Number']
    username = request.form['Username']
    password = request.form['Password']
    document = {
    'name': name,
    'email': email,
    'Contact Number':contact_num,
    'Date Of Birth': dob,
    'Address': address,
    'Driving license Number': dl,
    'username': username,
    'password': password
}
    db.Users.insert_one(document)
    return redirect('/login')

@app.route('/cars', methods=['GET','POST'])
def cars():
    if request.method=='GET':
        
        error = request.args.get('error', None)
        for cars in Car_collection.find():
            car = {
                'serial_number':cars['serial_number'],
                'car_name':cars['car_name'],
                'car_model_year':cars['car_model_year'],
                'car_ignition':cars['car_ignition'],
                'car_connectively':cars['car_connectively'],
                'car_drive_mode':cars['car_drive_mode'],
                'car_control_mode':cars['car_control_mode'],
                'car_stereo':cars['car_stereo'],
                'car_air_condition':cars['car_air_condition'],
                'car_image_path':cars['car_image_path'],
                'car_bag_count':cars['car_bag_count'],
                'car_seat_count':cars['car_seat_count'],
                'car_price_per_hour':cars['car_price_per_hour'],
                'car_insurance_included':cars['car_insurance_included'],
                'car_actual_name':cars['car_actual_name']
            }
            car_doc.append(car)
        return render_template('Cars.html',username=session['username'],car_doc=car_doc,error=error)
    if request.method=='POST':
        return redirect(url_for(filter_images))

    
    

@app.route('/bookingform', methods=['GET','POST'])
def booking_form():
    if request.method=='GET':
        random_number = random.randint(1000, 9999)
        booking_id = "B00"+str(random_number)
        document = db.Users.find_one({'username': session['username']})
        return render_template('BookingForm.html',document=document,booking_id=booking_id)
    

    if request.method=='POST':
        print("POST bookingform")
        random_number = random.randint(1000, 9999)
        booking_id = "B00"+str(random_number)
        document = db.Users.find_one({'username': session['username']})
        car_serial_number=request.form['car_serial_number']
        session['booked_car_serial_num']=car_serial_number
        book_car_collection=db['CarData']
        car_book=book_car_collection.find_one({"serial_number":int(car_serial_number)})
        booking_from_date=session['FromDate'].strftime('%m-%d-%Y')
        booking_to_date=session['ToDate'].strftime('%m-%d-%Y')
        delta = abs(session['ToDate'] - session['FromDate'])
        num_days = delta.days
        car_price_per_hour = car_book['car_price_per_hour']
        amount = car_price_per_hour * num_days * 24

        return render_template('BookingForm.html',document=document,booking_id=booking_id,car_book=car_book,from_date=booking_from_date,to_date=booking_to_date,num_days=num_days, amount=amount,username=session['username'])

@app.route('/yourbooking', methods=['GET','POST'])
def yourbooking():
    
    booking_data = {
        'BookingId':request.form.get('BookingId'),
        'FirstName':request.form.get('FirstName'),
        'Email':request.form.get('Email'),
        'ContactNumber':request.form.get('ContactNumber'),
        'CarBooked':request.form.get('CarBooked'),
        'InTime':request.form.get('InTime'),
        'OutTime':request.form.get('OutTime'),
        'NumberOfDays':request.form.get('NumberOfDays'),
        'Amount':request.form.get('Amount')
    }

    in_time=request.form.get('InTime')
    out_time=request.form.get('OutTime')

    in_time_dt=datetime.strptime(in_time, "%m-%d-%Y")
    #in_time_ts = in_time_dt.isoformat(timespec='milliseconds') + "+00:00"
    in_time_ts=datetime.combine(in_time_dt.date(), datetime.min.time())

    out_time_dt=datetime.strptime(out_time, "%m-%d-%Y")
    #out_time_ts = out_time_dt.isoformat(timespec='milliseconds') + "+00:00"
    out_time_ts=datetime.combine(out_time_dt.date(), datetime.min.time())
    
    booking_table_data= {
        'BookingId':request.form.get('BookingId'),
        'username':session['username'],
        'serial_number':int(session['booked_car_serial_num']),
        'booking_start_date':in_time_ts,
        'booking_end_date':out_time_ts,
        'NumberOfDays':request.form.get('NumberOfDays'),
        'Amount':request.form.get('Amount'),
        'CarBooked':request.form.get('CarBooked')
    }
    db.BookingData.insert_one(booking_table_data)

    current_booking_query = {
            "username": {"$eq": session['username']},
            "BookingId": {"$eq": request.form.get('BookingId')}
        }
        
    current_booking=[]
    for booking in Booking_collection.find(current_booking_query):
        current_booking = {
                'BookingId':booking['BookingId'],
                'username':booking['username'],
                'CarBooked':booking['CarBooked'],
                'booking_start_date':booking['booking_start_date'].strftime('%m-%d-%Y'),
                'booking_end_date':booking['booking_end_date'].strftime('%m-%d-%Y'),
                'NumberOfDays':booking['NumberOfDays'],
                'Amount':booking['Amount'],
            }
        break  # Stop after finding the first matching booking
            
    return render_template('YourBookingTable.html',username=session['username'], booking_data=[current_booking])

@app.route("/mybookings", methods=["GET","POST"])
def mybookings():
    user_booking_query = {
                    "username": {"$eq": session['username']}
    }
    
    user_total_booking=[]
    for userbookings in Booking_collection.find(user_booking_query):
        user_booking = {
            'BookingId':userbookings['BookingId'],
            'username':userbookings['username'],
            'CarBooked':userbookings['CarBooked'],
            'booking_start_date':userbookings['booking_start_date'].strftime('%m-%d-%Y'),
            'booking_end_date':userbookings['booking_end_date'].strftime('%m-%d-%Y'),
            'NumberOfDays':userbookings['NumberOfDays'],
            'Amount':userbookings['Amount'],
            }
        user_total_booking.append(user_booking)    
    return render_template('YourBookingTable.html',username=session['username'],booking_data=user_total_booking)

@app.route("/filter", methods=["GET","POST"])
def filter_images():
    fromDate = request.form["filterFromDate"]
    toDate = request.form["filterToDate"]
    start_date_obj = datetime.strptime(fromDate, '%Y-%m-%d')
    end_date_obj = datetime.strptime(toDate, '%Y-%m-%d')
    if(start_date_obj<end_date_obj):
        
        session['FromDate']=start_date_obj
        session['ToDate']= end_date_obj      
        booking_query = {
                    "booking_start_date": {"$lte": end_date_obj},
                    "booking_end_date": {"$gte": start_date_obj}
            }
                
        # Retrieve documents from the Booking_collection that match the query
        booking_cursor = Booking_collection.find(booking_query)
  
        # Build the list of excluded serial numbers from the Booking_collection results
        excluded_serial_numbers = [document['serial_number'] for document in booking_cursor]
                
        # Build the query to exclude documents in the Car_collection with the excluded serial numbers
        car_query = {"serial_number": {"$nin": excluded_serial_numbers}}
                
        # Retrieve documents from the Car_collection that do not match the excluded serial numbers

        # Process the results and return them as needed    
        session['filtered_cars'] = car_query
        
        car_results=[]
        for cars in Car_collection.find(session['filtered_cars']):
                car = {
                    'serial_number':cars['serial_number'],
                    'car_name':cars['car_name'],
                    'car_model_year':cars['car_model_year'],
                    'car_ignition':cars['car_ignition'],
                    'car_connectively':cars['car_connectively'],
                    'car_drive_mode':cars['car_drive_mode'],
                    'car_control_mode':cars['car_control_mode'],
                    'car_stereo':cars['car_stereo'],
                    'car_air_condition':cars['car_air_condition'],
                    'car_bag_count':cars['car_bag_count'],
                    'car_seat_count':cars['car_seat_count'],
                    'car_price_per_hour':cars['car_price_per_hour'],
                    'car_insurance_included':cars['car_insurance_included'],
                    'car_actual_name':cars['car_actual_name'],
                    'car_image_path':cars['car_image_path']
                }
                car_results.append(car)
        return render_template('Cars_filtered.html',username=session['username'], car_doc=car_results)
    else:
        return redirect(url_for('cars',error="Start Date should not be greater than End Date"))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/download_pdf')
def download_pdf():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090, debug=True)
