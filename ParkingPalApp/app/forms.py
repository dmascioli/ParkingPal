from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, SelectField
from wtforms.fields.html5 import DateField
from wtforms_components import TimeField
from wtforms.validators import DataRequired

# range_options = [(.1, '.1 miles'),
#                  (.25, '.25 miles'),
#                  (.5, '.5 miles'),
#                  (.75, '.75 miles'),
#                  (1, '1 mile')]

range_options = [(.05, '1 block'),
                 (.075, '2 blocks'),
                 (.1, '3 blocks'),
                 (.15, '4 blocks'),
                 (.3, '5 blocks')]


class FindParkingForm(FlaskForm):
    location = StringField('Street Address')
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time')
    distance = SelectField(
        'Range', choices=range_options)
    submit = SubmitField('Find Parking')
