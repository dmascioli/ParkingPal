from app import app
from calendar import day_name
from flask import render_template, flash, redirect, url_for, request
from app.forms import FindParkingForm
from app.meters import find_nearest_meters, get_geolocation, get_prediction, get_zone, async_get_meter_predictions, thread_get_meter_predictions
import asyncio
import datetime
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar

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
        if radius == .05:
            zoom = 20
        elif radius == .075:
            zoom = 18
        elif radius == .1:
            zoom = 17
        elif radius == .15:
            zoom = 17
        else:
            zoom = 16

        # possibly use sql instead of dataframe here
        close_meters = find_nearest_meters(user_location, radius)

        # make this async

        # for meter in close_meters:
        #     meter_req = {
        #         'day_of_week': day_name[form.date.data.weekday()],
        #         'is_holiday': str(False),
        #         'meter': meter['id'],
        #         'month': f'{form.date.data.month:02}',
        #         'time': form.time.data.isoformat(),
        #         'zone': get_zone(meter['id'])
        #     }
        #     prediction = get_prediction(meter_req)
        #     meter_availability.append(
        #         {'id': meter['id'], 'lat': meter['lat'], 'lon': meter['lon'], 'prediction': prediction})

        # check if day is a holiday and round to 10 minute interval
        day = day_name[form.date.data.weekday()]
        month = f'{form.date.data.month:02}'
        
        date = str(form.date.data)
        cal = calendar()
        holidays = cal.holidays('2020-01-01', '2020-12-31')
        is_holiday = str(pd.to_datetime(date).to_datetime64() in holidays)

        time = form.time.data.isoformat()
        time = str(pd.to_datetime(str(time)).round('10min').time())
       
        # async for slightly better speed boost
        meter_availability = asyncio.run(async_get_meter_predictions(
            close_meters, day, month, time, is_holiday))

        # sort ASC by prediction value
        meter_availability = sorted(meter_availability, key=lambda meter: meter['prediction'], reverse=True)

        # meter_availability = thread_get_meter_predictions(
        #     close_meters, day, month, time)
    return render_template("map.html", form=form, user_location=user_location, zoom=zoom, meters=meter_availability)
