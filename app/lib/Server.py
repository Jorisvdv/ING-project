"""
Class for acting as a server inside of a simpy simulation. This server is nothing
more than a resource with some additional patches.

@author Tycho Atsma <tycho.atsma@gmail.com>
@file   lib/Server.py
"""

# dependencies
from simpy import PreemptiveResource
from numpy.random import exponential, uniform


class Server(PreemptiveResource):

    def __init__(self, *args, **kwargs):
        """
        Constructor.

        Parameters
        ----------
        @see simpy.Resource

        Keyworded arguments
        -------------------
        uuid: string
            UUID as identifier for this server.
        kind: string
            Kind of the server (e.g. balance, regular, database).
        """
        # call the parent constructor
        super().__init__(*args)

        # reference to the environment and capacity
        self._env = args[0]

        # setup the initial state of this server
        self._state = {
            'name':  "%s#%s" % (kwargs['kind'], kwargs['uuid']),
            'kind':  kwargs['kind'],
            'time':  round(self._env.now, 4),
            'queue': len(self.queue),
            'users': self.count,
            'cpu': 0,
            'memory': 0,
            'latency': 0,
            'latencyscaler': 10
        }

    def environment(self):
        """
        Getter to expose the environment.

        Returns
        -------
        Environment
        """
        return self._env

    def get_capacity(self):
        """
        Getter to expose the server capacity.

        Returns
        -------
        int
        """
        return self.capacity

    def request(self, *args, **kwargs):
        """
        Method override to request a context in which this resource can be accessed.
        @see https://simpy.readthedocs.io/en/latest/api_reference/simpy.resources.html#simpy.resources.resource.Request

        Keyworded parameters
        ----------
        process_id: int
            ID of the current processes requesting this server.
        requested_by: string
            Name of the entity that requested this process (e.g. client or another
            server).
        message: string
            Description of the request.
        priority: int
            See simpy.PreemptiveResource.request.
        """
        self._state.update(
            time=round(self._env.now, 4),
            queue=len(self.queue),
            users=self.count,
            cpu=self.cpu(),
            memory=self.memory(),
            latency=self.latency()
        )

        # parse parameters for the super class method
        priority = kwargs['priority'] if 'priority' in kwargs else 1

        # call the parent class for the original method
        return super().request(priority=priority)

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

        Returns
        -------
        float
        """
        state = self.state()
        # expose a random value based on an exponential distribution, scaled
        # with the cpu usage
        # return exponential(self.cpu())
        return state["cpu"] * state["latencyscaler"]

    def memory(self):
        """
        Method to expose the server's memory usage.

        Returns
        -------
        float
        """
        # get the current state
        state = self.state()

        # expose the calculated memory usage based on the queue, users, and
        # scaled capacity
        return (state['users'] + state['queue']) / (self.capacity * 10) \
            + uniform(0.001, 0.01)

    def cpu(self):
        """
        Method to expose the server's cpu usage.

        Returns
        -------
        float
        """
        # get the current state
        state = self.state()
        # expose the cpu load
        return state['users'] / self.capacity + uniform(0.001, 0.01)

    def faulty_patch(self, state):
        # error function to increase the latency scaler tenfold when true
        if state:
            self._state.update(latencyscaler=100)
        if not state:
            self._state.update(latencyscaler=10)
