"""
Class for acting as a server inside of a simpy simulation. This server is nothing
more than a resource with some additional patches.

@author Tycho Atsma <tycho.atsma@gmail.com>
@file   lib/Server.py
"""

# dependencies
from simpy import Resource
from functools import wraps
from lib.Logger import Logger

def _server_monitor(resource, pre=None, post=None):
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
        super().__init__(env, capacity)

        # setup the initial state of this server
        self._state = {
            'name':  "server#%s" % uuid,
            'time':  round(env.now, 4),
            'queue': len(self.queue),
            'users': self.count
        }

        # setup a logger for this server
        self._logger = Logger(self._state['name'])

        def monitor(self):
            """
            Function to monitor a server.
            """
            # update the state of the server
            self._state.update(time=round(env.now, 4), queue=len(self.queue), users=self.count)

            # we need to construct a logmessage, which we can log on this server
            # and push onto the environment
            msg = "%(time)-15s %(name)-15s %(queue)-6s %(users)-6s" % self._state

            # log the update of the state
            self._logger.log(msg)

            # push the log to the environment
            env.push(msg)

        # install a server monitor
        _server_monitor(self, post=monitor)

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

        @todo   Implement configurable/editable latency.

        Returns
        -------
        float
        """
        return 0.01

    def memory(self):
        """
        Method to expose the server's memory usage.

        @todo   Implement configurable/editable memory.

        Returns
        -------
        float
        """
        pass

    def cpu(self):
        """
        Method to expose the server's cpu usage.

        @todo   Implement configurable/editable cpu.

        Returns
        -------
        float
        """
        pass
