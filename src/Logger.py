"""
Class for logging. This class can be used for logging processes that 
occur within a simulation given a certain level. This can be installed 
a middleware on a simulation.

@file   src/Logger.py
@author Tycho Atsma <tycho.atsma@gmail.com>
@scope  private
"""

# dependencies
from Middleware import Middleware
import logging
import os

class Logger(Middleware):

    def __init__(self, directory="logs"):
        """
        Constructor.
        
        Parameters
        ----------
        directory: string
            Path to a directory where all logfiles should be written
            to. Note that this directory must exist before logging.

        Throws
        ------
        ValueError
            Is raised when the directory does not exist.
        """

        # we need to check if the given directory path actually
        # points to an existing directory, otherwise we stop
        if not os.path.isdir(directory):
            raise ValueError("directory does not exist")

        # assignt the directory
        self._directory = directory

    def log(self, message):
        """
        Method to log a message.

        Parameters
        ----------
        message: string
            Message to log.

        Returns
        -------
        self
        """

        # @todo find a way to log to a specific file
        print("log: {}".format(message))

        # allow chaining
        return self

    def pipe(self, message):
        """
        Method to pipe a message to this logger.

        Parameters
        ----------
        message: string
            Message to pipe through this logger.

        Returns
        -------
        self
        """

        # log the message
        self.log(message)
        
        # allow chaining
        return self
