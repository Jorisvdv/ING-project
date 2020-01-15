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

class Processor(Process):

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
        """

        # call the parent class
        super().__init(self, *args)

        # we need a collection of server kinds
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
            server = self.servers(kind)

            # get the client who requested this process
            requested_by = 'client' if idx > 0 else kinds[idx - 1]

            # ask the server for a new request
            request = server.request(requested_by=requested_by, process_id=1)

            # yield the request and timeout
            yield request
            yield self.environment.timeout(server.latency())

            # add the open request to the collection of open servers, so 
            # we can release it later on
            open_servers.append(server)

        # release all server requests
        for server in open_servers:

            # release the server request
            server.release()
