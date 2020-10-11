from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import FindParkingForm


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/map", methods=['GET', 'POST'])
def map():
    form = FindParkingForm()
    if form.validate_on_submit:
        pass
    return render_template("map.html", form=form)
