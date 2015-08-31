function(doc) {
  // message-id should === _id, but there are cases where message-id is not
  // properly set, and we use a timestamp based on the Date header instead.
  if ('headers' in doc && 'message-id' in doc.headers) {
    emit(doc.headers['message-id'], 1);
  } else {
    emit(null, 1);
  }
}
