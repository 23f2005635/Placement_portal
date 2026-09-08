<template>
<div>
    <h1>Company Registration</h1>
    <form @submit.prevent="handleRegister">
        <div>
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" v-model="form.username" required>
        </div>
        <div>
            <label for="company_name">Company Name:</label>
            <input type="text" id="company_name" name="company_name" v-model="form.company_name" required>
        </div>
        <div>
            <label for="company_address">Company Address:</label>
            <input type="text" id="company_address" name="company_address" v-model="form.company_address" required>
        </div>
        <div>
            <label for="profile">Profile:</label>
            <textarea id="profile" name="profile" v-model="form.profile" required></textarea>
        </div>
        
        <div>
            <label for="industry">Industry:</label>
            <input type="text" id="industry" name="industry" v-model="form.industry" required>
        </div>
        <div>
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" v-model="form.email" required>
        </div>
        <div>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" v-model="form.password" required>
        </div>
        <div>
            <label for="hr_contact">HR Contact:</label>
            <input type="text" id="hr_contact" name="hr_contact" v-model="form.hr_contact" required>
        </div>
        <div>
            <label for="website">Website:</label>
            <input type="text" id="website" name="website" v-model="form.website">
        </div>
        <!-- <div>
            <label for="role">Select Role:</label>
            <select id="role" name="role" v-model="form.role" required>
                <option value="student">Student</option>
                <option value="company">Company</option>
            </select>
        </div> -->
        <button type="submit">Register</button>

    </form>
    <a href="#" @click.prevent="$emit('login-here')">Already have an account? Login</a>
</div>

</template>

<script>
import axios from 'axios'

export default {
    name: 'CompanyRegister',
    emits:['registered'],

    data() {
        return {
            form : {
                username: '',
                email: '',
                password: '',
                role:'company',
                company_name: '',
                company_address: '',
                profile: '',
                industry: '',
                hr_contact: '',
                website: ''
            }
        }
    },
    methods: {
        async handleRegister() {
            try {
                await axios.post('http://localhost:5000/api/register', this.form)
                this.$emit('registered')
            } catch (error) {
                console.error('Registration failed:', error);

            }
            
        }
    },
}
</script>