function(doc) {
  var addr, key = 'to';
  if (doc[key]) {
    addr = doc[key].match(/(?:"?([^"]*)"?\s)?(?:<?(.+@[^>]+)>?)/)
    emit([addr[2].toLowerCase(), addr[1]], doc.subject);
  }
}