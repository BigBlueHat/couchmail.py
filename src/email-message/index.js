var moment = require('moment');

module.exports = {
  template: require('./template.html'),
  data: function() {
    return {
      date: '',
      subject: '',
      message: ''
    }
  },
  computed: {
    dateFormatted: function() {
      if (typeof this.date === 'number') {
        return moment.unix(this.date).calendar();
      } else {
        return this.date;
      }
    },
    msg: function() {
      if (undefined !== this.message) {
        return this.message;
      } else {
        // context.io stores bodies in a `body` key
        // find the plain text one, and output that
        var message = this.body.map(function(body) {
          if (body.type == 'text/plain') {
            return body;
          }
        })[0];
        return message.content;
      }
    }
  }
};
