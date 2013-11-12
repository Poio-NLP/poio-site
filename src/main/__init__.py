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

from flask import Flask, render_template, Markup
from flask.ext.mobility import Mobility
from flask.ext.mobility.decorators import mobile_template

import pressagio.callback
import pressagio

from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

app = Flask(__name__)
Mobility(app)

# Import flask modules after defining app
import main.api

# Creating global language data
languages_data = {}
languages_data_file = os.path.join(app.static_folder, 'langinfo',
    'languages_data.pickle')
with open(languages_data_file, "rb") as f:
    languages_data = pickle.load(f)


###################################### Pages

@app.route("/")
@mobile_template('{mobile/}index.html')
def index(template):
    languages_iso = {}
    for iso in languages_data:
        languages_iso[languages_data[iso]['label']] = iso
    languages = sorted(languages_iso.keys())
    languages_json = json.dumps(languages_data)

    return render_template(template, languages = languages,
        languages_iso = languages_iso,
        languages_json = Markup(languages_json))

# We still need those for the mobile app

@app.route("/about")
@mobile_template('{mobile/}about.html')
def about(template):
    return render_template(template)

@app.route("/tools/prediction/<iso>")
@mobile_template('{mobile/}tools_prediction.html')
def tools_prediction(template, iso):
    return render_template(template, iso=iso)

