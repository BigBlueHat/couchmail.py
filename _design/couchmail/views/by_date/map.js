function(doc) {
  if ('date' in doc && 'subject' in doc) {
    emit(doc.date, doc.subject);
  }
}
