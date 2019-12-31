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
     *  Dummy formdata.
     *  @var    FormData
     */
    const data = new FormData();

    // add all dummy data to the data object
    [["nservers", 3], ["ncapacity", 3], ["runtime", 10]].forEach(([k, v]) => data.set(k, v));

    // make a new POST request, to start a simulation
    fetch('/simulation', {
        method:     'POST',
        body:       data,
    });
};
