function(doc) {
  var addr, key = 'cc';
  if (doc[key]) {
    addr = doc[key].match(/(?:"?([^"]*)"?\s)?(?:<?(.+@[^>]+)>?)/)
    emit([addr[2].toLowerCase(), addr[1]], doc.subject);
  }
}