<template>
  <div>

    <div>
      <h2>{{ company.name }}</h2>
    <p>{{ company.industry }}</p>
    <p>{{ company.location }}</p>

    </div>
    <div v-for="drive in placementDrives" :key="drive.id">
      <h4>{{ drive.title }}</h4>
      <button class="btn btn-primary" @click="selectedDrive=drive.id; applyForDrive()">
        Apply
      </button>
    
    </div>
    <button class="btn btn-secondary" @click="goBack()">
        Go Back
    </button>
  </div>


</template>
<script>
  import axios from 'axios'

export default {
  props: {
    companyId: {
      type: Number,
      required: true
    }
  },

  data() {
    return {
      company: {},
      placementDrives: [],
      selectedDrive:0
    }
  },
  async mounted() {
    await this.getCompanyDetails()
    await this.getPlacementDrives()
  },
  methods: {
    async getCompanyDetails() {
  try {
    const res = await axios.post(
    'http://localhost:5000/api/company/details',
    {
      company_id: this.companyId
    }
  )

  this.company = res.data.company
  this.placementDrives = res.data.placement_drives
  console.log(res.data)
console.log(this.placementDrives)
  } catch(error){
    console.error('Error creating placement drive:', error);
        console.log(error.response.status);
        console.log(error.response.data);
  }
},
goBack() {
      this.$emit('change-tab')
    },
async applyForDrive(){
  try{
  const token = localStorage.getItem('token')
  const res = await axios.post(
    'http://localhost:5000/api/ApplyPlacement',
    {
      drive_id: this.selectedDrive
    },
    {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
      alert("Applied")
    }  catch (error) {
        console.error('Error approving drive:', error)
        console.log(error.response.status);
        console.log(error.response.data);
      }
  },
},

}
</script>