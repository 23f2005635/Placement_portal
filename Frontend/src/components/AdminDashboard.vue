<template>
  <div style="height:100vh;width:100vw;">
    
    <!-- <div style="align-items: center;justify-content:center;display:flex;height:10vh;width:100vw;">
      <nav style="display:inline-flex;width:95vw;height:10vh;border: 1px solid #ccc;">
      <h3 style="margin-right: 25px;">hello Admin </h3>
      <button @click="logout()" style="margin-right: 10px;">logout</button>
    </nav>
    </div> -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <h2 style="color: black;">Hello admin</h2>
        <button @click="logout()" class="btn btn-outline-danger" type="button">Logout</button>
        <!-- <form class="d-flex">
          <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" >
          <button @click="searchData()" class="btn btn-outline-success" type="submit">Search</button>
        </form> -->
      </div>

    </nav>
    <div style="display: inline-flex;line-height: 100px;width: 100vw;justify-content: space-evenly;margin-top: 20px;margin-bottom: 20px;">
      <div style="height:100px;width:30%;border: 1px solid;background-color: white;color: black;">Total Students: {{ total_students }}</div>
      <div style="height:100px;width:30%;border: 1px solid;background-color: white;color: black;">Total Companies: {{ total_companies }}</div>
      <div style="height:100px;width:30%;border: 1px solid;background-color: white;color: black;"> Total Placements: {{ total_placements }}</div> 
    </div>
    <div>
      <h2>application for company</h2> 
      <table class="table">
      
       <thead>
        <tr>
          <th>Username</th>
          <th>Email</th>
          <th>Actions</th>
        </tr>
       </thead>
       <tbody>
        <tr v-for="company in pending_companies" :key="company.id">
          <td>{{ company.username }}</td>
          <td>{{ company.email }}</td>
          <td>
            <button @click="selectedCompany = company.id; approveCompany()" class="btn btn-success">Approve</button>
            <button @click="selectedCompany = company.user_id; rejectCompany()" class="btn btn-danger">Reject</button>
          </td>
        </tr>
      </tbody>
    </table>
    </div>

    <div>
      <h2>Registered Students</h2>
      <table class="table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Branch</th>
            <th>Cgpa</th>
            <th>Action</th>

          </tr>
        </thead>
        <tbody>
          <tr v-for="st in student" :key="st.id">
            <td>{{ st.name }}</td>
            <td>{{ st.branch }}</td>
            <td>{{ st.cgpa }}</td>
            <td> <button @click="selectedCompany = st.user_id; rejectCompany()" class="btn btn-danger">Blacklist</button></td>
          </tr>
        </tbody>
      </table>
    </div>


    <div>
      <h2>Registered Companies</h2>
      <table class="table">
        <thead>
          <tr>
            <th>Name</th>
            <th>profile</th>
            <th>industry</th>
            <th>location</th>
            <th>Hr Contact</th>
            <th>Websites</th>
            <th>Action</th>
            

          </tr>
        </thead>
        <tbody>
          <tr v-for="c in company" :key="c.id">
            <td>{{ c.name }}</td>
            <td>{{ c.profile }}</td>
            <td>{{ c.industry }}</td>
            <td>{{ c.location }}</td>
            <td>{{ c.hr_contact }}</td>
            <td>{{ c.website }}</td>
            <td> <button @click="selectedCompany = c.user_id; rejectCompany()" class="btn btn-danger">Blacklist</button></td>
          </tr>
        </tbody>
      </table>
    </div>

    <div>
      <h2>application for Placement Drive</h2> 
      <table class="table">
      
       <thead>
        <tr>
          <th>Company Name</th>
          <th>Job Title</th>
          <th>Job Description</th>
          <th>Work Location</th>
          <th>Hr Contact</th>
          <th>Actions</th>
        </tr>
       </thead>
       <tbody>
        <tr v-for="p in pending_drive" :key="p.id">
          <td>{{ p.company_name }}</td>
          <td>{{ p.job_title }}</td>
          <td>{{ p.job_description }}</td>
          <td>{{ p.work_location }}</td>
          <td>{{ p.hr_contact }}</td>
          <td>
            <button @click="selecteddrive = p.id; approveDrive()" class="btn btn-success">Approve</button>
            <button @click="selecteddrive = p.id; removeDrive()" class="btn btn-danger">Reject</button>
          </td>
        </tr>
      </tbody>
    </table>
    </div>

    <div>
      <h2>Student application</h2>
      <table class="table"> 
      <thead>
        <tr>
          <th>Username</th>
          <th>Email</th>
          <th>Drive id</th>
          <th>Job title</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="appl in studentapplication" :key="appl.id">
          <td>{{ appl.username }}</td>
          <td>{{ appl.email }}</td>
          <td>
            <button @click=" showapplication()" class="btn btn-success">view</button>
            
          </td>
        </tr>
      </tbody>
    </table>
    </div>

    </div>
    
