"""
Class for setting up a pipeline websocket connections can be made with
meant to enforce a push-and-pull architecture. Pusher classes should
connect to this pipeline, with the single purpose of pushing messages
through the pipeline. This class will then echo everything out, which
is meant for listener classes to listen to.

Note, that for now, this class will most likely be a singleton.
Please remove this comment when this has changed.

@author Tycho Atsma <tycho.atsma@gmail.com>
@file   web/lib/sockets/pipeline.py
@scope  public
"""

# dependencies
import asyncio
import websockets

# Collection of unique sockets which are communicating
# through the pipeline. the pipeline is echoing all
# messages out to a listener. however, we can receive
# many push calls from many connections, therefore
# we need to track those and echo everything back
# as we don't know which one sent one
# @var  set
sockets = set()

async def _echo(websocket, path):
    """
    Function for echoing websocket messages.

    Parameters
    ----------
    websocket: websockets.server.WebSocketServer
        Websocket instance to listen to and echo back.
    path: string
        Path pointing to the websocket instance.
    """
    # run indefinitely
    while True:

        # remember each connection so we can echo messages
        # back over that connection
        sockets.add(websocket)

        try:
            # we need to wait until we receive a message from a
            # pusher so we can push it to the pipeline
            pulled = await websocket.recv()
            
            # we need to push the same message out again, so others
            # on the other side of the pipeline can listen to it
            await asyncio.wait([socket.send(pulled) for socket in sockets])

        except websockets.ConnectionClosed:
            # at this point, we don't care about errors
            pass

        finally:
            # forget the connection when it closes, so we don't echo messages
            # into the void
            sockets.remove(websocket)

class Pipeline(object):

    def wait(self, ip="127.0.0.1", port=80):
        """
        Method to serve a websocket server and wait for incoming
        messages, which will be broadcast / echoed out again.

        Parameters
        ----------
        ip: string
            IP address the socket can be served on.
        port: integer
            Port corresponding with the IP address.

        Returns
        -------
        self
        """
        # start serving over a connection
        server = websockets.serve(_echo, ip, port)

        # run the server indefinitely
        asyncio.get_event_loop().run_until_complete(server)
        asyncio.get_event_loop().run_forever()

# run as main
if __name__ == "__main__":

    # a new socket pipeline
    socket = Pipeline()

    # wait for incoming messages
    socket.wait()
