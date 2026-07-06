<template>
<div>
  <div v-if="!isLoggedIn">
      <studentlogin v-if="!showRegister" @logged-in="handlelogin" @register-here="showRegister =true"/>
      <StudentRegister v-else  @registered="handleRegistration" @login-here="showRegister =false"/>
  </div>

<div v-else>
    <StudentDashboard  />
</div>


</div>

</template>

<script>
import StudentDashboard from '@/components/StudentDashboard.vue';
import studentlogin from '../components/studentlogin.vue'
import StudentRegister from '../components/StudentRegister.vue'

export default {
  name: 'StudentView',
  components: {
    studentlogin,
    StudentDashboard,
    StudentRegister
  },
  data () {
    return {
      isLoggedIn: false,
      showRegister: true
    }
  },
  methods: {
    handleRegistration() {
      this.showRegister = false;
      this.isLoggedIn = false;
    },
    handlelogin() {
      this.isLoggedIn = true;
    }
  }
}
</script>