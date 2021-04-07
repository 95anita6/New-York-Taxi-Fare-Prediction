from flask import Flask, request, render_template
import sklearn
import pickle
import pandas as pd
import numpy as np
from geopy import distance
import datetime
from geopy.geocoders import Nominatim

app = Flask(__name__)
model = pickle.load(open("FarePred_xgb.pkl", "rb"))

geolocator = Nominatim(user_agent="app")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/predict", methods = ["GET", "POST"])
def predict():
    if request.method == "POST":

        # Pickup Date and Time
        date_time_pickup = request.form["Pickup_Date_Time"]
#        pickup_time_weekday = pd.to_datetime(date_time_pickup, format="%Y-%m-%dT%H:%M").weekday
        
        pickup_time_hour = pd.to_datetime(date_time_pickup, format ="%Y-%m-%dT%H:%M").hour
        pickup_time_month = pd.to_datetime(date_time_pickup, format ="%Y-%m-%dT%H:%M").month
        pickup_time_year = pd.to_datetime(date_time_pickup, format ="%Y-%m-%dT%H:%M").year
        pickup_time_day = pd.to_datetime(date_time_pickup, format ="%Y-%m-%dT%H:%M").day
        
        date = datetime.datetime(pickup_time_year, pickup_time_month, pickup_time_day)
        pickup_time_weekday = date.weekday()
#        print("pickup time weekday : ", pickup_time_weekday)
        
        # Pickup and Drop location and calculate distance between them
        pickup_at = request.form["Pickup_location"]
        destination_to = request.form["Destination_location"]
        
        pickup_location = geolocator.geocode(pickup_at, timeout=10)
        destination_location = geolocator.geocode(destination_to, timeout=10)
        
        pickup = (pickup_location.latitude, pickup_location.longitude)
        destination = (destination_location.latitude, destination_location.longitude)
#        pickup = (40.721319, -73.844311)
#        destination = (40.712278, -73.841610)
        Distance_inMiles = int(distance.distance(pickup, destination).miles)
        
        # Total number of passengers
        passenger_count = int(request.form["Passenger_count"])

    #     ['passenger_count', 'Distance_inMiles', 'pickup_time_year', 'pickup_time_month',
    #    'pickup_time_weekday', 'pickup_time_hour']
        data = pd.DataFrame([[passenger_count, Distance_inMiles, pickup_time_year, pickup_time_month, pickup_time_weekday, pickup_time_hour]], columns= ['passenger_count', 'Distance_inMiles','pickup_time_year', 'pickup_time_month', 'pickup_time_weekday', 'pickup_time_hour'])
        prediction=model.predict(data)
        
        output=np.round(prediction[0],2)
        return render_template('home.html',prediction_text="Your estimated taxi fare is {} $".format(output))

    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)