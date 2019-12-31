"""
This file contains a function that installs a number of routes on a flask
webclient. This is more of a collection of routes than an actual function,
but this method allows us to easily call it from other places and keep that
part clean from these declarations.

@author Tycho Atsma <tycho.atsma@gmail.com>
@file   routes.py
@scope  public
"""

# dependencies
from flask import request, render_template
from flask.json import jsonify
from main import main

def install(client):
    """
    Function to install all routes onto a flask webclient.

    Parameters
    ----------
    client: Flask
        Flask application to install the routes on.
    """
    
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

    # declare endpoint for starting a new simulation
    @client.route('/simulation', methods=["GET", "POST"])
    def simulation():
        """
        Function to install handlers on the /simulation path. This allows for
        requesting simulation data or starting a new simulation.

        Returns
        -------
        GET: dict
        POST: int
        """
        if request.method == "POST":
            
            # start a new simulation
            main()

            # expose the id of the simulation
            return -1

        if request.method == "GET":

            # fetch data of a simulation

            # expose the data of that simulation
            return jsonify({})
