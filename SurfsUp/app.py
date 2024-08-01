# Import the dependencies.
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dict
import numpy as np
import datetime as dt
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using 'automap_base()'
Base = automap_base()

# Use the Base class to reflect the data tables
Base.prepare(autoload_with=engine)

# Assign the mearsuemet class to a ceriable called 'Measurement' and 
# the station class to a veriable called 'Station'
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session 
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask (__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
f"/api/v1.0/precipitation<br/>"
f"/api/v1.0/stations<br/>"
f"/api/v1.0/tobs<br/>"
f"/api/v1.0/temp/start<br/>"
f"/api/v1.0/temp/start/end")



@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_precipitation
    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Perform a query to retrieve the data and tobs scores
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= prev_year).filter(Measurement.station=='USC00519281').all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_tobs
    all_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/temp/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date>=start).all()

    session.close()

    # Convert list of tuples into normal list
    startdata = list(np.ravel(results))

    return jsonify(startdata)


@app.route("/api/v1.0/temp/<start>/<end>")
def start_end(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date>=start).filter(Measurement.date<=end).all()

    session.close()

    # Convert list of tuples into normal list
    startenddata = list(np.ravel(results))

    return jsonify(startenddata)



if __name__ == '__main__':
    app.run(debug=True)