"""
Class for designing and running a simpy simulation.

This class should be the starting point of every simulation, and 
the only class that you should construct if you want to run simulations.

See the constructor documentation to find out how you can configure the
initial start of a simulation.

@file   src/Simulation.py
@author Tycho Atsma <tycho.atsma@gmail.com>
@scope  public
"""

# dependencies
import simpy
from uuid import uuid4

class Simulation(object):

    # running state of a simulation
    _running = False

    # collection of middlewares
    _middlewares = []

    # collection of servers
    _servers = []

    # collection of processes
    _processes = []

    # collection of running process
    _running = []

    def __init__(self, nservers=1, ncapacity=1000, **kwargs):
        """
        Constructor.

        Parameters
        ----------
        nservers: integer
            The number of servers that will be used as resources.
            default: 1
        ncapacity; integer
            The capacity of each server. Thus, the maximum workload
            that each server can handle (e.g. 1000 transations).
            default: 1000

        Keyworded arguments
        -------------------
        Nothing yet.
        """
        self._nservers = nservers
        self._ncapacity = ncapacity

        # we need a new environment, which is where all processes,
        # resources, and other are taking place and run within
        # a simulation
        self._env = simpy.Environment()

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
        self._middlewares.append(middleware)

        # allow chaining
        return self

    def process(self, process):
        """
        Method to install a process on a simulation. This will be called whenever a
        simulatio is run. Each callback receives the simulation environment and
        active server as default arguments, respectively.

        Parameters
        ----------
        process: Process
            Process to run on a simulation.

        Returns
        -------
        self
        """
        
        # install this callback on the collection of processes
        self._processes.append(process)

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
        if self._running:
            return False
        
        # we need to instantiate a number of servers, which are the primary
        # resources within a simulation. this is where the transactions
        # will be processed.
        self._servers = [Server(uuid4(), self._env, capacity=self._ncapacity) for i in range(self._nservers)]

        # we need to iterate over each process so that it can be installed as process and run
        for Process in self._processes:
            self._running.append(Process(self._env, self._servers))

        # we can run the simulation until the given runtime
        self._env.run(until=runtime)

        # we need to update the state of this simulation, as we do not allow for
        # multiple simulation run simultaneously
        self._running = True

        # expose the success of the start of a simulation
        return True
