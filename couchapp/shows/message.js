function (doc, req) {
  var mustache = require('lib/mustache');
  if (doc) {
    return mustache.to_html(this.templates.layout, {message: doc}, this.templates);
  } else {
    // 404
  }
}
