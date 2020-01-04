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
from flask import request, render_template
from flask.json import jsonify, load
from os import path

# we need to setup logging configuration here,
# so all other loggers will properly function
# and behave the same
import logging
logging.basicConfig(level=logging.INFO)

# dependencies
from lib.Simulation import Simulation
from lib.Logger import Logger
from lib.Tests import TestProcesses

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
        return render_template('index.html')

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
            nservers: int
                Number of servers.
            ncapacity: int
                Capacity of each server.
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

            # we need a new simulation which we can run. this is going to be initialized
            # with a number of servers (nservers) and the capacity for each server (ncapacity)
            simulation = Simulation(nservers=int(request.form['nservers']), ncapacity=int(request.form['ncapacity']))

            # now that we have an output dir, we can construct our logger which we can use for
            # the simulation
            logger = Logger(__name__ + "#" + str(simc))

            # we can use the logger for the simulation, so we know where all logs will be written
            simulation.use(logger)

            # specify a generator as callback that will be used as the main process in a simulation
            # this callback will receive an environment, and a list of available servers
            simulation.process(TestProcesses)

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
