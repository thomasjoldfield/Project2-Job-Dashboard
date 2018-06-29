from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

from flask_sqlalchemy import SQLAlchemy
import os

#flask setup
app = Flask(__name__)

#setup that database!
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///TravelStressor3.sqlite"

db = SQLAlchemy(app)

class Delay(db.Model):
    __tablename__ = 'Delays'

    id = db.Column(db.Integer, primary_key=True)
    FlightDate= db.Column(db.Text)
    UniqueCarrier = db.Column(db.Text)
    Origin = db.Column(db.Text)
    Dest = db.Column(db.Text)
    DepDelay = db.Column(db.Float)
    ArrDelay = db.Column(db.Float)
    Cancelled = db.Column(db.Float)
    CancellationCode = db.Column(db.Text)
    Diverted = db.Column(db.Float)
    Distance = db.Column(db.Float)
    CarrierDelay = db.Column(db.Float)
    WeatherDelay = db.Column(db.Float)
    NASDelay = db.Column(db.Float)
    SecurityDelay = db.Column(db.Float)
    LateAircraftDelay = db.Column(db.Float)
    extend_existing=True



class Airport(db.Model):
    __tablename__ = 'Airports'
    id = db.Column(db.Integer, primary_key=True)
    iata_code = db.Column(db.Text)
    name = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    iso_region = db.Column(db.Text)
    average_wait = db.Column(db.Float)
    max_wait = db.Column(db.Float)
    min_wait = db.Column (db.Float)
    obs_count = db.Column (db.Float)
    extend_existing=True


#now, create the route that renders index.html
@app.route("/")
def index():
   return render_template("index.html")


#Sweet. Now, query the database and send the jsonified results
@app.route("/airports/<aircode>")
def AirportsFunc(aircode):
    """Return a list of Airports."""
    results = db.session.query(Airport.iata_code, Airport.name, Airport.latitude, Airport.longitude, Airport.average_wait).filter(Airport.iata_code == aircode )

    airport_data = [{
        "code" : [result[0] for result in results],
        "name" : [result[1] for result in results],
        "lat" : [result[2] for result in results],
        "long" : [result[3] for result in results],
        "wait" : [result[4] for result in results]
    }]

    return jsonify(airport_data)

@app.route("/delays/<takeoff>")
def DelayFunc(takeoff):
    results = db.session.query(Delay.id, Delay.FlightDate, Delay.Origin, Delay.Dest, Delay.UniqueCarrier, Delay.Cancelled, Delay.DepDelay, Delay.ArrDelay).filter(Delay.Origin == takeoff)

    delay_data = []

    for result in results:
        delay_data.append({
            result[0] : {
                "date" : result[1],
                "origin" : result[2],
                "dest" : result[3],
                "carrier" : result[4],
                "cancel" : result[5],
                "delayDep" : result[6],
                "delayArr" : result[7]
            }
        })

    return jsonify(delay_data)

if __name__ == '__main__':
    app.run()
