"""
This file contains a function that installs a number of routes on a flask
webclient. This is more of a collection of routes than an actual function,
but this method allows us to easily call it from other places and keep that
part clean from these declarations.

@author Tycho Atsma <tycho.atsma@gmail.com>
@file   routes.py
@scope  public
"""

# third party dependencies
import os
from os import listdir
from os import path
from os.path import isfile, join
from flask import request, render_template
from flask.json import jsonify, load
import csv
import pandas as pd
import numpy as np
import time
from datetime import datetime

# we need to setup logging configuration here,
# so all other loggers will properly function
# and behave the same
import logging
logging.basicConfig(level=logging.INFO)

# dependencies
from lib.Simulation import Simulation
from lib.Servers import Servers
from lib.Logger import Logger
from lib.Processor import Processor
from lib.LogProcessing import get_endpoint_matrix
from lib.Seasonality import TransactionInterval as Seasonality

# Global vars
LOG_PATH = 'logs'

def install(client):
    """
    Function to install all routes onto a flask webclient.

    Parameters
    ----------
    client: Flask
        Flask application to install the routes on.
    """

    # global simulation count
    simc = 0
    
    # declare the index route
    @client.route('/')
    def index():
        """
        Function to generate and expose content for the index route.

        Returns
        -------
        string
        """
        log_filenames = [f for f in listdir(LOG_PATH) if isfile(join(LOG_PATH, f)) and not f.startswith('.')]

        return render_template('index.html', log_filenames=log_filenames, len_logfiles=len(log_filenames))

    # declare endpoint for retrieving forms
    @client.route('/forms/<name>')
    def forms(name):
        """
        Function to install handlers on the /forms path. This allows for
        retrieving predefined forms.

        Parameters
        ----------
        GET:
            name: string
                Name of the form file.

        Returns
        -------
        GET: string
        """
        # construct the path to the form
        fp = path.join(path.dirname(__file__), 'web', 'forms', name)

        # we need to have a valid path
        if not path.exists(fp):

            # tell the user there's no form
            return jsonify({ "error": "file does not exist" })

        # open the file
        with open(fp) as form:

            # expose the json of the form
            return load(form)

    # declare endpoint for starting a new simulation
    @client.route('/simulation', methods=["GET", "POST"])
    def simulation():
        """
        Function to install handlers on the /simulation path. This allows for
        requesting simulation data or starting a new simulation.

        Parameters
        ----------
        POST:

            servers: list
                List containing configurations for a server pool as dicts.
                { capacity: int, size: int, kind: string } 
                For example, { size: 10, capacity: 10, kind: 'regular' }.

            process: list
                List specifying how a process should go (from server to server). 
                This should contain a sequence of server kinds.
                For example, ["regular", "balance", "pay"].

            runtime: int
                Runtime of the simulation (defined by simpy package).

        Returns
        -------
        GET: dict
        POST: int
        """
        if request.method == "POST":

            # nonlocal use of the simulation count
            nonlocal simc

            # increment the simulation count
            simc += 1

            # we need a new simulation which we can run.
            simulation = Simulation()

            # let's add a basic server pool to the simulation
            servers = simulation.servers()

            # iterate over all of the servers that need to be configured that
            # we received from the client
            for kind in request.form['kinds'].split(','):

                # append a new server pool to the multiserver system
                servers.append(Servers(simulation.environment, size=int(request.form['size']), capacity=int(request.form['capacity']), kind=kind.strip()))

            # now that we have an output dir, we can construct our logger which we can use for
            # the simulation
            logger = Logger("simulation#" + str(simc))

            # we can use the logger for the simulation, so we know where all logs will be written
            simulation.use(logger)

            # we need a new form of seasonality
            seasonality = Seasonality(join('seasonality', 'week.csv'), max_volume=1000)

            # now, we can put the process in the simulation, which will know
            # how to define the process
            simulation.process(Processor, seasonality=seasonality, kinds=[kind.strip() for kind in request.form['process'].split(',')])

            # run the simulation with a certain runtime (runtime). this runtime is not equivalent
            # to the current time (measurements). this should be the seasonality of the system.
            # for example, day or week.
            simulation.run(runtime=int(request.form['runtime']))

            # expose the id of the simulation
            return jsonify(simc)

        if request.method == "GET":

            # fetch data of a simulation

            # expose the data of that simulation
            return jsonify({})


    @client.route('/get_endpoint_data')
    def get_endpoint_data():
        """
        Function to process the .csv logfile and return an endpoint_matrix
        in JSON format.
        
        Parameters
        ----------
        f: logfile name

        Returns
        -------
        GET: JSON
        """

        # Scan the logfile directory 
        log_filenames = [f for f in listdir(LOG_PATH) if isfile(join(LOG_PATH, f)) and not f.startswith('.')]

        # Only process/return endpoint_matrix if a logfile exists
        if log_filenames:

            # By default, find the most recently created file
            creation_dict = {}
            for file in log_filenames:
                (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(os.path.join(LOG_PATH, file))
                creation_dict[file] = datetime.strptime(time.ctime(mtime), '%a %b %d %H:%M:%S %Y')

            creation_dict = {k: v for k, v in sorted(creation_dict.items(), key=lambda item: item[1])}
            last_created = list(creation_dict.keys())[-1]

            # Parse URL request file f using last_created default 
            f = request.args.get('f', default=last_created)
            print("Getting endpoint_matrix for logfile:", f)

            return get_endpoint_matrix(f)

        else:
            json_convert = {"data": 0, "message": "No logfile found."}
            return jsonify(json_convert)



    @client.route('/visualization')
    def show_visualization():
        """
        Function to generate the D3/Dash visualizations of a given simulation logfile (.csv)

        URL args
        -------
        f: simulation logfile - (By default takes the first .csv in /logs)

        Returns
        -------
        GET: JSON
        """

        # Scan the logfile directory
        log_filenames = [f for f in listdir(LOG_PATH) if isfile(join(LOG_PATH, f)) and not f.startswith('.')]

        # Only process/return endpoint_matrix if a logfile exists
        if log_filenames:

            # By default, find the most recently created file, else return index page
            creation_dict = {}
            for file in log_filenames:
                (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(os.path.join(LOG_PATH, file))
                creation_dict[file] = datetime.strptime(time.ctime(mtime), '%a %b %d %H:%M:%S %Y')

            creation_dict = {k: v for k, v in sorted(creation_dict.items(), key=lambda item: item[1])}
            last_created = list(creation_dict.keys())[-1]

            # Parse URL request file f using last_created default 
            sim_file = request.args.get('f', default=last_created)
            print("Generating visualizations for:", sim_file)

            return render_template('visualization.html', sim_file=sim_file)

        else:
            return render_template('index.html', log_filenames=log_filenames, len_logfiles=len(log_filenames))




