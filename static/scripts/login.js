const app = new Vue({
    el: '#app',
    data: {
      errors: [],
      email: null,
      password: null,
    },
    methods:{
        sendlog: function()
        {
            const dat={
                email:this.email,
                password:this.password
            };
            fetch('/tolog', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json', 
                  'Authorization': 'Bearer your-access-token', 
                },
                body: JSON.stringify(dat),
                redirect: 'follow'
              }).then(response => {
                if (response.ok) {
                  return response.json(); 
                } 
              })
              .then(data => {
                    if(data.x==1)
                    {
                        alert('Invalid password')
                    }
                    window.location.href = data.redirect_url; 
              })
              .catch(error => {
                console.error('Error during login:', error);
              });

        }
    }
  })





