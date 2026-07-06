<template>
  <form @submit.prevent="handle_placement_drive">
    <div class="form-group">
      <label for="jobTitle">Job Title</label>
      <input type="text" class="form-control" id="jobTitle" placeholder="Enter job title" v-model="form.jobTitle">
    </div>
    <div class="form-group">
      <label for="jobDescription">Job Description</label>
      <textarea class="form-control" id="jobDescription" rows="3" placeholder="Enter job description" v-model="form.jobDescription"></textarea>
    </div>
    <div class="form-group">
      <label for="work_Location">Work Location</label>
      <input type="text" class="form-control" id="work_Location" placeholder="Enter work location" v-model="form.workLocation">
    </div>
    <div class="form-group">
      <label for="eligibility_cgpa">Eligibility (CGPA)</label>
      <input type="text" class="form-control" id="eligibility_cgpa" placeholder="Enter minimum CGPA" v-model="form.eligibilityCgpa">
    </div>
    <div class="form-group">
      <label for="application_deadline">Application Deadline</label>
      <input type="date" class="form-control" id="application_deadline" v-model="form.applicationDeadline">
    </div>
    <button type="submit" class="btn btn-primary">Submit</button>
  </form>
</template>
<script>
import axios from 'axios'
export default {
  data() {
    return {
      form: {
        jobTitle: '',
        jobDescription: '',
        workLocation: '',
        eligibilityCgpa: '',
        applicationDeadline: ''
      }
    }
  },
  methods: {
    async handle_placement_drive() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.post('http://localhost:5000/api/create_placement_drive', this.form, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        alert('Placement drive created successfully!');
        this.form={
          jobTitle: '',
          jobDescription: '',
          workLocation: '',
          eligibilityCgpa: '',
          applicationDeadline: ''
        }
        this.$emit('change-tab')
        console.log('Placement drive created:', response.data);
      } catch (error) {
        console.error('Error creating placement drive:', error);
        // console.log(error.response.status);
        console.log(error.response.data);
      }
    }
  }
  
}
</script>