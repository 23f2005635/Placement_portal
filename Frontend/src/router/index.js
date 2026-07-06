import { createRouter, createWebHistory } from 'vue-router'
import LandingView from '../views/LandingView.vue'
import AdminView from '../views/AdminView.vue' 
import CompanyView from '../views/CompanyView.vue'
import StudentView from '../views/StudentView.vue'

const routes = [
  { path: '/', component: LandingView },
  { path: '/admin', component: AdminView }, 
  { path: '/company', component: CompanyView },
  { path: '/student', component: StudentView },
  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router