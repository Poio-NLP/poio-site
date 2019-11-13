import os
import pickle
import json
import operator

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from flask import Blueprint, Flask, request, Response, url_for, current_app

# import rdflib
import numpy as np
import scipy.spatial
import scipy.linalg
import jwt

import pressagio.callback
import pressagio

# Import Flask app
# from main import app

fapi = Blueprint("api", __name__)


class DemoCallback(pressagio.callback.Callback):
    def __init__(self, buffer):
        pressagio.callback.Callback.__init__(self)
        self.buffer = buffer

    def past_stream(self):
        return self.buffer

    def future_stream(self):
        return ""


################################################### API routes


@fapi.before_request
def before_request():
    if request.endpoint == "api.api_languages" or request.endpoint == "api.api_corpus":
        return

    # check if we have a token
    token = request.args.get("token", "", type=str)
    access_granted = False
    if token == "":
        if (
            "X-Mashape-Proxy-Secret" in request.headers
            and request.headers["X-Mashape-Proxy-Secret"]
            == current_app.config["MASHAPE_SECRET"]
        ):
            access_granted = True
        elif (
            "X-Poio-Android-IPL" in request.headers
            and request.headers["X-Poio-Android-IPL"]
            == current_app.config["IPL_SECRET"]
        ):
            access_granted = True
    else:
        try:
            jwt.decode(token, current_app.config["SECRET_KEY"])
            access_granted = True
        except (jwt.DecodeError, jwt.ExpiredSignature):
            pass
    # return
    if not access_granted:
        return Response(
            json.dumps({"error": "You do not have the rights to access the API."}),
            mimetype="application/json",
        )


@fapi.route("/prediction")
def api_prediction():
    return Response(json.dumps(get_prediction()), mimetype="application/json")


@fapi.route("/languages")
def api_languages():
    return Response(json.dumps(get_supported_languages()), mimetype="application/json")


################################################### Helpers


def get_prediction():
    iso = request.args.get("iso", "", type=str)
    predictions = []
    if iso != "none":
        string_buffer = request.args.get("text", "")

        config_file_base = current_app.config["PREDICTION_INI"]
        if "{0}" in config_file_base:
            config_file_base = config_file_base.format(iso)
        config_file = os.path.join(
            fapi.root_path, "static", "prediction", config_file_base
        )
        config = configparser.ConfigParser()
        config.read(config_file)
        dbconnection = None
        if config.get("Database", "class") == "PostgresDatabaseConnector":
            config.set("Database", "database", iso)
        else:
            db_file = os.path.abspath(
                os.path.join(
                    fapi.root_path, "static", "prediction", "{0}.sqlite".format(iso)
                )
            )
            config.set("Database", "database", db_file)

        callback = DemoCallback(string_buffer)
        prsgio = pressagio.Pressagio(callback, config, dbconnection)
        predictions = prsgio.predict()
        prsgio.close_database()

    return predictions


def get_supported_languages():
    languages_list = []
    for element in languages_config().keys():
        languages_list.append(element)
    return sorted(languages_list)


def languages_config():
    config_file = os.path.join(fapi.root_path, "..", "..", "config.json")
    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)
    languages_config = config["languages"]
    return languages_config
