import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import "bootstrap/dist/css/bootstrap.css"
import "bootstrap-icons/font/bootstrap-icons.css"

const app = createApp(App)

app.use(createPinia())
app.use(router)

// Ensure Bootstrap JS is loaded before mounting the app so global bootstrap
// event handlers (dropdowns, collapse, etc.) are available to components.
import 'bootstrap/dist/js/bootstrap.js'

app.mount('#app')
