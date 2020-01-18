"""
Class for building a process based on server kinds. This can be used to setup
a sequence of how a process within a system should go. So, which server connects
to which server, in a sequence.

@author Tycho Atsma <tycho.atsma@gmail.com>
@file   lib/Processor.py
@scope  private
"""

# dependencies
from lib.Process import Process
from uuid import uuid4
from simpy import Interrupt

class Processor(Process):

    def __init__(self, *args, **kwargs):
        """
        Constructor.

        Parameters
        ----------
        @see Process

        Keyworded parameters
        --------------------
        seasonality: Seasonality
            Source of incoming messages.
            [required]
        kinds: list
            List of server kinds as sequence.
            [optional]
        """

        # call the parent class
        super().__init__(*args)

        # required seasonality
        self._seasonality = kwargs['seasonality']

        # optional sequence of kinds
        self._kinds = kwargs['kinds'] if 'kinds' in kwargs else ['regular']

    def run(self):
        """
        Generator method to run the process.

        Yields
        ------
        simpy.Timeout|simpy.Process
        """
        # run indefinitely
        while True:

            # init a new subprocess
            Subprocess(self.environment, self._servers, kinds=self._kinds).process

            # timeout before proceeding to the next transaction
            yield self.environment.timeout(self._seasonality.interval(self.environment.now))

class Subprocess(Process):

    def __init__(self, *args, **kwargs):
        """
        Constructor.

        Parameters
        ----------
        @see Process

        Keyworded parameters
        --------------------
        kinds: list
            List of server kinds as sequence.
            [optional]
        """

        # call the parent class
        super().__init__(*args)

        # optional sequence of kinds
        self._kinds = kwargs['kinds'] if 'kinds' in kwargs else ['regular']

    def run(self):
        """
        Generator method to run the process.

        Yields
        ------
        simpy.Timeout|simpy.Process
        """
        # collection of servers processing a request
        open_servers = []

        # sequence of server kinds
        kinds = self._kinds

        # we need to iterate over all kinds
        for (idx, kind) in enumerate(kinds):

            # we need to get access to a server, so we can start a process
            server = self.servers(kind).server()

            # add the open request to the collection of open servers, so 
            # we can release it later on
            open_servers.append(server)

            # attempt to parse a server request
            try:

                # get the client who requested this process
                requested_by = { "name": 'client', "kind": "client" } if idx < 1 else open_servers[idx - 1].state()

                # ask the server for a new request
                request = server.request(exclude=[server], requested_by=requested_by['name'], process_id=uuid4(), message=f"Requesting {kind} by {requested_by['kind']}")

                # yield the request and timeout
                yield request
                yield self.environment.timeout(server.latency())

            # handle interruptions
            except Interrupt as interrupt:

                # TODO Actually log to an error log.

                # Check if error is due to interuption using error_generator
                if isinstance(interrupt.cause, simpy.resources.resource.Preempted):

                    # Manually print timeout message
                    print(f"ERROR: message {i} timeout at time {start + timeout_time}")

                else:
                    # Use interrupt clause to write error message
                    print(f"ERROR: message {i} {interrupt.cause} at time {env.now}")

        # release all server requests
        for server in open_servers:

            # release the server request
            server.release(request=request)
