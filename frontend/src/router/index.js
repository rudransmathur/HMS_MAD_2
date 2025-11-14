import { createRouter, createWebHistory } from 'vue-router'

import HomePage from '@/pages/HomePage.Vue'
import LoginPage from '@/pages/LoginPage.vue'
import Signup from '@/pages/Signup.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {path: '/', component: HomePage},
    {path: '/login', component: LoginPage},
    {path: '/signup', component: Signup}
  ],
})

export default router
