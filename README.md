# New-York-Taxi-Fare-Prediction

This is a machine learning project to predict the taxi fare given the pick up date, pick up location, drop off location and the number of passengers travelling. A fare is a fee paid by the passenger when one uses a public transport which differs from place to place. It is always good to know an estimate of the price one has to pay before the ride.

## Data collection:
The data for this project was collected from Kaggle. Here's the link : https://www.kaggle.com/dansbecker/new-york-city-taxi-fare-prediction.

## Data exploration and analysis:
The given dataset has 50,000 observations for Pick up date and time, Pickup and drop-off locations, passenger counts and the fare amount. Below is the list of colnums that the dataset has:

 - key : Contains date and time stamp 
 - fare_amount : the target variable
 - pickup_datetime : the pickup time for the ride 
 - pickup_latitude : latitude of the pickup location
 - pickup_longitude : longitude of the pickup location
 - dropoff_latitude : latitude of the drop off location
 - dropoff_longitude : longitude of the drop off location
 - passenger_count : the number of passengers for the ride

The target variable follows the below distribution and is positively skewed.


![image](https://user-images.githubusercontent.com/38220315/114553244-114f7180-9c83-11eb-9420-19724aca998d.png)

The fare amount for each of the number of passengers is as below:

![image](https://user-images.githubusercontent.com/38220315/114553789-a488a700-9c83-11eb-8dba-6816e5f0580e.png)

The dataset was analysed by creating new feature pickup_at from date and time having for categorical values as 'Morning', 'Afternoon', 'Evening' and 'Night' to see how the fare amount changes throughout the day. There was not much change in the fare depending on the time of the day. The mean fare amount was similar for all the categories.

Distance from Geopy library was used to calculate the distance between the prick up and the destination address. The distance was calculated in miles. 

Jointplots and heatmap was used to analyse how the fare amounts plotted itself for Distance, pickup_datetime_year, pickup_datetime_month, pickup_datetime_weekday.

The features used for the model building process were : passenger_count, Distance, pickup_time_year, pickup_time_month, pickup_time_weekday, pickup_time_hour.

## Feature Engineering, Feature Selection and Model Building:
The dataset was divided in 80:20 ratio (80 - Training and 20 -Validation) using train_test_split from sklearn.

The data cleaning was started with dropping key column which had the date and time stamp same as the pickup date and time. The rows that had zero value for latitude was also dropped. 

Distance from Geopy allows the latitude values to be in -90 to 90 range. There was a record having latitude value as 401.083332 which was dropped. The distance in miles was alculated from latitude and longitude of the pickup and drop locations. Geopy can calculate geodesic distance between two points using the geodesic distance or the great-circle distance, with a default of the geodesic distance available as the function geopy.distance.distance.  A geodesic distance is the shortest path between two points on a curved
surface.

After calculating distance features 'pickup_longitude', 'pickup_latitude', 'dropoff_longitude' and 'dropoff_latitude' were dropped.

The pickup date time features was used by extracting year, month, weekday and hour from it. The original features was dropped after extraction of relevant information. 

All of the variables were used for model training and building as they seem important for predicting the target variable. The performance metrics Mean absolute error was not good when some choosen variables were used for training.
LinearRegression, DecisionTreeRegressor, XGBRegressor and RandomForestRegressor models were trained with the data. XGB model performed better as compared to the other models. It had the lowest variance amongst the other models.

## Application:
The XGB model was saved as a pickle file to be used later. Flask was used to develop the API.
The application asks the user to enter the pickup date time, pick up and drop loation and the number of passengers for the ride. The locations entered by the user are converted into latitude and longitude using Geocoders from Geopy. Geopy includes geocoder classes for the OpenStreetMap Nominatim, Google Geocoding API (V3), and many other geocoding services. It leverages the third party API services to perform geocoding. The Taxi Fare Predictor application uses Nominatim class using a user agent. The user agent is necessary so that Nominatim can keep track of the requests an user makes. 
Using the information provided by the user, it predicts the estimated Taxi Fare.

This application was deployed to Microsoft Azure. 
Check out the application here : 

