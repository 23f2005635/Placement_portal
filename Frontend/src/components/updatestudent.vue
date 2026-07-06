<template>
  <form @submit.prevent="updatestudent">
    <div class="form-group">
      <label for="name">Student name</label>
      <input type="text" class="form-control" id="name" placeholder="Enter Student name" v-model="form.student_name">
    </div>
    <div class="form-group">
      <label for="branch">Branch</label>
      <input type="text" class="form-control" id="branch" placeholder="Enter branch" v-model="form.branch">
    </div>
    <div class="form-group">
      <label for="education">Education</label>
      <input type="text" class="form-control" id="education" placeholder="Enter highest educatio" v-model="form.education">
    </div>
    <div class="form-group">
      <label for="cgpa">CGPA</label>
      <input type="text" class="form-control" id="cgpa" placeholder="Enter cgpa" v-model="form.cgpa">
    </div>
    <div class="form-group">
      <label for="year">Passing Year</label>
      <input type="text" class="form-control" id="year" placeholder="Enter Passing year" v-model="form.year">
    </div>
    <div class="form-group">
      <label for="skills">Skills seperated by space</label>
      <input type="text" class="form-control" id="skills" placeholder="skills" v-model="form.skills">
    </div>
    <!-- <div class="form-group">
      <label for="resume">Resume</label>
      <input type="file" class="form-control" id="resume" placeholder="upload resume">
    </div> -->
    <button type="submit" class="btn btn-primary">Submit</button>
  </form>
</template>
<script>
import axios from 'axios'
export default{
  data(){
    return {
      form : {
        student_name:'',
        branch:'',
        education:'',
        cgpa:0.0,
        year:'',
        skills:''
        // resume:''


      }
    }
  },
  methods:{
    async updatestudent (){
      try {
        console.log(this.form);
        console.log(localStorage.getItem("token"));

        const token = localStorage.getItem('token');
        const response = await axios.post('http://localhost:5000/api/updatestudent',this.form ,{
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        alert('student details updated');
        this.form ={
          student_name:'',
          branch:'',
          education:'',
          cgpa:0.0,
          year:'',
          skills:'',
          // resume:''
        }
        this.$emit('change-tab')
        console.log('Placement drive created:', response.data);
      } catch (error) {
        console.error('Error updating student', error);
        //  console.log(error.response.status);
        // console.log(error.response.data);
      }
    }
  }
}

</script>