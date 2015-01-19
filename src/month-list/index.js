var PouchDB = require('pouchdb');
var db = new PouchDB(location.protocol + '//' + location.hostname + ':'
    + location.port + '/' + location.pathname.split('/')[1]);

module.exports = {
  replace: true,
  data: function() {
    return {
      year: false,
      months: []
    }
  },
  watch: {
    year: function() {
      this.fetchData();
    }
  },
  methods: {
    fetchData: function() {
      var self = this;
      if (self.year) {
        db.query('couchmail/by_date',
            {
              descending: true, group_level: 2,
              startkey: [self.year, 13],
              endkey: [self.year, 0]
            })
          .then(function(rv) {
            for (var i = 0; i < rv.rows.length; i++) {
              self.months.push({
                month: rv.rows[i]['key'][1],
                count: rv.rows[i]['value']
              });
            }
          });
      }
    }
  }
}


