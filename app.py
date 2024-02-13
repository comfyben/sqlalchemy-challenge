# Import the dependencies.
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import os


#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine('sqlite:///Resources/hawaii.sqlite')
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route('/')
def homepage():
    """List all the available routes"""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )



#################################################
# Flask Routes
#################################################
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    prcp_query = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    
    prcp_values = []
    for date, prcp in prcp_query:
        prcp_dict = {}
        prcp_dict['Date'] = date
        prcp_dict['Precipitation'] = prcp
        prcp_values.append(prcp_dict)
    
    return jsonify(prcp_values)

@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    station_query = session.query(Station.id, Station.station)
    session.close()
    
    station_values = []
    for id, station in station_query:
        station_dict = {}
        station_dict['id'] = id
        station_dict['Station'] = station
        station_values.append(station_dict)
        
    return jsonify(station_values)

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
   
    active_station = session.query(Measurement.station, func.count(Measurement.station)).\
    order_by(func.count(Measurement.station).desc()).\
    group_by(Measurement.station).first()
    
    active_station_id = active_station[0]

    session = Session(engine)
    previous_year = session.query(Measurement.date).order_by(Measurement.date.desc()).\
        filter(Measurement.station == active_station_id).limit(365)
    
    year_start = previous_year[-5]
    
    tobs_query = session.query(Measurement.date, Measurement.tobs, Measurement.station).\
        filter(Measurement.station == active_station_id).\
        filter(Measurement.date > year_start)
    session.close()
    
    tobs_values = []
    for date, tobs, station in tobs_query:
        tobs_dict = {}
        tobs_dict['Date'] = date
        tobs_dict['Temperature'] = tobs
        tobs_dict['Station'] = station
        tobs_values.append(tobs_dict)
    
    return jsonify(tobs_values)

@app.route('/api/v1.0/<start>')
def start_date(start):

    session = Session(engine)
    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range"""
    # start is a date value that the user inputs. Make a function that outputs the min, max and avg

    start_date_tobs_describe = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start)
    session.close()

    
    start_values = []
    for min, max, avg in start_date_tobs_describe:
        start_dict = {}
        start_dict['min'] = min
        start_dict['max'] = max
        start_dict['avg'] = avg
        start_values.append(start_dict) 

    return jsonify(start_values)

@app.route('/api/v1.0/<start>/<end>')
def start_end_date(start, end):
    session = Session(engine)

    start_end_tobs_describe = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end)
    
    session.close()        

    start_end_values = []
    for min, max, avg in start_end_tobs_describe:
        start_end_dict = {}
        start_end_dict['min'] = min
        start_end_dict['max'] = max
        start_end_dict['avg'] = avg
        start_end_values.append(start_end_dict)

    return jsonify(start_end_values)

if __name__ == '__main__':
    app.run(debug=True)