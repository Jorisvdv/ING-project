"""
Module which exposes a number of test utilities. For example, a test process.
Note that these should not be used for debugging purposes, but for testing
final behavior.
Please add unittests, or any other kind, to the /tests directory for
testing and debugging purposes.

@file   lib/Tests.py
@author Tycho Atsma <tycho.atsma@gmail.com>
@scope  public
"""

# dependencies
from lib.Process import Process

class TestProcess(Process):
    """
    Class that acts as test process. This yields a simple timeout.

    @extends Process
    """

    def run(self):
        """
        Method to run the test process.

        Yields
        ------
        simpy.Timeout
        """
        # yield a simply timeout using the environment
        for i in range(10):

            # we need to get access to a server, so we
            # can fake processing something
            server = self.server()

            # ask our server for a request
            with server.request() as request:

                # yield the request and timeout
                yield request
                yield self.environment.timeout(server.latency())

class TestProcesses(Process):
    """
    Class that acts as a collection of test processes. Opposed
    to TestProcess, this will spawn multiple processes.

    @extends Process
    """

    def run(self):
        """
        Method to run the collection of test processes.

        Yields
        ------
        simpy.Timeout
        """
        # spawn an arbitrary number of processes
        for _ in range(3):

            # we need to spawn a new process on the environment
            # this collection is assigned to
            process = TestProcess(self.environment, self._servers)

            # we're not interested in this actual process, so we
            # return a nullified timeout
            yield self.environment.timeout(0)
