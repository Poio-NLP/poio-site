import os
import pickle
import json
import operator
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from flask import Blueprint, Flask, request, Response, url_for, current_app

#import rdflib
import numpy as np
import scipy.spatial
import scipy.linalg
import jwt

import pressagio.callback
import pressagio

# Import Flask app
#from main import app

api = Blueprint('api', __name__)

class DemoCallback(pressagio.callback.Callback):
    def __init__(self, buffer):
        pressagio.callback.Callback.__init__(self)
        self.buffer = buffer

    def past_stream(self):
        return self.buffer
    
    def future_stream(self):
        return ''


################################################### API routes

@api.before_request
def before_request():
    if request.endpoint == 'api.api_languages' or \
            request.endpoint == 'api.api_corpus':
        return

    # check if we have a token
    token = request.args.get('token', '', type=str)
    access_granted = False
    if token == '':
        if 'X-Mashape-Proxy-Secret' in request.headers and \
                request.headers['X-Mashape-Proxy-Secret'] == \
                current_app.config['MASHAPE_SECRET']:
            access_granted = True
        elif 'X-Poio-Android-IPL' in request.headers and \
                request.headers['X-Poio-Android-IPL'] == \
                current_app.config['IPL_SECRET']:
            access_granted = True
    else:
        try:
            jwt.decode(token, current_app.config['SECRET_KEY'])
            access_granted = True
        except jwt.DecodeError, jwt.ExpiredSignature:
            pass

    if not access_granted:
        return Response(json.dumps({'error':
                'You do not have the rights to access the API.'}),
            mimetype='application/json')

@api.route("/semantics")
def api_semantics():
    return Response(json.dumps(get_semantic_map()), mimetype='application/json')

@api.route("/prediction")
def api_prediction():
    return Response(json.dumps(get_prediction()), mimetype='application/json')

@api.route("/languages")
def api_languages():
    return Response(json.dumps(get_supported_languages()), mimetype='application/json')

@api.route("/corpus")
def api_corpus():
    return Response(json.dumps(get_corpus_files()), mimetype='application/json')


################################################### Helpers

def get_prediction():
    iso = request.args.get('iso', '', type=str)
    predictions = []
    if iso != 'none':
        string_buffer = request.args.get('text', '')

        config_file_base = current_app.config['PREDICTION_INI']
        if "{0}" in config_file_base:
            config_file_base = config_file_base.format(iso)
        config_file = os.path.join(api.root_path, 'static', 'prediction',
            config_file_base)
        config = configparser.ConfigParser()
        config.read(config_file)
        dbconnection = None
        if config.get("Database", "class") == 'PostgresDatabaseConnector':
            config.set("Database", "database", iso)
        else:
            db_file = os.path.abspath(os.path.join(api.root_path, 'static',
                'prediction', "{0}.sqlite".format(iso)))
            config.set("Database", "database", db_file)

        callback = DemoCallback(string_buffer)
        prsgio = pressagio.Pressagio(callback, config, dbconnection)
        predictions = prsgio.predict()
        prsgio.close_database()

    return predictions


def get_semantic_map(iso = None, term = None):
    if not iso:
        iso = request.args.get('iso', '', type=str)
    if not term:
        term = request.args.get('term', '')

    plot_dir = os.path.join(api.root_path, 'static', 'plots')
    plot_filename = u"{0}-{1}.pickle".format(iso, term)
    plot_filepath = os.path.join(plot_dir, plot_filename)

    if os.path.exists(plot_filepath):
        inputfile = open(plot_filepath, 'rb')
        graphdata = pickle.load(inputfile)
        inputfile.close()
        return graphdata

    sem_dir = os.path.join(api.root_path, 'static', 'semantics')

    indices_file = os.path.join(sem_dir, "{0}-indices.pickle".format(iso))
    with open(indices_file, "rb") as f:
        indices = pickle.load(f)
        keys = [k 
            for k, _ in sorted(indices.items(), key=operator.itemgetter(1))]
    if not term in indices:
        return None


    ut_file = os.path.join(sem_dir, "{0}-ut.bin".format(iso))
    with open(ut_file, "rb") as f:
        ut = np.load(f)
    s_file = os.path.join(sem_dir, "{0}-s.bin".format(iso))
    with open(s_file, "rb") as f:
        s = np.load(f)
    vt_file = os.path.join(sem_dir, "{0}-vt.bin".format(iso))
    with open(vt_file, "rb") as f:
        vt = np.load(f)

    reconstructed_matrix = np.dot(ut.T, np.dot(np.diag(s), vt))
    tree = scipy.spatial.cKDTree(reconstructed_matrix)
    neighbours = tree.query(reconstructed_matrix[indices[term]], k=50)

    subset = reconstructed_matrix[neighbours[1]]
    words = [keys[i] for i in neighbours[1]]
    tempU, tempS, tempVt = scipy.linalg.svd(subset)

    graphdata = []
    count = 0
    for element in tempU[:,1]:
        graphdata.append([words[count], element, tempU[:,2][count]])
        count += 1

    outputfile = open(plot_filepath, 'wb')
    pickle.dump(graphdata, outputfile)
    outputfile.close()

    return graphdata


def get_supported_languages():
    languages_list = []
    for element in languages_data():
        languages_list.append(element)
    return sorted(languages_list)


def get_corpus_files():
    iso = request.args.get('iso', '', type=str)
    
    if iso in get_supported_languages():
        files = []
        for filename in languages_data()[iso]["files"]:
            files.append(url_for('static', filename="corpus/" + filename, _external=True ))

        return files


def languages_data():
    languages_data = dict()
    languages_data_file = os.path.join(api.root_path, 'static', 'langinfo',
        'languages_data.pickle')
    with open(languages_data_file, "rb") as f:
        languages_data = pickle.load(f)
    return languages_data
