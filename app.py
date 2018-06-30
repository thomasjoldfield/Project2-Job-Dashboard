from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import os

#flask setup
app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

@app.route("/compare")
def compare():
    return render_template("compare.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/flights")
def flights():
    return render_template("flights.html")


#Sweet. Now, query the database and send the jsonified results

@app.route("/airports")
def AllAirportsFunc():
    """Return a list of Airports."""
    results = db.session.query(Airport.iata_code, Airport.name, Airport.latitude, Airport.longitude, Airport.average_wait).all()

    all_airports_data = []
    for result in results:
        all_airports_data.append({
                "code" : result[0],
                "name" : result[1],
                "lat" : result[2],
                "long" : result[3],
                "wait" : result[4]
        })

    return jsonify(all_airports_data)

@app.route("/airports/<aircode>")
def AirportsFunc(aircode):
    """Return a details about a specific Airport."""
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
def AllDelayFunc(takeoff):
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

@app.route("/delays/<takeoff>/<landing>")
def DelayFunc(takeoff, landing):
    results = db.session.query(Delay.id, Delay.FlightDate, Delay.Origin, Delay.Dest, Delay.UniqueCarrier, Delay.Cancelled, Delay.DepDelay, Delay.ArrDelay).filter(Delay.Origin == takeoff).filter(Delay.Dest == landing)

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




#this route is specifically for our "mariokart" chart
@app.route("/delaycomparison/<takeoff>/<landing>")
def DelayComparison(takeoff, landing):
    results = db.session.query(Delay.id, Delay.FlightDate, Delay.Origin, Delay.Dest, Delay.UniqueCarrier, Delay.Cancelled, Delay.DepDelay, Delay.ArrDelay).filter(Delay.Origin == takeoff).filter(Delay.Dest == landing)
    airport_result = db.session.query(Airport.iata_code, Airport.average_wait).filter(or_(Airport.iata_code == takeoff, Airport.iata_code == landing))

    delay_list = []
    cancel_list = []

    for result in results:
        delay_list.append(result.ArrDelay)
        cancel_list.append(result.Cancelled)
    
    #equation should be (average / worst) * 100
    delay_number = ((sum(delay_list) / len(delay_list)) / 10) * 100
    cancel_number = ((sum(cancel_list) / len(delay_list)) / .2) * 100
    tsa_number = ((airport_result[0].average_wait + airport_result[1].average_wait) / 27 * 100)
    R1 = (255 * delay_number) / 100
    G1 = (255 * (100-delay_number)) / 100
    R2 = (255 * cancel_number) / 100
    G2 = (255 * (100-cancel_number)) / 100
    R3 = (255 * tsa_number) / 100
    G3 = (255 * (100-tsa_number)) / 100

    compare_data = {
        "x" : ["Delays", "Cancelations", "TSA Wait"],
        "y" : [delay_number, cancel_number, tsa_number],
        "type" : "bar",
        #"orientation" : "h",
        "marker" : {
            "color" : [f"rgba({R1},{G1},0,1)", f"rgba({R2},{G2},0,1)", f"rgba({R3},{G3},0,1)",]}
    }

    return jsonify(compare_data)



if __name__ == '__main__':
    app.run()