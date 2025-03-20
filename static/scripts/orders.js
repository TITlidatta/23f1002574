const app = new Vue({
    el: '#ords',
    data: {
      errors: [],
      address: null,
      rem:null,
      sid:null,
      xv:idd
    },
    methods:{
      remark: function(sid) {
        this.sid=sid;
        Swal.fire({
          title: 'Urbanlife', 
          input: 'text',
          inputLabel: 'Add Remark:',
          inputPlaceholder: 'Type here...',
          showCancelButton: true,
          customClass: {
            confirmButton: 'swal2-custom-button',
            cancelButton: 'swal2-custom-button'
          }
        }).then((result) => {
          if (result.isConfirmed) {
            this.rem = result.value; 
            v=this.rem;
            fetch('/remark/'+this.sid, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json', 
                'Authorization': 'Bearer your-access-token', 
              },
              body: JSON.stringify(v)
          }).then(response => {
              if (response.ok) {
                  console.log('Request sent successfully');
                  alert('Thanks for adding remark')
              } else {
                  console.error('Failed to send request:', response.statusText);
              }
          }).catch(error => {
              console.error('Error sending request:', error);
          }); 
          }
        });    
      },
      cancel: function(sid)
      {
        fetch('/cancel/'+sid, {
            method: 'POST',
        }).then(response => {
            if (response.ok) {
                console.log('Request sent successfully');
                alert('Order Cancelled');
            } else {
                console.error('Failed to send request:', response.statusText);
            }
        }).catch(error => {
            console.error('Error sending request:', error);
        }); 
        return 
      }, 
      rate: function(sman)
      {
        Swal.fire({
          title: 'Urbanlife', 
          input: 'text',
          inputLabel: 'Rate in range 0:being worst to 5:being best:',
          inputPlaceholder: 'Type here...',
          showCancelButton: true,
          customClass: {
            confirmButton: 'swal2-custom-button',
            cancelButton: 'swal2-custom-button'
          }
        }).then((result) => {
          if (result.isConfirmed) {
            const val = result.value; 
            fetch('/ratee/'+sman, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json', 
                'Authorization': 'Bearer your-access-token', 
              },
              body: JSON.stringify(val)
          }).then(response => {
              if (response.ok) {
                  console.log('Request sent successfully');
                  alert('Thanks for rating')
              } else {
                  console.error('Failed to send request:', response.statusText);
              }
          }).catch(error => {
              console.error('Error sending request:', error);
          });   
          }
        });
        
        
      }, 
      blockk: function(sid) {
            fetch('/blockk/'+ this.xv +'/'+sid, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json', 
                'Authorization': 'Bearer your-access-token', 
              },
          }).then(response => {
              if (response.ok) {
                  alert('Professional Blocked')
              } else {
                  console.error('Failed to send request:', response.statusText);
              }
          }).catch(error => {
              console.error('Error sending request:', error);
          }); 
      },
      unblockk: function(sid) {
          fetch('/unblockk/'+ this.xv +'/'+sid, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json', 
                'Authorization': 'Bearer your-access-token', 
              },
          }).then(response => {
              if (response.ok) {
                  alert('Professional Unblocked')
              } else {
                  console.error('Failed to send request:', response.statusText);
              }
          }).catch(error => {
              console.error('Error sending request:', error);
          });   
    },
  }
  })