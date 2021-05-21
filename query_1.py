from flask import Flask, jsonify

import numpy as np
from sqlalchemy.engine import base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import pandas as pd
import datetime as dt

def get_table_keys(db):
    engine = create_engine(db)
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    keys = Base.classes.keys()
    # print(classes_name)
    table_keys = keys
    return table_keys

hawaii_keys = get_table_keys("sqlite:///Resources/hawaii.sqlite")
print(hawaii_keys)

def classes_name(keys_list):
    class_name = []

    for key in keys_list:
        key_name = key.capitalize()
        class_name.append(key_name)
    return class_name
    # x += 1
print(classes_name(hawaii_keys))

# # Measurement = base.classes.measurement
# # Station = base.classes.station
# def engine_create(db):
#     engine = create_engine(db)
#     Base = automap_base()
#     Base.prepare(engine, reflect=True)

# engine_create('sqlite:///Resources/hawaii.sqlite')
# session = Session(engine)
# inspector = inspect(engine)
# inspector.get_table_names()


# session = Session(engine)

# session.close()


# engine_create('sqlite:///Resources/hawaii.sqlite')

# Measurement = Base.classes.measurement
# Station = Base.classes.station
# session = Session(engine)
# inspector = inspect(engine)
# inspector.get_table_names()

# columns1 = inspector.get_columns('measurement')
# print(f'Measurement table has the following columns: ')
# for c in columns1:
#     print(c['name'], c['type'])
# print(f'Station table has the following columns: ')
# columns2 = inspector.get_columns('station')
# for c in columns2:
#     print(c['name'], c['type'])

# recent = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
# print(f'Measurement table most recent date is {[recent for recent in recent]}.')

# recent = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
# print(f'Measurement table most recent date is {[recent for recent in recent]}.')

# query_date = dt.date(2017,8,23) - dt.timedelta(days=365)
# ic(query_date)

# # Perform a query to retrieve the data and precipitation scores
# results = session.query(Measurement.date, Measurement.prcp).\
#     filter(Measurement.date >= query_date).all()
# # ic(results)
# dates = [result[0] for result in results]
# ic(len(dates))
# precip = [result[1] for result in results]
# ic(len(precip))
# # Save the query results as a Pandas DataFrame and set the index to the date column
# precip_df = pd.DataFrame(list(zip(dates, precip)))
# precip_df.columns = ["Date", "Precipitation"]

# precip_df = precip_df.set_index('Date')
# # precip_df.head()

# # Sort the dataframe by date
# precip_sorted = precip_df.sort_values(by=["Date"])
# precip_sorted.head(20)
# # Use Pandas Plotting with Matplotlib to plot the data
# plt.figure(figsize=(10,5))
# precip_sorted['Precipitation'].plot(ylabel="Precipitation", title="Precipitation in Hawai'i \nfrom 2016-08-24 Through 2017-08-23", color='green', legend=True)