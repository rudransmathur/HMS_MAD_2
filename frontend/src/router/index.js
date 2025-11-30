import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {path: '/', component: () => import('@/pages/HomePage.vue')},
    {path: '/login', component: () => import('@/pages/LoginPage.vue')},
    {path: '/signup', component: () => import('@/pages/Signup.vue')},
<<<<<<< HEAD
    {path: '/patientappointments', component: () => import('@/pages/patient/Dashboard.vue')},
    {path: '/patienttreatments', component: () => import('@/pages/patient/Diagnosis.vue')},
    {path: '/patientsearch', component: () => import('@/pages/patient/Search.vue')},
    {path: '/profile', component: () => import('@/pages/patient/Profile.vue')}
=======
    {path: '/patientappointments', component: () => import('@/pages/patient/Dashboard.vue')}
>>>>>>> 41b185b6bed628ebefdf242bf3df96c74a0e7835
  ],
})

export default router
