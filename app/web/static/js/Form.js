/**
 *  Class for constructing a form.
 *
 *  @author Tycho Atsma <tycho.atsma@gmail.com>
 *  @file   web/static/js/Form.js
 *  @scope  public
 */

/**
 *  Private property accessors.
 *  @var    Symbol
 */
const container = Symbol('container');
const installed = Symbol('installed');

/**
 *  Export class definition.
 */
export class Form {

    /**
     *  Constructor.
     *  @param  Element Parent element.
     *  @param  Object  Configuration for the form. Supported options are:
     *
     *                      "fields"    Array   List of fields beloning to the form.
     */
    constructor(parent, options = {}) {

        /**
         *  Element for encapsulating the form fields.
         *  @var    Element
         */
        this[container] = document.createElement('form');

        /**
         *  Collection of installed classes.
         *  @var    WeakSet
         */
        this[installed] = new WeakSet();
    }

    /**
     *  Method to instantiate a class on this form.
     *  @param  Function    Constructor function that needs to accept at least
     *                      a parent element as first parameter.
     *  @param  variadic    Additional arguments.
     *  @return mixed
     */
    instantiate(Constructor, ...args) {

        // construct the new class
        const widget = new Constructor(this[container], ...args);

        // remember the widget
        this[installed].add(widget);

        // expose the widget
        return widget;
    }

    /**
     *  Method to add a form field to the form.
     *  @return FormField
     */
    field() {

        // expose the newly constructed form field
        return this.instantiate(FormField);
    }

    /**
     *  Method to add an input field.
     *  @param  Object  Configuration for the field. Should at least contain
     *                  a "name" and "type" property. See InputField for more info.
     *  @return InputField
     */
    input(config = {}) {

        // add a new input field
        return this.field().append(InputField, config);
    }

    /**
     *  Method to add a text input field.
     *  @param  Object  Configuration for the field. Should at least contain a
     *                  "name" property. See TextField for more info.
     *  @return TextField
     */
    text(config = {}) {

        // add a new text field
        return this.field().append(TextField, config);
    }

    /**
     *  Method to add a number input field.
     *  @param  Object  Configuration for the field. Should at least contain a
     *                  "name" property. See numberField for more info.
     *  @return numberField
     */
    number(config = {}) {
        
        // add a new number field
        return this.field().append(NumberField, config);
    }

    /**
     *  Cleanup.
     */
    remove() {

        // remove all installed classes
        for (let widget of this[installed]) widget.remove();

        // clear the installed classes
        this[installed].clear();

        // drop the reference
        this[installed] = null;

        // remove the container
        this[container].remove();

        // drop the reference
        this[container] = null;
    }
};
