#!/usr/bin/env python3
"""
Script to run the simulation as CLI tool.

@file   command_line_simulation.py
"""

# dependencies
from lib.Simulation import Simulation
from lib.Servers import Servers
from lib.Logger import Logger
from lib.Processor import Processor
from lib.Seasonality import TransactionInterval as Seasonality

# 3rd party dependencies
import os
import glob
from datetime import datetime

# we need to setup logging configuration here,
# so all other loggers will properly function
# and behave the same
import logging
logging.basicConfig(level=logging.INFO)

def main(n, config, seasonality, log_dir, log_prefix):
    """
    Main loop that runs a simulation. This simulation can be configured by passing
    a configuration dictionary, and specifying where all logs will be written to.

    Parameters
    ----------
    n: int
        The Nth simulation.
    config: dict
        Configuration for the simulation. Should contain the following keys:
        - servers:      List of dictionaries, describing a server pool.
        - process:      Sequence of kinds of servers, describing how a process within
                        the simulation runs.
        - runtime:      Until when the simulation should run.
        - max_volumne:  Maximum number of events.
    seasonality: Seasonality
        Seasonality object to use for the simulation. This defines the intervals
        between events.
    log_dir: string
        Path pointing to where all logs should be written.
    log_prefix: string
        Prefix of every log file.

    Returns
    -------
    bool
    """
    # we need a new simulation which we can run.
    simulation = Simulation()

    # let's add a basic server pool to the simulation
    servers = simulation.servers()

    # iterate over all of the servers that need to be configured that
    # we received from the client
    for server in config['servers']:

        # append a new server pool to the multiserver system
        servers.append(Servers(simulation.environment, size=server['size'], capacity=server['capacity'], kind=server['kind']))

    # we need a logger that will log all events that happen in the simulation
    name    = "{0}_{1:04d}_{2}".format(log_prefix, n, datetime.now().strftime("%Y-%m-%d_%H-%M"))
    logger  = Logger(name, directory=log_dir)

    # we can use the logger for the simulation, so we know where all logs will be written
    simulation.use(logger)

    # we need a new form of seasonality
    seasonality = Seasonality(seasonality, max_volume=config["max_volume"])

    # now, we can put the process in the simulation, which will know
    # how to define the process
    simulation.process(Processor, seasonality=seasonality, kinds=config['process'])

    # run the simulation with a certain runtime (runtime). this runtime is not equivalent
    # to the current time (measurements). this should be the seasonality of the system.
    # for example, day or week.
    return simulation.run(runtime=int(config['runtime']))

# run this as main
if __name__ == "__main__":

    # configuration for the simulation to run
    config = {
        "servers": [{
            "size":     5,
            "capacity": 1000,
            "kind":     "balance"
        }, {
            "size":     5,
            "capacity": 1000,
            "kind":     "credit"
        }, {
            "size":     5,
            "capacity": 1000,
            "kind":     "payment"
        }],
        "process":    ["balance","payment","balance","credit"],
        "runtime":    100,
        "max_volume": 1000
    }

    # Find location of file and set log location relative to that
    file_dir    = os.path.dirname(os.path.abspath(__file__))
    log_dir     = os.path.join(file_dir, "CLI_Logs")
    seasonality = os.path.join(file_dir, 'seasonality', 'week.csv')
    log_prefix  = "log"

    # get simulation count by counting number of simulation files in folder
    n = len(glob.glob(os.path.join(log_dir, log_prefix+'*'))) + 1

    # run main
    main(n=n, config=config, seasonality=seasonality, log_dir=log_dir, log_prefix=log_prefix)
