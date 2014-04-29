function (doc) {
  if ('to' in doc && 'from' in doc && 'subject' in doc && 'message' in doc) {
    index('default', [doc.subject, doc.message].join(' '));
    index('to', doc.to, {store: true, facet: true});
    index('from', doc.from, {store: true, facet: true});
    index('subject', doc.subject.replace('Re: ', '').replace('Fwd: ', ''),
      {store: true, facet: true});
    // generate a number based on year + month for range counting
    index('date', (doc.date[0]*100)+doc.date[1], {store: true, facet: true});
  }
}
