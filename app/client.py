#!/usr/bin/env python3
"""
Class for starting up a webclient, which can be used as frontend for the
simulation.

@author Tycho Atsma <tycho.atsma@gmail.com>
@file   client.py
@scope  public
"""

# dependencies
from flask import Flask
import routes

# configuration object for the flask application
config = {
    'TESTING': True,
    'ENV': 'development',
    'DEBUG': True
}

class Client(object):

    def __init__(self):
        """
        Constructor.
        """
        # we need to construct a flask application, which will be the
        # backbone of the web client
        self._client = Flask(__name__, static_url_path='', static_folder="web/static", template_folder="web/templates")

        # we need to setup some configuration variables, these may need to change
        # when running in production
        self._client.config.update(config)

    def run(self):
        """
        Method to run the client. This will start up a simple webserver.
        """

        # we need to install all routes onto the client
        routes.install(self._client)

        # run the client
        self._client.run()

# run as main
if __name__ == "__main__":

    # run a new client
    Client().run()
