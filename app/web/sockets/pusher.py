"""
Class for pushing messages to the websocket pipeline.

@author Tycho Atsma <tycho.atsma@gmail.com>
@file   web/lib/sockets/pusher.py
@scope  public
"""

# dependencies
import asyncio
import websockets

import logging
logger = logging.getLogger('websockets')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

class Pusher(object):

    def __init__(self, ip="127.0.0.1", port=80):
        """
        Constructor.

        Parameters
        ----------
        ip: string
            IP address to push messages to.
        port: int
            Port that corresponds with the ip address.
        """
        # uri to connect to
        self._uri = "ws://{}:{}/".format(ip, port)

    async def connect(self):
        """
        Async method to connect to a websocket connection.

        Returns
        -------
        websockets.WebSocketCommonProtocol
        """
        # expose the connection if there is one already
        if hasattr(self, '_connection'):
            return self._connection

        # await the connection
        self._connection = await websockets.connect(self._uri)

        # if the connection is open, we can expose the connection
        if self._connection.open:
            return self._connection

    async def _send(self, message):
        """
        Async method to send a message over a websocket.

        Parameters
        ----------
        message: mixed
            Message formatted in a way that websockets can 
            receive them.
        """
        # await the connection
        async with websockets.connect(self._uri) as ws:

            # send the message
            await ws.send(message)

    def push(self, message):
        """
        Method to push a message to the pipeline.

        Parameters
        ----------
        message: mixed
            Message formatted in a way that websockets can 
            receive them.

        Returns
        -------
        self
        """
        # get access to the event loop and run the send
        # callback to push the message to the pipeline
        asyncio.get_event_loop().run_until_complete(self._send(message))

        # allow chaining
        return self

# run as main
if __name__ == "__main__":

    import time
    import json

    # pusher instance
    pusher = Pusher()

    # push a message every second
    pusher.push(json.dumps({ "type": "log", "message": "foo" }))

