"""
Class for acting as a server inside of a simpy simulation. This server is nothing
more than a resource with some additional patches.

@author Tycho Atsma <tycho.atsma@gmail.com>
@file   lib/Server.py
"""

# dependencies
from simpy import Resource
from lib.Logger import Logger

class Server(Resource):

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

        # reference to the environment
        self.env = args[0]

        # setup the initial state of this server
        self._state = {
            'name':  "server#%s" % kwargs['uuid'],
            'kind':  kwargs['kind'],
            'time':  round(self.env.now, 4),
            'queue': len(self.queue),
            'users': self.count
        }

        # setup a logger for this server
        self._logger = Logger(self._state['name'])

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
        """
        # update the state of the server
        self._state.update(time=round(self.env.now, 4), queue=len(self.queue), users=self.count)

        # we need to update the state with the current process id, so we can
        # track this process later on
        state = self._state.copy()
        state.update({
            "id": kwargs['process_id'] if 'process_id' in kwargs else None,
            "requested_by": kwargs['requested_by'] if 'requested_by' in kwargs else None
        })

        # we need to construct a logmessage, which we can log on this server
        # and push onto the environment
        msg = ';'.join([str(_) for _ in state.values()])

        # log the update of the state
        self._logger.log(msg)

        # push the log to the environment
        self.env.push(msg)

        # call the parent class for the original method
        return super().request()

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
