const app = new Vue({
    el: '#prof',
    data: {
      errors: [],
    },
    methods:{
      accept: function(sid) {
        fetch('/accept/'+sid, {
            method: 'POST',
        }).then(response => {
            if (response.ok) {
                console.log('Request sent successfully');
                alert('marked accepted');
            } else {
                console.error('Failed to send request:', response.statusText);
            }
        }).catch(error => {
            console.error('Error sending request:', error);
        });   
      },
      reject: function(sid)
      {
        fetch('/reject/'+sid, {
            method: 'POST',
        }).then(response => {
            if (response.ok) {
                console.log('Request sent successfully');
                alert('rejected service');
            } else {
                console.error('Failed to send request:', response.statusText);
            }
        }).catch(error => {
            console.error('Error sending request:', error);
        }); 
        return 
       }  
    }
  })