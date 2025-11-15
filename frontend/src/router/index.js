import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {path: '/', component: () => import('@/pages/HomePage.vue')},
    {path: '/login', component: () => import('@/pages/LoginPage.vue')},
    {path: '/signup', component: () => import('@/pages/Signup.vue')},
    {path: '/patientappointments', component: () => import('@/pages/patient/Dashboard.vue')}
  ],
})

export default router
