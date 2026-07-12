<template>
  <div style="height:100vh;width:100vw;">
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <h2 style="color: black;">Hello {{ this.user_data.name}}</h2>
        <button @click="logout()" class="btn btn-outline-danger" type="button">Logout</button>
        
    
    
  </div>
</nav>

  <div>
    <div>
      <button @click="activeTab='create'" class="btn btn-outline-success" type="button">Update Profile</button>
          <updatestudent v-if="activeTab === 'create'" @change-tab="activeTab = ''" />
    </div>
    <div class="table" style="margin-top: 10px;height: 250px; overflow-y: auto; overflow-x: auto; border: 1px solid">
      <h2>Placement drives</h2>
      <table class="table">
        <thead>
          <tr>
            <th>Company Name</th>
            <th>Industry</th>
            <th>Location</th>
            <th>Website</th>
            <th>Hr contact</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="company in company_data" :key="company.id">
            <td>{{ company.company_name }}</td>
            <td>{{ company.industry }}</td>
            <td>{{ company.location }}</td>
            <td>{{ company.website }}</td>
            <td>{{ company.hr_contact }}</td>
            <td>
              <button @click="selectedCompany=company.id; activeTab='show_drive'" class="btn btn-primary">check placement drives</button>
            </td>
          </tr>
        </tbody>
      </table>

      
    </div>
    <showdrive v-if="activeTab==='show_drive'" :company-id="selectedCompany" @change-tab="activeTab = ''"/>
  </div>
  </div>
</template>

<script>
import axios from 'axios'
import updatestudent from './updatestudent.vue';
import showdrive from './showdrive.vue'
export default {
  name: 'StudentDashboard',
  components:{
    updatestudent,
    showdrive
  },
  data() {
    return {
      activeTab:'',
      currentUser: {},
      company_data:[],
      user_data :{},
      selectedCompany:0,
      // Add any data properties you need for the student dashboard
    }
  },

  methods: {
    logout() {
      localStorage.removeItem('token')
      this.$router.push('/admin-login')
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


      async fetchcompanies() {
      try {
        const token = localStorage.getItem('token')
        const response = await axios.get('http://localhost:5000/api/companies', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        this.company_data = response.data
      } catch (error) {
        console.error('Error fetching companies:', error)
      }
  },
    
    checkplacementdrive(companyId) {
      this.$router.push({ name: 'PlacementDrive', params: { companyId } })
    },
    updateprof() {
      this.$router.push('/update-profile')
    }
  },

  async mounted() {
    this.fetchcompanies()
    this.showprofile()
  }
}
</script>
