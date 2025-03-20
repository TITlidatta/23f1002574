const app = new Vue({
    el: '#app',
    data: {
      errors: [],
      Name:null,
      email: null,
      password: null,
      role:null
    },
    methods:{
      checkForm: function(e) {
        if ( this.email && this.password && this.role && this.Name) {
          return true;
        }
  
        this.errors = [];
  
        if (!this.email) {
          this.errors.push('Email required.');
        }
        if (!this.password) {
            this.errors.push('password required.');
          }
        if (!this.Name) {
            this.errors.push('name required.');
        }
        if (!this.role) {
              this.errors.push('role required.');
            }
        e.preventDefault();
      }
    }
  })