</template>

<script>
import axios from 'axios'
export default {
  name: 'AdminDashboard',
  data() {
    return {
      total_students: 0,
      total_companies: 0,
      total_placements: 0,
      company:[],
      student:[],
      pending_companies:[],
      studentapplication:[],
      pending_drive:[],
      selectedCompany: 0,
      selecteddrive:0
      // Add any data properties you need for the admin dashboard
    }
  },


  methods: {
    logout() {
      localStorage.removeItem('admin_token')
      this.$router.push('/admin-login')
    },
    async fetchtotaldata() {
      try {
        const token = localStorage.getItem('admin_token')
        const response = await axios.get('http://localhost:5000/api/admin/fetchtotaldetails', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        // console.log('Admin Dashboard response:', response.data)
        this.total_students = response.data.total_students
        this.total_companies = response.data.total_companies
        this.total_placements = response.data.total_placements
        this.pending_companies = response.data.pending_companies
        this.pending_drive = response.data.pending_drive
        this.company = response.data.company
        this.student = response.data.student
        this.studentapplication = response.data.studentapplication
      } catch (error) {
        console.log(error.response.status);
        console.log(error.response.data);
        console.error('Admin Dashboard error:', error)
      }
    },



    async approveCompany() {
      try {
        const token = localStorage.getItem('admin_token')
        await axios.post('http://localhost:5000/api/admin/approve_company',{
        company_id: this.selectedCompany
      }, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        this.pending_companies = this.pending_companies.filter(
    c => c.id !== this.selectedCompany
)
      } catch (error) {
        console.error('Error approving company:', error)
      }

        await this.fetchtotaldata()


    // async searchData() {
    //   try {
    //     const token = localStorage.getItem('admin_token')
    //     const response = await axios.post(`http://localhost:5000/api/admin/search_users_companies`, {
    //       search: this.search
    //     }, {
    //       headers: {
    //         Authorization: `Bearer ${token}`,
    //       },
    //     })
    //     console.log('Search response:', response.data)
    //     this.company_data = response.data.companies
    //     this.student_data = response.data.students
    //     // Handle the search results as needed
    //   } catch (error) {
    //     console.error('Search error:', error)
    //   }
    // },



    // async fetchPendingCompanies() {
    //   try {
    //     const token = localStorage.getItem('admin_token')
    //     const response = await axios.get('http://localhost:5000/api/admin/fetch_pending_companies', {
    //       headers: {
    //         Authorization: `Bearer ${token}`,
    //       },
    //     })
    //     console.log('Pending Companies response:', response.data)
    //     this.pending_companies = response.data.pending_companies
    //   } catch (error) {
    //     console.error('Pending Companies error:', error)
    //   }
    // },

  },
  async rejectCompany(){
      try {
        const token = localStorage.getItem('admin_token')
        await axios.post('http://localhost:5000/api/admin/remove_company',{
        company_id: this.selectedCompany
      }, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        this.pending_companies = this.pending_companies.filter(
      c => c.id !== this.selectedCompany)
      } catch (error) {
        console.error('Error approving company:', error)
      }

        await this.fetchtotaldata()




      },
  async approveDrive() {
      try {
        const token = localStorage.getItem('admin_token')
        await axios.post('http://localhost:5000/api/admin/approve_drive',{
        drive_id: this.selecteddrive
      }, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        this.pending_drive = this.pending_drive.filter(
    c => c.id !== this.selecteddrive
)
      } catch (error) {
        console.error('Error approving drive:', error)
      }

        await this.fetchtotaldata()

    },
    async removeDrive() {
      try {
        const token = localStorage.getItem('admin_token')
        await axios.post('http://localhost:5000/api/admin/remove_drive',{
        drive_id: this.selecteddrive
      }, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        this.pending_drive = this.pending_drive.filter(
    c => c.id !== this.selecteddrive
)
      } catch (error) {
        console.error('Error approving drive:', error)
      }

        await this.fetchtotaldata()

    },

  },






  mounted() {
    this.fetchtotaldata();
    // this.approveCompany();
  },
}   

</script>