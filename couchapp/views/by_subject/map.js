function(doc) {
  if (doc.subject) {
    emit(doc.subject, 1);
  }
}
