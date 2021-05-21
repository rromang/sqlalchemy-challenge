from flask import Flask, jsonify

import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import pandas as pd
import datetime as dt

# Flask Setup

app = Flask(__name__)

# Flask Routes

@app.route("/")
def welcome():
    return(
        f"Welcome to your Hawai'i Weather Exploration API!"
        f"Available Routes:"
        f'/api/v1.0/precipitation'
    )

