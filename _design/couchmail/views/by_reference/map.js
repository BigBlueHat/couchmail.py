function(doc) {
  var reference = null;
  if (doc.headers.reference) {
    reference = doc.headers.reference;
  } else if (doc.headers.Reference) {
    reference = doc.headers.Reference;
  }
  if (reference !== null) {
    emit([reference].append(doc.date), doc.subject);
  }
}