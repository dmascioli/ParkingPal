import pandas as pd
import math
from app import app
from geopy.geocoders import Nominatim
from google.cloud import automl_v1beta1 as automl
from google.oauth2 import service_account
import datetime

# only read this once
meter_data = pd.read_csv('app/data/meter_data.csv')
meter_info = pd.read_csv('app/data/meter_info.csv')
# re-use one client instance
client = automl.TablesClient(
    project=app.config['PROJECT_ID'], 
    region=app.config['COMPUTE_REGION'],
    credentials=service_account.Credentials.from_service_account_file('app/data/PittParkingPal-9d5a9e2d9504.json')
)

def get_geolocation(street_address):
    # Potentially look into different geolocator, mixed results with Nominatim
    try:
        geolocator = Nominatim(user_agent="ParkingPal")
        geocode = geolocator.geocode(street_address)
        cords = (geocode.latitude, geocode.longitude)
    except:
        cords = []
    finally:
        return cords

def find_nearest_meters(user_location, radius):
    radius = radius/69.2 # ~69.2 miles to 1 decimal degree
  
    meter_locations = meter_data.loc[:,['id','latitude','longitude','status']].iterrows()
    close_meters = []

    if(user_location != []):
        for index, meter in meter_locations:
            if(meter['status'] == 'Active' and math.dist(user_location, [meter['latitude'], meter['longitude']]) < radius):
                close_meters.append({'id':meter['id'], 'lat':meter['latitude'], 'lon':meter['longitude']})
    return close_meters

# return the zone for a given meter ID
def get_zone(id):
    return meter_data.loc[meter_data['id'] == id, 'zone'].values[0]

# get online prediction from GCP AutoML Tables
def get_prediction(inputs):
    response = client.predict(
        model_display_name=app.config['MODEL_DISPLAY_NAME'],
        inputs=inputs
    )
    # this assumes we only recieve one result
    return response.payload[0].tables.value

# get $/hr for a meter using meter_info csv
def get_price(pred_info):
    if pred_info['day_of_week'] == 'Sunday':
        return 'Free'

    start_time = datetime.time(8,0)
    pred_time = datetime.time.fromisoformat(pred_info['time'])
    end_time = datetime.datetime.strptime(meter_info.loc[meter_info['zone'] == pred_info['zone'], pred_info['day_of_week']].iat[0], '%H:%M').time()
    
    if start_time < pred_time and end_time > pred_time:
        return meter_info.loc[meter_info['zone'] == pred_info['zone'], 'rate_description'].iat[0]
    return 'Free'