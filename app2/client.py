#!/usr/bin/env python3
"""
Class for starting up a webclient, which can be used as frontend for the
simulation.

@author Tycho Atsma <tycho.atsma@gmail.com>
@file   client.py
@scope  public
"""

# 3rd party dependencies
from flask import Flask
from dash import Dash

# dependencies
import routes
from lib.LogProcessing import show_dash_graphs

class Client(object):

    def __init__(self, config):
        """
        Constructor.

        Parameters
        ----------
        config: dict
            Configuration for the flask application.
        """
        # we need to construct a flask application, which will be the
        # backbone of the web client
        self._client = Flask(__name__, static_url_path='', static_folder="web/static", template_folder="web/templates")
        self._dashapp = Dash(__name__, server=self._client, routes_pathname_prefix='/dash/')

        # we need to setup some configuration variables, these may need to change
        # when running in production
        self._client.config.update(config)

        # we need to install all routes onto the client
        show_dash_graphs(self._dashapp)
        routes.install(self._client)

    def run(self):
        """
        Method to run the client. This will start up a simple webserver.
        """
        # run the dash application
        self._dashapp.run_server(debug=True)

# run as main
if __name__ == "__main__":

    # run a new client
    Client({
        'TESTING':  True,
        'ENV':     'development',
        'DEBUG':    True
    }).run()
