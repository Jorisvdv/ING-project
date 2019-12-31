/**
 *  Class for building forms. This exposes a static (factory-like) interface for
 *  creating forms based on a json template.
 *
 *  @author Tycho Atsma <tycho.atsma@gmail.com>
 *  @file   web/static/js/Forms.js
 *  @scope  public
 */

/**
 *  Dependencies.
 */
import { Api } from './js/Api.js';
import { Form } from './js/Form.js';

/**
 *  Api instance for form templates.
 *  @var    Api
 */
const templates = new Api('/forms');

/**
 *  Export class definition.
 */
export class Forms {

    /**
     *  Static method to generate a form based on a json template.
     *  @param  Element Container to load the form in.
     *  @param  String  Name of the template.
     *  @return Promise
     */
    static create(parent, name) {

        // make a new request to fetch the form template
        return templates.get(name).then((json) => {

            // we need a new form to add to the container
            return new Form(parent, Object.assign({ fields: [] }, json));
        });
    }
};
