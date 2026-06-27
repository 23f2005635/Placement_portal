<template>

</template>


<script>
  import axios from 'axios';
  export default {
    name: 'UserRegister',
    data() {
      return {
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
        errorMessage: ''
      };
    },
    methods: {
      async registerUser() {
        if (this.password !== this.confirmPassword) {
          this.errorMessage = 'Passwords do not match.';
          return;
        }
  
        try {
          const response = await axios.post('http://localhost:3000/api/register', {
            username: this.username,
            email: this.email,
            password: this.password
          });
  
          // Handle successful registration (e.g., redirect to login page)
          console.log('Registration successful:', response.data);
          this.$router.push('/login');
        } catch (error) {
          // Handle registration error
          console.error('Registration error:', error.response.data);
          this.errorMessage = error.response.data.message || 'Registration failed.';
        }
      }
    }
  };
</script>