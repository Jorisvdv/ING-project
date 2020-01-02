/**
 *  Class for constructing a form.
 *
 *  @todo   event handling.
 *
 *  @author Tycho Atsma <tycho.atsma@gmail.com>
 *  @file   web/static/js/Form.js
 *  @scope  public
 */

/**
 *  Dependencies.
 */
import { Container } from './js/Container.js';
import { FormField } from './js/FormField.js';
import { InputField } from './js/InputField.js';
import { TextField } from './js/TextField.js';
import { NumberField } from './js/NumberField.js';

/**
 *  Private property accessors.
 *  @var    Symbol
 */
const container = Symbol('container');

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
         *  Container for all the classes.
         *  @var    Container
         */
        this[container] = new Container(parent, {
            element: 'form',
            className: 'form'
        });
    }

    /**
     *  Method to instantiate a class on this form.
     *  @param  Function    Constructor function that needs to accept at least
     *                      a parent element as first parameter.
     *  @param  variadic    Additional arguments.
     *  @return mixed
     */
    instantiate(Constructor, ...args) {

        // expose the newly created class instance
        return this[container].append(Constructor, ...args);
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

        // remove the container
        this[container].remove();

        // drop the reference
        this[container] = null;
    }
};
