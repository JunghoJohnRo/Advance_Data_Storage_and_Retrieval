import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

# Adding this - DL
from sqlalchemy.orm import scoped_session, sessionmaker

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# Adding this - DL
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
##############################

@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = db_session.query(Measurement.date, Measurement.prcp).all()
    return jsonify(results)

@app.route("/api/v1.0/stations")
def stations():
    results = db_session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = db_session.query(Measurement.tobs).filter(Measurement.date > query_date).order_by(Measurement.date).all()
    return jsonify(results)

# Adding this - DL
@app.teardown_appcontext
def cleanup(resp_or_exc):
    print('Teardown received')
    db_session.remove()

if __name__ == '__main__':
    app.run(debug=True)
