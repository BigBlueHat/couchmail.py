function(doc) {
  if ('date' in doc && typeof doc.date === 'number') {
    emit(doc.date, doc.subject);
  }
}
