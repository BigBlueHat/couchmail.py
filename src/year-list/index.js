var PouchDB = require('pouchdb');
var db = new PouchDB(location.protocol + '//' + location.hostname + ':'
    + location.port + '/' + location.pathname.split('/')[1]);

module.exports = {
  replace: true,
  template: require('./template.html'),
  data: function() {
    return {
      current: false,
      years: []
    }
  },
  created: function() {
    this.fetchData();
  },
  methods: {
    fetchData: function() {
      var self = this;
      db.query('couchmail/by_date',
          {descending: true, group_level: 1})
        .then(function(rv) {
          for (var i = 0; i < rv.rows.length; i++) {
            self.years.push({
              year: rv.rows[i]['key'][0],
              count: rv.rows[i]['value']
            });
          }
          if (!self.current) {
            self.current = self.years[0].year;
          }
        });
    }
  }
}


