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
import { Container } from './Container.js';
import { FormField } from './FormField.js';
import { InputField } from './InputField.js';
import { TextField } from './TextField.js';
import { NumberField } from './NumberField.js';
import { Mixin } from './Mixin.js';
import { EventBus } from './EventBus.js';

/**
 *  Private property accessors.
 *  @var    Symbol
 */
const container = Symbol('container');

/**
 *  Export class definition.
 */
export class Form extends Mixin.mix(Container).with(EventBus) {

    /**
     *  Constructor.
     *  @param  Element Parent element.
     *  @param  Object  Configuration for the form. Supported options are:
     *
     *                      "fields"    Array   List of fields beloning to the form.
     */
    constructor(parent, options = {}) {

        // call the parent
        super(parent, {
            element: 'form',
            className: 'form'
        });

        // we need to check if we need to define some fields already
        if (options.fields) options.fields.forEach(this.input.bind(this));
    }

    /**
     *  Method to add a form field to the form.
     *  @return FormField
     */
    field() {

        // expose the newly constructed form field
        return this.append(FormField);
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
};
