import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {path: '/', component: () => import('@/pages/HomePage.vue')},
    {path: '/login', component: () => import('@/pages/LoginPage.vue')},
    {path: '/signup', component: () => import('@/pages/Signup.vue')},
    {path: '/patientappointments', component: () => import('@/pages/patient/PatientDashboard.vue')},
    {path: '/patienttreatments', component: () => import('@/pages/patient/PatientDiagnosis.vue')},
    {path: '/patientsearch', component: () => import('@/pages/patient/PatientSearch.vue')},
    {path: '/patientprofile', component: () => import('@/pages/patient/PatientProfile.vue')},
    {path: '/doctorappointments', component: () => import('@/pages/doctor/DoctorDashboard.vue')},
    {path: '/doctortreatments', component: () => import('@/pages/doctor/DoctorDiagnosis.vue')},
    {path: '/doctorprofile', component: () => import('@/pages/doctor/DoctorProfile.vue')},
    {path: '/admindoctors', component: () => import('@/pages/admin/AdminDashboard.vue')},
    {path: '/adminappointments', component: () => import('@/pages/admin/AdminAppointments.vue')},
    {path: '/adminsearch', component: () => import('@/pages/admin/AdminSearch.vue')}
  ]
})

export default router