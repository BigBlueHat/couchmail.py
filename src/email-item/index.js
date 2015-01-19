module.exports = {
  replace: true,
  paramAttributes: ['messageId'],
  template: require('./template.html'),
  computed: {
    selected: function() {
      return this.$root.message_id == this.email._id;
    }
  },
  methods: {
    loadMessage: function() {
      this.$root.message_id = this.email._id;
    }
  }
}

