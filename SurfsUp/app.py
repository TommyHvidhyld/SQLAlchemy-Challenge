import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

################################
session = Session(engine)

# find the last date in the database
last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

# Calculate the date 1 year ago from the last data point in the database
query_date = dt.date(2017,8,23) - dt.timedelta(days=365)

# Calculate most active stations
stations = session.query(Measurement.station, func.count(Measurement.date)).\
    filter(Measurement.date >= query_date).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.date).desc()).all()

#Single most active station
most_active = stations[0]

session.close()
################################

# Flask Setup
app = Flask(__name__)

#################################################
# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"List of precipitation data: /api/v1.0/precipitation<br/>"
        f"List of stations and names: /api/v1.0/stations<br/>"
        f"List of temperatures for the most active station of the previous year: /api/v1.0/tobs<br/>"
        f"List of minimum, maximum, and average temperature for given start date 'yyyy-mm-dd': /api/v1.0/yyyy-mm-dd<br/>"
        f"List of minimum, maximum, and average temperature for given start and end date 'yyyy-mm-dd'/'yyyy-mm-dd': /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation over the last 12 monthes"""
    # Query all precipitation of last 12 monthes
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= query_date)
    session.close()

    # Create Dictionary of precipitation
    precipitation = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        precipitation.append(prcp_dict)

    return jsonify(precipitation)

##############################################

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results = session.query(Station.station, Station.name).all()
    session.close()

    # Convert list of tuples into dictionary of stations
    all_stations = []
    for station, name in results:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        all_stations.append(station_dict)

    return jsonify(all_stations)

##############################################

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature observations for the most-active station over the previous year"""
    # Query all temperature observations for the most-active station
    results = session.query(Measurement.station, func.count(Measurement.date)).\
    filter(Measurement.date >= query_date).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.date).desc()).all().first()
    session.close()