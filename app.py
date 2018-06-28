import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, render_template

app = Flask(__name__)

engine = create_engine("sqlite:///TravelStressor.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)


session = Session(engine)

@app.route("/")
def index():
   return render_template("index.html")



@app.route("/airports/<iata_code>")
def Airports():
    """Return a list of Airports."""
    return render_template("flights.html")
    Airport = Base.classes.Airport
    results = session.query(Airport.name).all()
    Airports = list(np.ravel(results))
    return jsonify(Airports)

@app.route("/flights")
def Airports():
    """Return a list of Airports."""
    return render_template("flights.html")
    Airport = Base.classes.Airport
    results = session.query(Airport.name).all()
    Airports = list(np.ravel(results))
    return jsonify(Airports)

####################
    canonicalized = real_name.replace(" ", "").lower()
    for character in justice_league_members:
        search_term = character["real_name"].replace(" ", "").lower()

        if search_term == canonicalized:
            return jsonify(character)

    return jsonify({"error": f"Character with real_name {real_name} not found."}), 404
####################

@app.route("/delays")
def Delays():
    """Return delays."""
    Delays = Base.classes.delays
    results = session.query(Delays.Orgin).all()
    AllDelays = list(np.ravel(results))
    return jsonify(AllDelays)


if __name__ == '__main__':
    app.run(debug = True)

