const browserSync = require('browser-sync').create();

browserSync.init({
    files: ['app/static/**/*', '**/templates/**/*'],
    proxy: 'http://localhost:8000',
    open: false,
    notify: false,
});
