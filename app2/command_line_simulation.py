#!/usr/bin/env python3
"""
File to start simulation from command line interface
"""

import logging
from lib.Simulation import Simulation
from lib.Servers import Servers
from lib.Logger import Logger
from lib.Processor import Processor
from lib.Seasonality import TransactionInterval as Seasonality
import os
import glob
from datetime import datetime

# we need to setup logging configuration here,
# so all other loggers will properly function
# and behave the same
logging.basicConfig(level=logging.INFO)

# Find location of file and set log location relative to that
file_dir = os.path.dirname(os.path.abspath(__file__))
location_logs = os.path.join(file_dir, "CLI_Logs")
seasonality_file = os.path.join(file_dir, 'seasonality', 'week.csv')
file_prefix = "log"
# print(file_dir, location_logs, seasonality_file, file_prefix, sep='\n')


settings = {"servers": [{"size": 5,
                         "capacity": 1000,
                         "kind": "balance"},
                        {"size": 5,
                         "capacity": 1000,
                         "kind": "credit"},
                        {"size": 5,
                         "capacity": 1000,
                         "kind": "payment"}],
            "process": "balance,payment,balance,credit",
            "runtime": 100,
            "max_volume": 1000}


# get simulation count by counting number of simulation files in folder
sim_count = len(glob.glob(os.path.join(location_logs, file_prefix+'*')))

# Interate sim_count to next number
sim_count += 1


def run_simulation(simc, settings_simulation, name_run="Test_Run",
                   seasonality_file=os.path.join(os.path.dirname(__file__),
                                                 'seasonality', 'week.csv'),
                   logs=os.path.join(os.path.dirname(__file__), "CLI_Logs"),
                   file_prefix="log"):
    # we need a new simulation which we can run.
    simulation = Simulation()

    # let's add a basic server pool to the simulation
    servers = simulation.servers()

    # iterate over all of the servers that need to be configured that
    # we received from the client
    for server in settings_simulation['servers']:

        # append a new server pool to the multiserver system
        servers.append(Servers(simulation.environment,
                               size=server['size'], capacity=server['capacity'],
                               kind=server['kind']))

    # Get the current date and time to append to the logger file name
    log_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

    # now that we have an output dir, we can construct our logger which we can use for
    # the simulation
    logger = Logger("{0}_{1:04d}_{2}".format(
        file_prefix, simc, log_timestamp), directory=location_logs)

    # we can use the logger for the simulation, so we know where all logs will be written
    simulation.use(logger)

    # we need a new form of seasonality
    seasonality = Seasonality(seasonality_file,
                              max_volume=settings_simulation["max_volume"])

    # now, we can put the process in the simulation, which will know
    # how to define the process
    simulation.process(Processor, seasonality=seasonality,
                       kinds=settings_simulation['process'].split(','))

    # run the simulation with a certain runtime (runtime). this runtime is not equivalent
    # to the current time (measurements). this should be the seasonality of the system.
    # for example, day or week.
    simulation.run(runtime=int(settings_simulation['runtime']))


if __name__ == "__main__":
    run_simulation(simc=sim_count, settings_simulation=settings,
                   seasonality_file=seasonality_file, logs=location_logs,
                   file_prefix=file_prefix)
    pass
