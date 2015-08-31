function(doc) {
  var keys;
  if (doc._attachments) {
    keys = Object.keys(doc._attachments);
    for (i = 0; i < keys.length; i += 1) {
      emit(keys[i], doc.subject);
    }
  }
}
