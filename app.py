import numpy as np
import pandas as pd
import datetime as dt
from datetime import timedelta

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine
                  )


@app.route("/")
def welcome():
    return (
        f"Aloha! Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # return precipitation data for the last year:

    Measurement = Base.classes.measurement

    Station = Base.classes.station
    session = Session(engine)

    one_year=dt.date(2017, 8, 23) - dt.timedelta(days=365)

    precip=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year).all()


    precipitation={date: prcp for date, prcp in precip}

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():
    # return a list of stations:
    Measurement=Base.classes.measurement
    Station=Base.classes.station
    session=Session(engine)

    stations=session.query(Station.station).all()

    all_stations=list(np.ravel(stations))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # return temperature observations for the last year

    Measurement=Base.classes.measurement
    Station=Base.classes.station
    session=Session(engine)

    one_year=dt.date(2017, 8, 23) - dt.timedelta(days=365)

    temp=session.query(Measurement.date, Measurement.tobs).filter(
        Measurement.date >= one_year).all()

    temps=list(np.ravel(temp))

    return jsonify(temps)


@app.route("/api/v1.0/temp/<start>")
def stats(start):
    # return TMIN, TAVG, TMAX

    Measurement=Base.classes.measurement
    Station=Base.classes.station
    session=Session(engine)

    result=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    results=list(np.ravel(result))

    return jsonify(results)



@app.route("/api/v1.0/temp/<start>/<end>")
def stats1(start=None, end=None):
    # return TMIN, TAVG, TMAX
#print(calc_temps('2012-02-28', '2012-03-05'))

    Measurement=Base.classes.measurement
    Station=Base.classes.station
    session=Session(engine)

    result1=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    results1=list(np.ravel(result1))

    return jsonify(results1)


if __name__ == '__main__':
    app.run(debug=True)