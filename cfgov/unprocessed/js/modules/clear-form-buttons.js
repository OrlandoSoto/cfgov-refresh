/* ==========================================================================
   Clear form button
   - Clear checkboxes and selects
   - Clear jquery.custom-input elements
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );

/**
 * Set up DOM references, attributes, and event handlers.
 */
function init() {
  $( '.js-form_clear' ).on( 'click', function() {
    var $this = $( this );
    var $form = $this.parents( 'form' );

    // Clear text inputs
    $form.find( 'input[type="text"]' ).val( '' );

    // Clear checkboxes
    $form.find( '[type="checkbox"]' )
    .removeAttr( 'checked' );

    // Clear radio
    $form.find( '[type="radio"]' )
    .removeAttr( 'checked' );

    // Clear select options
    $form.find( 'select option' )
    .removeAttr( 'selected' );
    $form.find( 'select option:first' )
    .attr( 'selected', true );
  } );
}

// Expose public methods.
module.exports = { init: init };
