"""
Class for acting as a server inside of a simpy simulation. This server is nothing
more than a resource with some additional patches.

@author Tycho Atsma <tycho.atsma@gmail.com>
@file   src/Server.py
"""

# dependencies
from simpy import Resource
from functools import partial, wraps
import logging

def server_monitor(resource, pre=None, post=None):
    """
    Function to patch a server resource to monitor a server.
    """
    def get_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            # call the handler before the resource operation
            if pre:
                pre(resource)

            # get the resource operation value
            ret = func(*args, **kwargs)

            # call the handler after the resource operation
            if post:
                post(resource)
            
            # expose the operation return value
            return ret

        # expose the wrapper
        return wrapper

    # wrap the request operations
    if hasattr(resource, 'request'):
        setattr(resource, 'request', get_wrapper(getattr(resource, 'request')))

class Server(Resource):

    def __init__(self, uuid, env, capacity=100):
        """
        Constructor.

        Parameters
        ----------
        uuid: string
            UUID as identifier for this server.
        +
        See simpy.Resource
        """
        # call the parent constructor
        super().__init__(env, capacity=capacity)

        # setup the name of this server
        self._name = "server#%s" % uuid

        # we need a logger instance
        self._logger = logging.getLogger(self._name)
        file_handler = logging.FileHandler(self._name + '.log')
        
        # we need to add the file handler to the logger, so
        # all logs are forwarded, and written to the
        # specified file
        self._logger.addHandler(file_handler)

        # initialize an empty state
        self._state = {'time': 0, 'queue': 0, 'users': 0}

        def monitor(self):
            """Function to monitor a server."""
            self._state = {
                'time':  self._env.now,
                'queue': len(self.queue),
                'users': self.count
            }

        # install a server monitor
        server_monitor(self, post=monitor)

    def log(self, msg):
        """
        Method to log a message on this server.

        Parameters
        ----------
        msg: string
            Message to log.

        Returns
        -------
        self
        """
        self._logger.debug(msg)

    def state(self):
        """
        Method to expose the current state of a server.

        Returns
        -------
        dict
        """
        return self._state

    def latency(self):
        """
        Method to expose the server latency.

        @todo   Implement configurable latency.

        Returns
        -------
        int
        """
        return 0.01
