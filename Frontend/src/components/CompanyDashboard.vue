<template>
  
  <div style="height:100vh;width:100vw;">
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <h2 style="color: black;">Hello {{ this.user_data.company_name }}</h2>
        <button @click="logout()" class="btn btn-outline-danger" type="button">Logout</button>
        <div class="d-flex">
          <button @click="showprofile()" class="btn btn-outline-success" type="submit">Show Profile</button>
        </div>
  </div>
</nav>
<div>
  
  <button @click="activeTab='create'" class="btn btn-outline-primary" type="button">Create Placement drive</button>

  
  <placementDrive v-if="activeTab === 'create'"
  @change-tab="activeTab = ''" />
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
      }
      
    },
    async mounted() {
    await this.showprofile()
  }
  }
</script>
