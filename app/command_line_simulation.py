"""
File to start simulation from command line interface
"""

# dependencies
from lib.Processor import Processor
from lib.Logger import Logger
from lib.Servers import Servers
from lib.Simulation import Simulation

# we need to setup logging configuration here,
# so all other loggers will properly function
# and behave the same
import logging
logging.basicConfig(level=logging.INFO)


location_logs = "app/CLI_Logs"
settings = {"servers": [{"size": 5,
                         "capacity": 1000,
                         "kind": "balance"}],
            "process": "balance",
            "runtime": 10}


# global simulation count
simc = 0


def run_simulation(id, settings_simulation, logs=location_logs):
    #
    # increment the simulation count
    simc = id

    # we need a new simulation which we can run.
    simulation = Simulation()

    # let's add a basic server pool to the simulation
    servers = simulation.servers()

    # iterate over all of the servers that need to be configured that
    # we received from the client
    for server in settings_simulation['servers']:

        # append a new server pool to the multiserver system
        servers.append(Servers(simulation.environment,
                               size=server['size'], capacity=server['capacity'], kind=server['kind']))

    # now that we have an output dir, we can construct our logger which we can use for
    # the simulation
    logger = Logger("simulation cli#" + str(simc), directory=location_logs)

    # we can use the logger for the simulation, so we know where all logs will be written
    simulation.use(logger)

    # now, we can put the process in the simulation, which will know
    # how to define the process
    simulation.process(Processor, kinds=settings_simulation['process'].split(','))

    # run the simulation with a certain runtime (runtime). this runtime is not equivalent
    # to the current time (measurements). this should be the seasonality of the system.
    # for example, day or week.
    simulation.run(runtime=int(settings_simulation['runtime']))


if __name__ == "__main__":
    run_simulation(1, settings)
