from flask import Flask, jsonify
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import sqlite3
import pandas as pd
import datetime as dt

# Hawaii = sqlite3.connect('Resources/hawaii.sqlite')

# Measurement_df = pd.read_sql_query("SELECT * FROM Measurement", Hawaii)
# Station_df = pd.read_sql_query("select * from Station", Hawaii)

engine = create_engine('sqlite:///Resources/hawaii.sqlite')
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Vacation Weather API!<br/><br/>"

        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.station, 
       Measurement.prcp).filter(Measurement.date>(dt.date(2017,8,23)-dt.timedelta(365))).all()
   
    session.close()

    precipitation = []
    for Date, Station, Precipitation in results:
        precipitation_dict = {}
        precipitation_dict["Date"]= Date
        precipitation_dict["Station"]= Station
        precipitation_dict["Precipitation"]= Precipitation
        precipitation.append(precipitation_dict)

    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Station.station, Station.name).group_by(Station.station).all()

    session.close()

    stations_list = []
    for Station_number, Name in results:
        station_dict = {}
        station_dict["Station"]=Station_number
        station_dict["Name"]=Name
        stations_list.append(station_dict)

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    results = session.query(Measurement.date, Measurement.station, 
       Measurement.tobs).filter(Measurement.date>(dt.date(2017,8,23)-dt.timedelta(365))).all()
   
    session.close()

    temps = []
    for Date, Station, Tobs in results:
        temps_dict = {}
        temps_dict["Date"]= Date
        temps_dict["Station"]= Station
        temps_dict["Tobs"]= Tobs
        temps.append(temps_dict)

    return jsonify(temps)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def dates(start,end=None):
    if end == None:
        end = start
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    temps = []
    for TMIN, TAVG, TMAX in results:
        temps_dict = {}
        temps_dict["TMIN"]=TMIN
        temps_dict["TAVG"]=TAVG
        temps_dict["TMAX"]=TMAX
        temps.append(temps_dict)

    return jsonify(temps)


if __name__ == "__main__":
    app.run(debug=True)