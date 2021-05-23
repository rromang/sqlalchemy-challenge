# import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)
print(Base.classes.keys())

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# #################################################
# # Flask Setup
# #################################################
app = Flask(__name__)


# #################################################
# # Flask Routes
# #################################################

@app.route("/")
def welcome():
    # """List all available api routes."""
    return (
        f"Welcome to Hawai'i's Weather Exploration API!</br>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2016-08-23<br/>")
        


@app.route("/api/v1.0/precipitation")
def precipiation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all measurement information"""
    # Query all measurements
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    all_prcp = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict['date'] = date
        precip_dict['precipitation'] = prcp
        all_prcp.append(precip_dict)
    
    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station information"""
    # Query all passengers
    results = session.query(Station.id, Station.station, Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_station = []
    for id, station, name in results:
        station_dict = {}
        station_dict['Station Id'] = id
        station_dict['Station'] = station
        station_dict['Name'] = name

        all_station.append(station_dict)
    
    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    query_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    measure_results = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()

    stations = [result[0] for result in measure_results]
    station_counts = [result[1] for result in measure_results]
    stations_df = pd.DataFrame(list(zip(stations,station_counts)))
    stations_df.columns = ["Station Id", "Counts"]
    stations_df

    active_station = stations_df['Station Id'].max()

    results_temps = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= query_date, Measurement.station==active_station).all()

    session.close()

    lastyear_temps = []
    for station, date, tobs in results_temps:
        temps_dict = {}
        temps_dict['Station'] = station
        temps_dict['Date'] = date
        temps_dict['Temperature'] = tobs

        lastyear_temps.append(temps_dict)
    
    return jsonify(lastyear_temps)

@app.route("/api/v1.0/2016-08-23")
def year_stats():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    query_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    results_max_temp = session.query(Measurement.date, func.max(Measurement.tobs)).\
    filter(Measurement.date >= query_date)

    results_min_temp = session.query(Measurement.date, func.min(Measurement.tobs)).\
    filter(Measurement.date >= query_date)

    results_avg_temp = session.query(func.avg(Measurement.tobs)).\
    filter(Measurement.date >= query_date)

    session.close()

    lastyear_stats = []
    max_stats = []
    min_stats = []


    max_key = ["Max Temp"]
    date_max = [result[0] for result in results_max_temp]
    max_temp = [result[1] for result in results_max_temp]
    max_stats.append(list(zip(date_max, max_temp)))
    lastyear_stats.append(dict(zip(max_key,max_stats)))   

    min_key = ["Min Temp"]
    date_min = [result[0] for result in results_min_temp]
    min_temp = [result[1] for result in results_min_temp]
    min_stats.append(list(zip(date_min, min_temp)))
    lastyear_stats.append(dict(zip(min_key,min_stats)))   

    avg_key = ["Year Avg Temp"]
    avg_temp = [round(result[0],2) for result in results_avg_temp]
    lastyear_stats.append(dict(zip(avg_key, avg_temp)))

    
    return jsonify(lastyear_stats)


if __name__ == '__main__':
    app.run(debug=True)
