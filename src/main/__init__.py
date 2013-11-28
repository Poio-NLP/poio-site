# -*- coding: utf-8 -*-
#
# Poio Corpus
#
# Copyright (C) 2009-2013 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE.TXT

import os
import glob
import json
import pickle
import time
import datetime
import jwt
from random import choice
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from flask import Flask, render_template, Markup, g
from flask.ext.mobility import Mobility
from flask.ext.mobility.decorators import mobile_template

import psycopg2

from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

app = Flask(__name__)
Mobility(app)

# Creating global language data
languages_data = dict()
languages_data_file = os.path.join(app.static_folder, 'langinfo',
    'languages_data.pickle')
with open(languages_data_file, "rb") as f:
    languages_data = pickle.load(f)

# Creating global database connections
#dbconnections = dict()
languages_iso = dict()
for iso in languages_data:
    languages_iso[languages_data[iso]['label']] = iso
    # config_file = os.path.join(app.static_folder, 'prediction', "{0}.ini".format(iso))
    # config = configparser.ConfigParser()
    # config.read(config_file)
    # if config.get("Database", "class") == 'PostgresDatabaseConnector':
    #     dbconnections[iso] = psycopg2.connect(
    #         host=config.get("Database", "host"),
    #         database=iso,
    #         user=config.get("Database", "user"),
    #         password=config.get("Database", "password"))

languages = sorted(languages_iso.keys())

# Import flask modules after defining app
import main.api

###################################### Helpers

@app.before_request
def choose_color():
    color_codes = {
        'green': '#2bb673',
        'orange': '#fcb040',
        'pink': '#ed0281',
        'purple': '#8a288f',
    }
    g.color = choice(['green', 'orange', 'pink', 'purple'])
    g.color_code = color_codes[g.color]

###################################### Pages

@app.route("/")
@mobile_template('{mobile/}index.html')
def index(template):
    languages_json = json.dumps(languages_data)

    token = jwt.encode({'exp': time.mktime((datetime.datetime.now() + datetime.timedelta(hours=1)).timetuple())}, 'supersecret')
    print token
    return render_template(template, languages = languages,
        languages_iso = languages_iso,
        languages_json = Markup(languages_json),
        token = token)
    
# We still need those for the mobile app

@app.route("/about")
@mobile_template('{mobile/}about.html')
def about(template):
    return render_template(template)

@app.route("/tools/prediction/<iso>")
@mobile_template('{mobile/}tools_prediction.html')
def tools_prediction(template, iso):
    return render_template(template, iso=iso)

