"""
Class for designing and running a simpy simulation.

This class should be the starting point of every simulation, and 
the only class that you should construct if you want to run simulations.

See the constructor documentation to find out how you can configure the
initial start of a simulation.

@file   lib/Simulation.py
@author Tycho Atsma <tycho.atsma@gmail.com>
@scope  public
"""

# dependencies
import simpy
from lib.Environment import Environment
from lib.MultiServers import MultiServers

class Simulation(object):

    # running state of a simulation
    _runs = False

    # collection of processes
    _processes = []

    # collection of running process
    _running = []

    def __init__(self):
        """
        Constructor.
        """
        # we need a new environment, which is where all processes,
        # resources, and other are taking place and run within
        # a simulation
        self._env = Environment()

        # we need a new multiservers pool, which we can append pools to
        self._multiserver = MultiServers()

    @property
    def environment(self):
        """
        Getter to expose the environment.

        @todo   Find solution which can get rid of this method so the env is
                not exposed to the outside world.
        
        Returns
        -------
        simpy.Environment
        """
        return self._env

    def servers(self):
        """
        Method to get access to the multiservers system. This way you can append
        server pools to the system.

        Returns
        -------
        MultiServers
        """
        # expose the multiserver system
        return self._multiserver

    def use(self, middleware):
        """
        Method to install middleware on a simulation. All middlewares receive
        the output from a simulation. If you want to create your own middleware
        you can create your own class that exposes a Middleware interface.

        Parameters
        ----------
        middleware: Middleware
            An instance of middleware to apply on a simulation.

        Returns
        -------
        self
        """
        # append the middleware to the collection of middlewares
        self._env.use(middleware)

        # allow chaining
        return self

    def process(self, Process, **kwargs):
        """
        Method to install a process on a simulation. This will be called whenever a
        simulatio is run. Each callback receives the simulation environment and
        active server as default arguments, respectively.

        Parameters
        ----------
        Process: Process
            Process to run on a simulation.

        Keyworded parameters
        --------------------
        Arguments for the process class constructor.

        Returns
        -------
        self
        """
        
        # install this callback on the collection of processes
        self._processes.append([Process, kwargs])

        # allow chaining
        return self

    def run(self, runtime=100):
        """
        Method to run a simulation. After calling this method, every other
        method becomes obsolete.

        Parameters
        ----------
        runtime: integer|(@todo support named input as string)
            The total number of simulation time units that
            the simulation will run.

        Returns
        -------
        boolean
        """

        # we need to check if a simulation is already running, if so,
        # don't continue
        if self._runs:
            return False

        # we need to iterate over each process so that it can be installed as process and run
        for [Process, kwargs] in self._processes:

            # append the process to the collection of running processes
            self._running.append(Process(self._env, self._multiserver, **kwargs))

        # we can run the simulation until the given runtime
        self._env.run(until=runtime)

        # we need to update the state of this simulation, as we do not allow for
        # multiple simulation run simultaneously
        self._runs = True

        # expose the success of the start of a simulation
        return True
