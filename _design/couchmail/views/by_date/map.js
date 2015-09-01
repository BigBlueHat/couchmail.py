function(doc) {
  var moment = require('views/lib/moment');
  if ('date' in doc && 'subject' in doc) {
    if (typeof doc.date === 'number') {
      // we've got a timestamp, so convert it to an array
      date = moment.unix(doc.date).toArray();
    } else {
      date = doc.date;
    }
    emit(date, doc.subject);
  }
}
