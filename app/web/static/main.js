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
};
