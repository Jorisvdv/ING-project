"""
Class for acting as a server inside of a simpy simulation. This server is nothing
more than a resource with some additional patches.

@author Tycho Atsma <tycho.atsma@gmail.com>
@file   src/Server.py
"""

# dependencies
from simpy import Resource
from functools import partial, wraps

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

def monitor(data, resource):
    """Function to monitor a server."""
    print("server process request - {}".format(resource._env.now))

    # we need to add the metrics to a data container
    data.append((
        resource._env.now,
        resource.count
    ))

class Server(Resource):

    def __init__(self, *args, **kwargs):
        """
        Constructor.

        Parameters
        ----------
        See simpy.Resource
        """
        # call the parent constructor
        super().__init__(*args, **kwargs)

        # init empty metrics container
        self.metrics = []

        # bind monitor method to data
        monitor = partial(monitor, self.metrics)

        # install a server monitor
        server_monitor(self, pre=monitor)

    def metrics(self):
        """
        Method to expose metrics of the current state of a server.

        Returns
        -------
        list
        """
        return self.metrics

    def latency(self):
        """
        Method to expose the server latency.

        @todo   Implement configurable latency.

        Returns
        -------
        int
        """
        return 0.01