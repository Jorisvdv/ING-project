#!/usr/bin/env python3

# dependencies
from lib.Simulation import Simulation
from lib.Logger import Logger
from lib.Tests import TestProcesses
import lib.settings as settings
import logging

# we need to setup logging configuration here,
# so all other loggers will properly function
# and behave the same
logging.basicConfig(level=logging.INFO)

def main():
    """
    Main application runtime.
    """
    # we need a new simulation which we can run. this is going to be initialized
    # with a number of servers (nservers) and the capacity for each server (ncapacity)
    simulation = Simulation(nservers=settings.NSERVERS, ncapacity=settings.NCAPACITY)

    # now that we have an output dir, we can construct our logger which we can use for
    # the simulation
    logger = Logger(__name__)

    # we can use the logger for the simulation, so we know where all logs will be written
    simulation.use(logger)

    # specify a generator as callback that will be used as the main process in a simulation
    # this callback will receive an environment, and a list of available servers
    simulation.process(TestProcesses)

    # run the simulation with a certain runtime (runtime). this runtime is not equivalent
    # to the current time (measurements). this should be the seasonality of the system.
    # for example, day or week.
    simulation.run(runtime=settings.RUNTIME)

# run as main
if __name__ == "__main__":
    main()
