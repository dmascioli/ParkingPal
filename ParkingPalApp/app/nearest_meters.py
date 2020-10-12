import pandas as pd
import math
from geopy.geocoders import Nominatim

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

    df = pd.read_csv('app/meter_data.csv')
    meter_locations = df.loc[:,['latitude','longitude','status']].iterrows()

    close_meters = []

    if(user_location != []):
        for index, meter in meter_locations:
            if(meter['status'] == 'Active' and math.dist(user_location, [meter['latitude'], meter['longitude']]) < radius):
                close_meters.append({'id':index, 'lat':meter['latitude'], 'lon':meter['longitude']})
    return close_meters
