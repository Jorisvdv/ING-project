"""
Class for setting up a pool of servers. This can be used to pool
a given number of servers and get access to an available one.

@file   src/Servers.py
@author Tycho Atsma <tycho.atsma@gmail.com>
@scope  private
"""

# dependencies
from src.Server import Server
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

        # we need to iterate over all pools and find out if one has
        # space left in the queue
        for server in self._pool:

            # we need to get the current state of the server
            state = server.state()

            # if there's space left in the queue, expose the server
            # as an available one
            if state['queue'] < state['users']:
                return server

        # we need a reference to the server with the lowest number of
        # processes in queue
        lowest = None

        # all servers all full, then get the server with the least
        # number of users in the queue
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

