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
import operator
import codecs
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from flask import Flask, render_template, Markup, request, url_for, redirect, \
    flash, Response
from flask.ext.mobility import Mobility
from flask.ext.mobility.decorators import mobile_template

#import rdflib
import numpy as np
import scipy.spatial
import scipy.linalg

import pressagio.callback
import pressagio

from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

app = Flask(__name__)
Mobility(app)

# Import flask modules after defining app:

import api 


# Get languages:

languages_data = {}
languages_data_file = os.path.join(app.static_folder, 'langinfo',
    'languages_data.pickle')
with open(languages_data_file, "rb") as f:
    languages_data = pickle.load(f)


###################################### Pages

@app.route("/")
@mobile_template('{mobile/}index.html')
def index(template):
    if request.MOBILE:
        languages_iso = {}
        for iso in languages_data:
            languages_iso[languages_data[iso]['label']] = iso
        languages = sorted(languages_iso.keys())
        return render_template(template, languages = languages,
            languages_iso = languages_iso)
        
    else:
        #languages_data = get_languages_data()
        languages_json = json.dumps(languages_data)

        return render_template(template,
            languages_json = Markup(languages_json))

@app.route("/about")
@mobile_template('{mobile/}about.html')
def about(template):
    return render_template(template)

@app.route("/corpus")
def corpus():
    #languages_data = get_languages_data()
    iso_codes = sorted(languages_data.keys())

    return render_template('corpus.html', languages_data = languages_data,
        languages = iso_codes)

@app.route("/tools")
def tools():
    #languages_data = get_languages_data()
    iso_codes_all = sorted(languages_data.keys())

    # filter iso codes for semantic maps
    iso_codes_semantics = []
    for iso in iso_codes_all:
        indices_file = os.path.join(app.static_folder, 'semantics',
            "{0}-indices.pickle".format(iso))
        if os.path.exists(indices_file):
            iso_codes_semantics.append(iso)

    # filter iso codes for text prediction
    iso_codes_prediction = []
    for iso in iso_codes_all:
        config_file = os.path.join(app.static_folder, 'prediction',
            "{0}.ini".format(iso))
        if os.path.exists(config_file):
            iso_codes_prediction.append(iso)

    return render_template('tools.html', languages_data = languages_data,
        languages_semantics = iso_codes_semantics,
        languages_prediction = iso_codes_prediction)


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
    return render_template('tools_semantics.html', iso=iso, term=term)


@app.route("/tools/prediction/<iso>")
@mobile_template('{mobile/}tools_prediction.html')
def tools_prediction(template, iso):
    return render_template(template, iso=iso)


@app.route("/documentation")
def documentation():
    return render_template('documentation.html')


@app.route("/imprint")
def imprint():
    return render_template('imprint.html')


@app.route("/privacy")
def privacy():
    return render_template('privacy.html')


@app.route("/licenses")
def licenses():
    return render_template('licenses.html')
