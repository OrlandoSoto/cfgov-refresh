'use strict';

/* Notes:
   - gulp/tasks/scripts.js handles js recompiling with webpack --watch flag.
   - gulp/tasks/browserSync.js watches and reloads compiled files.
*/

var gulp = require( 'gulp' );
var config = require( '../config' );

gulp.task( 'watch', [ 'browserSync' ], function() {
  gulp.watch( config.scripts.src, [ 'scripts' ] );
  gulp.watch( config.styles.cwd + '/**/*.less', [ 'styles' ] );
  gulp.watch( config.images.src, [ 'images' ] );
} );
