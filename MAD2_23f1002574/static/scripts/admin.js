const Customers = {
  props: ['C'],
  template: `<ul class="list-group list-group-flush"><li class="list-group-item" :style="{'background-color':'rgba(63, 63, 63, 0.529)','font-family': 'serif','font-style': 'oblique','color':'white','margin-bottom':'2vh'}" v-for="c in C">Customer id : {{ c.id }}<br>Customer name : {{ c.name }}<br>Customer email : {{ c.email }} <br><button :style="{ 'margin-left':'66vw' }"><a :href="'/custhist/'+c.id">Lookout</a></button><button :style="{ 'margin-left':'1vw' }" @click="custremove(c.id)">Remove</button></li></ul>`,
  methods:{
    custremove: function(id) {
      Swal.fire({
          title: 'Urbanlife', 
          input: 'text',
          inputLabel: 'Enter your cause:',
          inputPlaceholder: 'Type here...',
          showCancelButton: true,
          customClass: {
            confirmButton: 'swal2-custom-button',
            cancelButton: 'swal2-custom-button'
          }
        }).then((result) => {
          if (result.isConfirmed) {
            const cause = result.value; 
            fetch('/custremove/'+id, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json', 
                'Authorization': 'Bearer your-access-token', 
              },
              body: JSON.stringify(cause)
            }).then(response => {
              if (response.ok) {
                  console.log('Request sent successfully');
                  alert('Customer Removed');
              } else {
                  console.error('Failed to send request:', response.statusText);
              }
          }).catch(error => {
              console.error('Error sending request:', error);
          });
          }
        });
    },
  }
};

