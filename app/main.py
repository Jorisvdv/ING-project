#!/usr/bin/env python3

# third party dependencies
from os import path

# dependencies
from lib.Simulation import Simulation
from lib.Logger import Logger
from lib.Tests import TestProcesses
from lib.SocketPusher import SocketPusher
import lib.settings as settings
import logging

# we need to setup logging configuration here,
# so all other loggers will properly function
# and behave the same
logging.basicConfig(level=logging.DEBUG)

def main():
    """
    Main application runtime.
    """
    
    # we need a new simulation which we can run. this is going to be initialized
    # with a number of servers (nservers) and the capacity for each server (ncapacity)
    simulation = Simulation(nservers=settings.NSERVERS, ncapacity=settings.NCAPACITY)

    # -- not needed right now -- #

        # we need to specify the output dir for the logger. we need to make sure the directory
        # exists, as the logger does not create one. all server logs will be outputted there
        #log_dir = 'logs'

        # now that we have an output dir, we can construct our logger which we can use for
        # the simulation
        #logger = Logger(__name__, log_dir)

        # we can use the logger for the simulation, so we know where all logs will be written
        #simulation.use(logger)

    # -- end -- #

    # we need a new socket pusher, which we can install as middleware on the simulation.
    # this causes all messages that are going through the simulation to also be pushed
    # to the web client through websockets
    simulation.use(SocketPusher())

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
