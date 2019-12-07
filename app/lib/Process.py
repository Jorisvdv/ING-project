"""
Class to act as base class for all processes within a simulation. This
class should not be instantiated directly, but inherited from if you
want to specify your own process.

@file   lib/Process.py
@author Tycho Atsma <tycho.atsma@gmail.com>
@scope  private
"""

# dependencies
from abc import ABCMeta, abstractmethod
import unittest

class Process(metaclass=ABCMeta):

    def __init__(self, environment, servers):
        """
        Constructor.

        Parameters
        ----------
        environment: simpy.Environment
            The environment the process is running in.
        servers: Servers
            The list of servers that are active within a simulation.
        """
        self.environment = environment
        self._servers = servers

        # we need to run this process immediately and expose the process as
        # public which allows others to interfere with it, which is allowed.
        # this could be useful for, for example, introducing errors.
        self.process = self.environment.process(self.run())

    def server(self):
        """
        Method to get access to a server from the pool of servers given
        to this process.

        Returns
        -------
        Server
        """
        return self._servers.get()

    @abstractmethod
    def run(self):
        """
        Generator method to run as simpy process.
        This needs to be implemented by child classes.

        Yields
        ------
        simpy.Timeout or simpy.Process
        """
        pass

class ProcessTestCase(unittest.TestCase):

    def test_should_not_construct(self):
        """
        Test to ensure that the class cannot be instantiated.
        """
        self.assertRaises(TypeError, Process)

# run as main
if __name__ == "__main__":
    unittest.main()
