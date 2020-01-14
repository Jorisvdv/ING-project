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
from os import listdir
from os import path
from os.path import isfile, join
from flask import request, render_template
from flask.json import jsonify, load
import csv
import pandas as pd
import numpy as np

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

# Global vars
LOG_PATH = 'logs'
LOG_FILENAMES = [f for f in listdir(LOG_PATH) if isfile(join(LOG_PATH, f)) and not f.startswith('.')]

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
        return render_template('index.html', log_filenames=LOG_FILENAMES, len_logfiles=len(LOG_FILENAMES))

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
            for server in request.form['servers']:

                # append a new server pool to the multiserver system
                severs.append(Servers(simulation.environment, size=server['size'], capacity=server['capacity'], kind=server['kind']))

            # now that we have an output dir, we can construct our logger which we can use for
            # the simulation
            logger = Logger("simulation#" + str(simc))

            # we can use the logger for the simulation, so we know where all logs will be written
            simulation.use(logger)

            # now, we can put the process in the simulation, which will know
            # how to define the process
            simulation.process(Processor, kinds=request.form['process'].split(','))

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

        Returns
        -------
        GET: JSON
        """
        # Read in the log data
        filename = request.args.get('f', default=LOG_FILENAMES[0])
        log_df = pd.read_csv('logs/' + filename, sep=';')

        # Create 'final_matrix' (initially a zeros matrix)
        rows = log_df['Server'].unique()
        cols = log_df['To_Server'].unique()
        final_matrix = pd.DataFrame(0, index=cols, columns=rows)

        # Filter by Server and To_Server
        filtered_log_df = log_df[['Server', 'To_Server']]

        # Group by unique combinations and count occurrences
        df = filtered_log_df.groupby(['Server', 'To_Server']).size().reset_index().rename(columns={0:'count'})

        # Iterate over combinations in grouped_by df and fill in occurrences in final_matrix df
        for index, row in df.iterrows():
            final_matrix.loc[row['To_Server']][row['Server']] = row['count']

        # Convert 'final_matrix' df to array and prepare data for jsonify
        final_matrix_numpy = final_matrix.values.tolist()
        json_convert = {"data": final_matrix_numpy}

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

        # Parse the URL arg
        sim_file = request.args.get('f', default=LOG_FILENAMES[0])

        return render_template('visualization.html', sim_file=sim_file)




