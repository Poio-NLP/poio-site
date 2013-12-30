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
import datetime
from random import choice
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from flask import Flask, render_template, Markup, g, request, url_for, redirect
from flask.ext.mobility import Mobility
from flask.ext.mobility.decorators import mobile_template

import jwt
import psycopg2

from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('main.default_settings')
app.config.from_pyfile('application.cfg', silent=True)

Mobility(app)

from main.api import api
app.register_blueprint(api, url_prefix='/api')

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

languages = sorted(languages_iso.keys())

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
@mobile_template('{mobile}/index.html')
def index(template):
    languages_json = json.dumps(languages_data)
    token = jwt.encode({'exp': datetime.datetime.utcnow() + \
        datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])
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

@app.route("/tools/semantics/<iso>", methods=["POST"])
def tools_semantics_term(iso):
    term = None
    if "term" in request.form:
        term = request.form["term"]
        term = "".join(
            [c for c in term if c.isalpha() or c.isdigit() or c==' '])\
            .rstrip().lower()
    target = url_for("tools_semantics", iso=iso, term=term)
    return redirect(target)

@app.route("/tools/semantics/<iso>")
@app.route("/tools/semantics/<iso>/<term>")
def tools_semantics(iso, term=None):
    if term != None:
        graphdata = main.api.get_semantic_map(iso, term)
        # if not map_file:
        # flash('No result for search term "{0}".'.format(term))
        # else:
        # return render_template('tools_semantics.html', iso=iso,
        # map=map_file.encode('utf-8'), term=term)
        graphdata_json = json.dumps(graphdata)
        return render_template('tools_semantics.html', iso=iso,
            map=None, term=term, graphdata_json = Markup(graphdata_json))
    return render_template('tools_semantics.html', iso=iso,
        map=None, term=term)
