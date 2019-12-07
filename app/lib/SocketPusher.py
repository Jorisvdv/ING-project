"""
Class for combining the client, socket pushing interface with the
simulation middelware interface. This allows for installing a
pusher as middleware on a simulation.

@author Tycho Atsma <tycho.atsma@gmail.com>
@file   lib/SocketPusher.py
@scope  public
"""

# dependencies
from lib.Middleware import Middleware
from web.sockets.pusher import Pusher
import json

class SocketPusher(Pusher, Middleware):

    def __init__(self):
        """
        Constructor.
        """
        Pusher.__init__(self)
        Middleware.__init__(self)

    def pipe(self, message):
        """
        Method to pipe a message over a websocket.

        Parameters
        ----------
        message: string
            Message to push over a socket.

        Returns
        -------
        self
        """
        # if the message is valid, the message can be pushed
        # over a socket connection
        if message:

            # convert the message to json, as the socket expects
            # a json string
            self.push(json.dumps(message))

        # allow chaining
        return self
