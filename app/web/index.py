"""
This file is the index and initialization point for the web client
of the application. All routes, static files, and configurations
should be declared here (if they relate to the entire client).

@author Tycho Atsma <tycho.atsma@gmail.com>
@file   web/index.py
@scope  public
"""

# dependencies
from flask import Flask, render_template
from multiprocessing import Process
from lib.sockets.pipeline import Pipeline

# we need to instantiate a flask application, which will be the
# backbone of the web client
client = Flask(__name__, static_url_path='', static_folder="static", template_folder="templates")

# for now, we only need to setup a single route, which will be
# the first URI the user lands on
@client.route('/')
def index():
    """
    Function to generate and expose content for the index route.

    Returns
    -------
    string
    """
    return render_template('index.html')

def main():
    """
    Function to dictate the main life cycle of the client.
    """
    # a new pipeline for the websocket processes
    pipeline = Pipeline()

    # initialize the pipeline as a process
    pprocess = Process(target=pipeline.wait)

    # initialize the client application as process
    cprocess = Process(target=client.run)

    # start the processes to initialize the application
    pprocess.start()
    cprocess.start()

# run as main
if __name__ == "__main__":
    main()
