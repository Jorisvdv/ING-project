/**
 *  Main function loop for the webclient code.
 *
 *  @author Tycho Atsma <tycho.atsma@gmail.com>
 *  @file   static/main.js
 *  @scope  public
 */

/**
 *  Event handler that initialized when the document
 *  is ready.
 */
onload = function() {

    /**
     *  Element for encapsulating the main content of
     *  the webclient. This will hold all subsequently
     *  created classes and such.
     *  @var    Element
     */
    const mainContainer = document.getElementById('main');

    /**
     *  Dummy placeholder to show that everything works.
     *  This can be removed.
     *  @var    Element
     */
    const dummy = document.createElement('div');
    mainContainer.appendChild(dummy);

    /**
     *  Websocket that receives data from the server.
     *  @var    WebSocket
     */
    const socket = new WebSocket("ws://127.0.0.1:80/");

    // listen to messages
    socket.onmessage = (event) => {

        // apply the data to a textual node, so we can append
        // it to an element
        let textNode = document.createTextNode(event.data); 

        // append the data of the event to our dummy container,
        // so we can visibly see if the data is coming in
        dummy.appendChild(textNode); 
    };
};
