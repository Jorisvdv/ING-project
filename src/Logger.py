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

    def __init__(self, name, directory="logs"):
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

        # we need to get the logger with the given name
        self._logger = logging.getLogger(name)

        # we need a new file handler so the logs are written to the file
        filehandler = logging.FileHandler(os.path.join(directory, name))

        # add the file handler to the logger so all logs will be outputted there
        self._logger.addHandler(filehandler)

        # assignt the directory
        self._directory = directory

    def log(self, message, level=20):
        """
        Method to log a message.

        Parameters
        ----------
        message: string
            Message to log.
        level: integer
            Level of logging (default: 20).

        Returns
        -------
        self
        """
        
        # log the message using our logger
        self._logger.log(level, message)

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
