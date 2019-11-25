"""
Class for pushing messages to the websocket pipeline.

@author Tycho Atsma <tycho.atsma@gmail.com>
@file   web/lib/sockets/pusher.py
@scope  public
"""

# dependencies
import asyncio
import websockets

async def _send(uri, message):
    """
    Async function to send a message to a websocket.

    Parameters
    ----------
    uri: string
        URI of the websocket.
    message: mixed
        Message formatted in a way that websockets can 
        receive them.
    """
    # connect with the websocket so we can send messages
    async with websockets.connect(uri) as websocket:

        # send out the message to the pipeline
        await websocket.send(message)

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
        self._uri = "ws://{}:{}/".format(ip, port)

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
        asyncio.get_event_loop().run_until_complete(_send(self._uri, message))

        # allow chaining
        return self

# run as main
if __name__ == "__main__":

    import time

    # pusher instance
    pusher = Pusher()

    # push a message every second
    while True:
        print("push message")
        pusher.push("foo")
        time.sleep(1)

