"""
Class for building a process based on server kinds. This can be used to setup
a sequence of how a process within a system should go. So, which server connects
to which server, in a sequence.

@author Tycho Atsma <tycho.atsma@gmail.com>
@file   lib/Processor.py
@scope  private
"""

# 3rd party dependencies
from uuid import uuid4
from simpy import Interrupt
from simpy.resources.resource import Preempted
import pandas as pd

# dependencies
from lib.Process import Process

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
            process = Subprocess(self.environment, self._servers, kinds=self._kinds).process

            # timeout before proceeding to the next transaction
            yield process | self.environment.timeout(0.0000000001)
            yield self.environment.timeout(self._seasonality.interval(self.environment.now))

            # see if the processed timed out, so that we can interrupt it
            if not process.triggered:
                process.interrupt("timeout")

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

        # sequence of server kinds
        kinds = self._kinds

        # collection of servers processing a request
        request_df = pd.DataFrame(columns=["open_servers", "open_requests", "kind"],
                                  index=range(len(kinds)))

        # we need to iterate over all kinds
        for (idx, kind) in enumerate(kinds):

            # reference to a return loop
            return_loop = None

            # id of the current process
            process_id = uuid4()

            # Test if request is back at a previously accessed server
            if kind in request_df["kind"].values:

                # Remember first location of server
                return_loop = request_df.index[request_df['kind'] == kind].tolist()

                # Get same server as before:
                server = request_df.loc[return_loop[0], "open_servers"]

            else:
                # we need to get access to a server, so we can start a process
                server = self.servers(kind).server()

            # Set kind of server in DataFrame
            request_df.loc[idx, "kind"] = kind

            # add the open request to the collection of open servers, so
            # we can release it later on
            request_df.loc[idx, "open_servers"] = server

            # attempt to parse a server request
            try:

                # get the client who requested this process
                requested_by = {"name": 'client',
                                "kind": "client"} if idx < 1 else request_df.loc[idx - 1, "open_servers"].state()

                # ask the server for a new request
                request = server.request(exclude=[server], requested_by=requested_by['name'], process_id=process_id, message=f"Requesting {kind} by {requested_by['kind']}")

                # Add request to list of open open_requests
                request_df.loc[idx, "open_requests"] = request

                # yield the request and timeout
                yield request
                yield self.environment.timeout(server.latency())

                # When request is processed and return loop index exists
                # Release in between servers
                if return_loop:
                    drop_indexes = []

                    # release all server requests between occurances of the same kind
                    for row in request_df.iloc[return_loop[0]:idx, :].itertuples(index=True):

                        # Get server and corresponding request
                        server = getattr(row, "open_servers")
                        request = getattr(row, "open_requests")

                        # release the server request
                        server.release(request=request)

                        # Add index to remove list
                        drop_indexes.append(getattr(row, "Index"))

                    # remove closed request from DataFrame
                    request_df = request_df.drop(drop_indexes, axis=0)

            # handle interruptions
            except Interrupt as interrupt:

                # Check if error is due to interuption using error_generator
                if isinstance(interrupt.cause, Preempted):

                    # Manually print timeout message
                    self.environment.log(f"ERROR: message {process_id} timeout at time {self.environment.now}", type="error")

                else:

                    # Use interrupt clause to write error message
                    self.environment.log(f"{self.environment.now};{requested_by['name']};ERROR;{process_id};{server.state()['name']};{interrupt.cause}", type="error")

        # release all server requests
        for row in request_df.itertuples(index=False):

            # Get server and corresponding request
            server = getattr(row, "open_servers")
            request = getattr(row, "open_requests")

            # release the server request
            server.release(request=request)
