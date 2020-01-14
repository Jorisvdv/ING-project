/**
 *  Class for containing a form field. This only acts as a container, not to be
 *  the actual field itself, a text field for example.
 *
 *  This can hold one or more of such fields, enforcing a consistent layout
 *  between forms.
 *
 *  @author Tycho Atsma <tycho.atsma@gmail.com>
 *  @file   web/static/js/FormField.js
 *  @scope  public
 */

/**
 *  Dependencies.
 */
import { Container } from './Container.js';

/**
 *  Export class definition.
 */
export class FormField extends Container {
    
    /**
     *  Constructor.
     *  @param  Element Parent element.
     */
    constructor(parent) {

        // call the parent class
        super(parent, { className: 'formfield' });
    }
};
