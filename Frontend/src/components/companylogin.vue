<template>
  <div>
    <h1>Company Login</h1>
    <form @submit.prevent="handleLogin">
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" v-model="form.username" required>
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" v-model="form.password" required>
      </div>
      <button type="submit">Login</button>
    </form>
    <a href="#" @click.prevent="$emit('register-here')">register here</a>

  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'companylogin',
  data () {
    return {
      form: {
        username: '',
        password: '',
        role: 'company'
      }
    }
  },
  methods: {
    async handleLogin () {
      try {
        const response = await axios.post('http://localhost:5000/api/login', this.form)
        console.log('Login response:', response.data)
        localStorage.setItem('token', response.data.data.access_token)
        localStorage.setItem('role', this.form.role)
        this.$emit('logged-in')
      } catch (error) {
        console.error('Login error:', error)
      }
    }
  }
}
</script>