from app import app
from flask import render_template, flash, redirect, url_for, request
from app.forms import FindParkingForm
from app.nearest_meters import find_nearest_meters, get_geolocation


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/map", methods=['GET', 'POST'])
def map():
    form = FindParkingForm()
    user_location = (40.441, -79.995)
    zoom = 13
    meter_availability = []
    if form.validate_on_submit and request.method == 'POST':
        user_location = get_geolocation(form.location.data)
        radius = float(form.distance.data)
        if radius == .1:
            zoom = 18
        elif radius == .25:
            zoom = 17
        elif radius == .5:
            zoom = 16
        elif radius == .75:
            zoom = 15
        else:
            zoom = 14

        close_meters = find_nearest_meters(user_location, radius)
        for meter in close_meters:
            meter_availability.append(
                {'id': meter['id'], 'lat': meter['lat'], 'lon': meter['lon'], 'prediction': .5})
        pass
    return render_template("map.html", form=form, user_location=user_location, zoom=zoom, meters=meter_availability)
