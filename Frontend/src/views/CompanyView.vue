<template>
<div>
  <div v-if="!isLoggedIn">
      <CompanyLogin v-if="!showRegister" @logged-in="handlelogin" @register-here="showRegister =true"/>
      <CompanyRegister v-else  @registered="handleRegistration" @login-here="showRegister =false"/>
  </div>

<div v-else>
    <CompanyDashboard  />
</div>


</div>

</template>

<script>
import CompanyDashboard from '@/components/CompanyDashboard.vue';
import CompanyLogin from '../components/CompanyLogin.vue'
import CompanyRegister from '../components/CompanyRegister.vue'

export default {
  name: 'CompanyView',
  components: {
    CompanyLogin,
    CompanyDashboard,
    CompanyRegister
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