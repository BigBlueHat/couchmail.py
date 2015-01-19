var PouchDB = require('pouchdb');
var Vue = require('vue');
Vue.config.debug = true;

var db = new PouchDB(location.protocol + '//' + location.hostname + ':'
    + location.port + '/' + location.pathname.split('/')[1]);
window.db = db;

var months = [];

window.CouchMail = new Vue({
  el: 'body',
  data: {
    message_id: '',
    message: {},
    year: false,
    emails: []
  },
  watch: {
    message_id: function () {
      this.fetchData();
    }
  },
  created: function() {
    this.fetchEmails();
  },
  methods: {
    fetchData: function() {
      var xhr = new XMLHttpRequest(),
          self = this;
      xhr.open('GET', self.message_id);
      xhr.setRequestHeader('Accept', 'application/json');
      xhr.onload = function () {
        self.message = JSON.parse(xhr.responseText);
      }
      xhr.send();
    },
    fetchEmails: function() {
      var self = this;
      db.query('couchmail/by_date',
          {
            reduce: false,
            descending: true, limit: 20,
            include_docs: true
          })
        .then(function(rv) {
          for (var i = 0; i < rv.rows.length; i++) {
            self.emails.push(rv.rows[i]['doc']);
          }
        });
    }
  },
  components: {
    'email-item': require('./email-item'),
    'email-message': require('./email-message'),
    'year-list': require('./year-list'),
    'month-list': require('./month-list')
  }
});
