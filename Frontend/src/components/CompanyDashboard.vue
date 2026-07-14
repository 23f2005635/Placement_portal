<template>
  
  <div style="height:100vh;width:100vw;">
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <h2 style="color: black;">Hello {{ this.user_data.company_name }}</h2>
        <button @click="logout()" class="btn btn-outline-danger" type="button">Logout</button>
        <div class="d-flex">
          <button @click="activeTab='show' ;showprofile()" class="btn btn-outline-success" type="submit">Show Profile</button>
        </div>
  </div>
</nav>
<div>
  
  <button @click="activeTab='create'" class="btn btn-outline-primary" type="button">Create Placement drive</button>

  
  <placementDrive v-if="activeTab === 'create'"
  @change-tab="activeTab = ''" />
</div>
<div v-if="activeTab==='show'">
  <h2>{{ this.user_data.company_name }}</h2>
  <p>Email : {{ this.user_data.email }}</p>
</div>
<div>
  <div >
    <h2>The Running Drive</h2>
    <table class="table">
      <thead>
        <tr>
          <th>Drive id</th>
          <th>Job Title</th>
          <th>eligibility</th>
          <th>Action</th>
        </tr>
        
      </thead>
      <tbody>
        <tr v-for="d in drive":key="d.id">
          <td>{{ d.id }}</td>
          <td>{{ d.job_title }}</td>
          <td>{{ d.eligibility }}</td>
          <td><button @click="selecteddriveid=d.id;activeTab='showappl'" class="btn btn-outline-primary" type="button">show application</button></td>
        </tr>
      </tbody>
    </table>
    <div v-if="activeTab==='showappl'">
      <h2>Application to the placement drive you selected</h2>
      <table class="table">
        <thead>
          
          <tr >
            <th>Drive id</th>
            <th>Student id</th>
            <th>Student name</th>
            <th>application date</th>
            <th>Cgpa</th>
            <th>Action</th>
          </tr>
          
        </thead>
        <tbody>
          <tr v-for="appl in application.filter(a => a.drive_id === selecteddriveid)" :key="appl.id">
        <td>{{ appl.drive_id }}</td>
        <td>{{ appl.student_id }}</td>
        <td>{{ appl.student_name }}</td>
        <td>{{ appl.application_date }}</td>
        <td>{{ appl.cgpa }}</td>
        <td><button @click="selectedappl=appl.id;approveapplication()"class="btn btn-success">approve</button>
            <button @click="selectedappl=appl.id;removeapplication()"class="btn btn-danger">reject</button></td>
      </tr>
        </tbody>
      </table>
    </div>
  </div>
  
</div>
<div>
  
</div>

  
</div>

</template>


<script>
  import axios from 'axios'
  import placementDrive from './placementDrive.vue'

  export default{
    name: 'CompanyDashboard',
    components: {
      placementDrive
    },
    data() {
      return {
        activeTab: '',
        user_data: {},
        application:[],
        drive:[],
        selecteddriveid:0,
        selectedappl:0
        // Add any data properties you need for the company dashboard
      }
    
    },
    
    methods: {
      logout() {
        localStorage.removeItem('token')
        this.$router.push('/login')
      },
      async showprofile() {
        try {
          const token = localStorage.getItem('token');
          const response = await axios.get('http://localhost:5000/api/show_current_user', {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          const userData = response.data;
          this.user_data = userData;
        } catch (error) {
          console.error('Error fetching user profile:', error);
        }
      },
      async drive_details(){
        try{
          const token = localStorage.getItem('token');
          const response = await axios.get('http://localhost:5000/api/fetch_drive' ,
            {
              headers:{
            Authorization: `Bearer ${token}`,
            },
            }
          )
          this.application=response.data.applications
          this.drive=response.data.drives
        }catch(error){
          console.error('Error fetching user profile',error);
        }
      },
      async approveapplication(){
        try{
          const token = localStorage.getItem('token');
          const response = await axios.post('http://localhost:5000/api/approveappl' ,{id:this.selectedappl},
          {
              headers:{
            Authorization: `Bearer ${token}`,
            },
            })
        }catch(error) {
        console.error('Error approving company:', error)
      }
        await this.drive_details();
      },
      async removeapplication(){
        try{
          const token = localStorage.getItem('token');
          const response = await axios.post('http://localhost:5000/api/removeappl' ,{id:this.selectedappl},
          {
              headers:{
            Authorization: `Bearer ${token}`,
            },
            })
        }catch(error) {
        console.error('Error approving company:', error)
      }
        await this.drive_details();
      },
      
    },
    async mounted() {
    await this.showprofile();
    await this.drive_details();
  }
  }
</script>
