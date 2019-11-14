# -*- coding: utf-8 -*-
#
# Poio Corpus
#
# Copyright (C) 2009-2019 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE

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
from flask_mobility import Mobility
from flask_mobility.decorators import mobile_template
import jwt
import psycopg2
from werkzeug.contrib.cache import SimpleCache
import poiolib.langinfo

import main.api

cache = SimpleCache()

app = Flask(__name__, instance_relative_config=True)
app.config.from_object("main.default_settings")
app.config.from_pyfile("application.cfg", silent=True)

Mobility(app)

app.register_blueprint(main.api.fapi, url_prefix="/api")

###################################### Helpers


def languages_info():
    languages = {}
    langinfo = poiolib.langinfo.LangInfo()
    for l in main.api.languages_config().keys():
        languages[l] = {
            "name": langinfo.langname_for_iso(l),
            "geo": langinfo.geoinfo_for_iso(l),
        }
    return languages


languages_info = languages_info()
languages = [
    l[0] for l in sorted(languages_info.items(), key=lambda k_v: k_v[1]["name"])
]


@app.before_request
def choose_color():
    color_codes = {
        "green": "#2bb673",
        "orange": "#fcb040",
        "pink": "#ed0281",
        "purple": "#8a288f",
    }
    g.color = choice(["green", "orange", "pink", "purple"])
    g.color_code = color_codes[g.color]


###################################### Pages


@app.route("/")
@mobile_template("{mobile}/index.html")
def index(template):
    token = jwt.encode(
        {"exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},
        app.config["SECRET_KEY"],
    ).decode("utf-8")
    return render_template(
        template, languages=languages, languages_info=languages_info, token=token,
    )


# We still need those for the mobile app


@app.route("/about")
@mobile_template("{mobile/}about.html")
def about(template):
    return render_template(template)


@app.route("/tools/prediction/<iso>")
@mobile_template("{mobile/}tools_prediction.html")
def tools_prediction(template, iso):
    return render_template(template, iso=iso)