const Professionals = {
  props: ['P'],
  template: `<ul class="list-group list-group-flush"><li class="list-group-item"  :style="{'background-color':'rgba(63, 63, 63, 0.529)','font-family': 'serif','font-style': 'oblique','color':'white','margin-bottom':'2vh'}" v-for="p in P">Servicemen id : {{ p.id }}<br>Name: {{ p.name}} <button :style="{ 'margin-left':'-1vw','background-color': 'transparent','border': 'none','color':'white' }" @click="nam(p.id)">✎</button> <br>Date Of Joining :  {{ p.doc}}  &nbsp Service Offered :  {{p.ser}}  <br>Description : {{ p.des }} <button :style="{ 'margin-left':'-1vw','background-color': 'transparent','border': 'none','color':'white' }" @click="dep(p.id)">✎</button><br>Experience : {{ p.exp }}  <button :style="{ 'margin-left':'-1vw','background-color': 'transparent','border': 'none', 'color':'white'}" @click="exp(p.id)">✎</button> Rating : {{p.rate}} &nbsp status: {{ p.status}}<br><button :style="{ 'margin-left':'57vw' }" @click="profverify(p.name)">Verify</button><button :style="{ 'margin-left':'1vw' }" @click="profunverify(p.name)">Unverify</button><button :style="{ 'margin-left':'1vw' }" @click="profremove(p.name)">Remove</button><button :style="{ 'margin-left':'1vw' }"><a :href="'/profhist/'+ p.name">Lookout</a></button></li></ul>`,
  methods:{
    profverify: function(namee) {
      fetch('/profverify/'+namee, {
          method: 'POST',
        }).then(response => {
          if (response.ok) {
              console.log('Request sent successfully');
              alert('Marked Verified');
          } else {
              console.error('Failed to send request:', response.statusText);
          }
      }).catch(error => {
          console.error('Error sending request:', error);
      });
    },
    profunverify: function(namee) {
      fetch('/profunverify/'+namee, {
          method: 'POST',
        }).then(response => {
          if (response.ok) {
              console.log('Request sent successfully');
              alert('Professional marked under verification');
          } else {
              console.error('Failed to send request:', response.statusText);
          }
      }).catch(error => {
          console.error('Error sending request:', error);
      });
    },
    profremove: function(namee) {
      Swal.fire({
          title: 'Urbanlife', 
          input: 'text',
          inputLabel: 'Enter your cause:',
          inputPlaceholder: 'Type here...',
          showCancelButton: true,
          customClass: {
            confirmButton: 'swal2-custom-button',
            cancelButton: 'swal2-custom-button'
          }
        }).then((result) => {
          if (result.isConfirmed) {
            const cause = result.value; 
            fetch('/profremove/'+namee, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json', 
                'Authorization': 'Bearer your-access-token', 
              },
              body: JSON.stringify(cause)
            }).then(response => {
              if (response.ok) {
                  console.log('Request sent successfully');
                  alert('Professional Removed');
              } else {
                  console.error('Failed to send request:', response.statusText);
              }
          }).catch(error => {
              console.error('Error sending request:', error);
          }); 
          }
        });
    },
    nam: function(idx) {
      Swal.fire({
          title: 'Urbanlife', 
          input: 'text',
          inputLabel: 'Enter new name:',
          inputPlaceholder: 'Type here...',
          showCancelButton: true,
          customClass: {
            confirmButton: 'swal2-custom-button',
            cancelButton: 'swal2-custom-button'
          }
        }).then((result) => {
          if (result.isConfirmed) {
            const cause = result.value; 
            fetch('/nam/'+ idx, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json', 
                'Authorization': 'Bearer your-access-token', 
              },
              body: JSON.stringify(cause)
            }).then(response => {
              if (response.ok) {
                  console.log('Request sent successfully');
                  alert('Name changed');
              } else {
                  console.error('Failed to send request:', response.statusText);
              }
          }).catch(error => {
              console.error('Error sending request:', error);
          }); 
          }
        });
    },
    dep: function(idx) {
      Swal.fire({
          title: 'Urbanlife', 
          input: 'text',
          inputLabel: 'Enter new description',
          inputPlaceholder: 'Type here...',
          showCancelButton: true,
          customClass: {
            confirmButton: 'swal2-custom-button',
            cancelButton: 'swal2-custom-button'
          }
        }).then((result) => {
          if (result.isConfirmed) {
            const cause = result.value; 
            fetch('/dep/'+idx, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json', 
                'Authorization': 'Bearer your-access-token', 
              },
              body: JSON.stringify(cause)
            }).then(response => {
              if (response.ok) {
                  console.log('Request sent successfully');
                  alert('Description updated');
              } else {
                  console.error('Failed to send request:', response.statusText);
              }
          }).catch(error => {
              console.error('Error sending request:', error);
          }); 
          }
        });
    },
    exp: function(idx) {
      Swal.fire({
          title: 'Urbanlife', 
          input: 'text',
          inputLabel: 'Enter updated expirience:',
          inputPlaceholder: 'Type here...',
          showCancelButton: true,
          customClass: {
            confirmButton: 'swal2-custom-button',
            cancelButton: 'swal2-custom-button'
          }
        }).then((result) => {
          if (result.isConfirmed) {
            const cause = result.value; 
            fetch('/exp/'+idx, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json', 
                'Authorization': 'Bearer your-access-token', 
              },
              body: JSON.stringify(cause)
            }).then(response => {
              if (response.ok) {
                  console.log('Request sent successfully');
                  alert('Experience Edited');
              } else {
                  console.error('Failed to send request:', response.statusText);
              }
          }).catch(error => {
              console.error('Error sending request:', error);
          }); 
          }
        });
    },
  }
};
const Orders = {
  props: ['O'],
  template: `
  <div class="container text-center">
    <div class="row">
        <div class="col-md-4 mb-3" v-for="o in O" :key="o.id">
            <div class="border p-3 rounded bg-dark text-white">
                <h5>Order ID: {{ o.id }}</h5>
                <p>
                    <strong>Service Type:</strong> {{ o.sname }}<br>
                    <strong>Date of Order:</strong> {{ o.dob }}<br>
                    <strong>Date of Completion:</strong> {{ o.doc }}<br>
                    <strong>Professional:</strong> {{ o.prof }}<br>
                    <strong>Customer:</strong> {{ o.cust }}<br>
                    <strong>Remarks:</strong> {{ o.remark }}<br>
                    <strong>Status:</strong> {{ o.status }}<br>
                    <strong>Customer Contact:</strong> {{ o.cno }}
                </p>
            </div>
        </div>
    </div>
</div>`
}; 
const Services = {
  props: ['S'],
  template: `<ul class="list-group list-group-flush" ><li class="list-group-item" :style="{'background-color':'rgba(63, 63, 63, 0.529)','font-family': 'serif','font-style': 'oblique','color':'white','margin-bottom':'2vh'}" v-for="s in S">Service id : {{ s.id}}<br> Service Type : {{ s.name }} <br> Description : {{ s.dex}}  <button :style="{ 'margin-left':'0.5vw' }"  @click="servicedes(s.id)"> Edit</button> &nbsp &nbsp Price: {{s.price}} <button @click="servicep(s.id)"> Edit</button> <br> Time Needed : {{ s.time}} <button @click="serviced(s.id)" :style="{ 'margin-left':'72vw' }">Delete</button></li></ul>`,
  methods:{
    servicedes: function(id) {
      Swal.fire({
          title: 'Urbanlife', 
          input: 'text',
          inputLabel: 'Enter your description:',
          inputPlaceholder: 'Type here...',
          showCancelButton: true,
          customClass: {
            confirmButton: 'swal2-custom-button',
            cancelButton: 'swal2-custom-button'
          }
        }).then((result) => {
          if (result.isConfirmed) {
            const dd = result.value; 
            fetch('/servicedes/'+id, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json', 
                'Authorization': 'Bearer your-access-token', 
              },
              body: JSON.stringify(dd)
            }).then(response => {
              if (response.ok) {
                  console.log('Request sent successfully');
                  alert('Description Edited');
              } else {
                  console.error('Failed to send request:', response.statusText);
              }
          }).catch(error => {
              console.error('Error sending request:', error);
          });
          }
        });
      
    },
    servicep: function(id) {
      Swal.fire({
          title: 'Urbanlife', 
          input: 'text',
          inputLabel: 'Enter new price:',
          inputPlaceholder: 'Type here...',
          showCancelButton: true,
          customClass: {
            confirmButton: 'swal2-custom-button',
            cancelButton: 'swal2-custom-button'
          }
        }).then((result) => {
          if (result.isConfirmed) {
            const pp = result.value; 
            fetch('/servicep/'+id, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json', 
                'Authorization': 'Bearer your-access-token', 
              },
              body: JSON.stringify(pp)
            }).then(response => {
              if (response.ok) {
                  console.log('Request sent successfully');
                  alert('Price Edited');
              } else {
                  console.error('Failed to send request:', response.statusText);
              }
          }).catch(error => {
              console.error('Error sending request:', error);
          });
          }
        });
      
    },
    serviced: function(id) {
        fetch('/serviced/'+id, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json', 
                'Authorization': 'Bearer your-access-token', 
              },
            }).then(response => {
              if (response.ok) {
                  alert('Service Removed from platform');
              } else {
                  console.error('Failed to send request:', response.statusText);
              }
          }).catch(error => {
              console.error('Error sending request:', error);
          });
    }
  }
};
  const app = new Vue({
    el: '#adm',
    data: {
      errors: [],
      cust:C,
      profs:P,
      ord:O,
      serv:S,
      descr:null,
      pp:null,
      caus:null
    },
    components: {
      
      'customers': Customers,
      'professionals': Professionals,
      'orders': Orders,
      'services': Services
    },
    methods:{
    }
  })


function report(){
  fetch('/hello', {
    method: 'POST',
     }).then(response => {
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return response.blob();
    }).then(blob => {

        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'report.csv'; 
        a.click();
        window.URL.revokeObjectURL(url); 
    }).catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });

} 