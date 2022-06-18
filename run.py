from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate("/Users/rokastarasevicius/Documents/Parcel_location/parcel-tracer-firebase-adminsdk-26wu1-e83ccc8e76.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://parcel-tracer-default-rtdb.europe-west1.firebasedatabase.app/'
})

ref = db.reference('/')

default_longitude = 24.0791646
default_latitude = 56.9519282

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

class IdForm(FlaskForm):
    id = StringField('ID')
    submit = SubmitField('Search')

@app.route('/', methods=['GET', 'POST'])
def home():
    form = IdForm()
    description = ''
    if request.method == 'POST':
        id = form.id.data
        longitude = ref.child("parcel").child(id).child("longitude").get()
        latitude = ref.child("parcel").child(id).child("latitude").get()
        description = "Last seen on " + ref.child("parcel").child(id).child("last_update").get()[:-14]
        default = 0
    else:
        longitude = default_longitude
        latitude = default_latitude
        default = 1
    print(longitude)
    print(latitude)
    return render_template('index.html', url_for=url_for, form=form, latitude=latitude, longitude=longitude, default=default, description=description)

@app.route('/map')
def map():
    return render_template('map.html', url_for=url_for)

if __name__ == '__main__':
    app.run(debug=True)
