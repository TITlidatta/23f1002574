function send(){
  
    const fileInput = document.getElementById('inputGroupFile02');
    const file = fileInput.files[0];
    if (file){
      console.log('okay')
    }
    const formData = new FormData();
    formData.append('file', file);
    fetch('/verifyou/'+id, {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer your-access-token', 
          },
        body: formData,
      }).then(response => {
        if (response.ok) {
            console.log('Request sent successfully');
            alert('You will be notified shortly')
        } else {
            console.error('Failed to send request:', response.statusText);
        }
    }).catch(error => {
        console.error('Error sending request:', error);
    });

    }

    const app = new Vue({
        el: '#sky',
        data: {
          Sname:null,
          imgc:null,
          des:null,
          exp:null
        },
        methods:{
            upload : function (){
               x={
                sname:this.Sname,
                imgc:this.imgc,
                des:this.des,
                exp:this.exp,
                idu:id
               }
                fetch('/getin', {
                    method: 'POST', 
                    headers: {
                      'Content-Type': 'application/json' 
                    },
                    body: JSON.stringify(x) 
                  })
                    .then(response => {
                      if (!response.ok) {
                        throw new Error('Network response was not ok');
                      }
                      else{
                        alert('Uploaded')
                      }
                    })
                    .catch(error => {
                      console.error('Error occurred:', error); 
                    });
            }
        }
      })