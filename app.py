import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
print(Base.classes.keys())
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

lastyear = dt.date(2017, 8, 23) - dt.timedelta(days=365)
mostactive = 'USC00519281'

@app.route("/")
def welcome():
    return (
        f"HW10<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/temp/start/end<br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= lastyear).all()
    preciptable = {date: prcp for date, prcp in precip}
    return jsonify(preciptable)

@app.route("/api/v1.0/stations")
def stations():
    stationsquery = session.query(Station.station).all()
    stations = list(np.ravel(stationsquery))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    tempquery = session.query(Measurement.tobs).filter(Measurement.station == mostactive).filter(Measurement.date >= lastyear).all()
    temps = list(np.ravel(tempquery))
    return jsonify(temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start,end):
    data = [func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)]
    if not end:
        results = session.query(*data).filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*data).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)



if __name__ == '__main__':
    app.run()