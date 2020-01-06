/**
 *  Main function loop for the webclient code.
 *
 *  @author Tycho Atsma <tycho.atsma@gmail.com>
 *  @file   static/main.js
 *  @scope  public
 */

// strict checks
'use strict';

// test dependencies
import { Forms } from './js/Forms.js';
import { api } from './js/Api.js';

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

    const data = new FormData();
    data.append('nservers', 5);
    data.append('ncapacity', 5);
    data.append('runtime', 5);
    api.post('/simulation', data);

    /**
     *  Test form.
     */
    Forms.create(dummy, '/test.json').then((form) => {

        // has been created
        console.log('form has been created');
    });
};
