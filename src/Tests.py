"""
Module which exposes a number of test utilities. For example, a test process.
Note that these should not be used for debugging purposes, but for testing
final behavior.
Please add unittests, or any other kind, to the /tests directory for
testing and debugging purposes.

@file   src/Tests.py
@author Tycho Atsma <tycho.atsma@gmail.com>
@scope  public
"""

# dependencies
from Process import Process

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
        
        # yield a simply timeout using the environment. note that we can use the
        # "private" variable, as we extend from it and it belongs to this class
        yield self._env.timeout(3)
