const app = new Vue({
    el: '#ord',
    data: {
      errors: [],
      address: null,
      phone: null,
      select:null
    },
    methods:{
      place: function() {
            v={
              sname:sss,
              sman: this.select,
              cname: uuu,
              adrs: this.address,
              ph : this.phone
            }
            fetch('/place', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json', 
                'Authorization': 'Bearer your-access-token', 
              },
              body: JSON.stringify(v),
              redirect: 'follow'
            }).then(response => {
              if (response.ok) {
                alert('thanks for order');
                return response.json(); 
              } else {
                console.error('Failed to log in');
              }
            })
            .then(data => {
                window.location.href = data.redirect_url; 
            })
            .catch(error => {
              console.error('Error during login:', error);
            });

      },
      add: function(namex){
        this.select=namex;
      }
    }
  })