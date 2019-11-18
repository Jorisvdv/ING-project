"""
Class for setting up a pool of servers. This can be used to pool
a given number of servers and get access to an available one.

@file   lib/Servers.py
@author Tycho Atsma <tycho.atsma@gmail.com>
@scope  private
"""

# dependencies
from lib.Server import Server
from uuid import uuid4

class Servers(object):

    def __init__(self, env, size, capacity):
        """
        Constructor.

        Parameters
        ----------
        env: Environment
            The environment this pool is using.
        size: integer
            The size of the pool.
        capacity: integer
            The capacity of each server.
        """

        # we need to construct a new pool of servers
        self._pool = [Server(uuid4(), env, capacity) for i in range(size)]

    def get(self):
        """
        Method to get access to an available server from the pool.

        Returns
        -------
        Server
        """
        # we need a reference to the server with the lowest number of
        # processes in queue, which is the server that is going to
        # be targeted
        lowest = None

        # we need to iterate over the pool of servers, so we can check
        # the state of each server and find the one with the least
        # amount of traffic
        for server in self._pool:

            # assign a new server as the lowest
            if lowest is None:
                lowest = server

            # assign a new server if has a lower number of processes
            # in the queue
            elif server.state()['queue'] < lowest.state()['queue']:
                lowest = server

        # expose the server with the lowest number of processes in
        # the queue
        return lowest

