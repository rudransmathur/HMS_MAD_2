<template>
    <footer class="bg-dark text-white py-5 mt-5">
        <div class="container">
            <div class="row">
                <!-- Links Section -->
                <div class="col-md-6">
                    <h6 class="fw-bold mb-3" color="white">Quick Links</h6>
                    <ul class="list-unstyled">
                        <li class="mb-2">
                            <router-link to="/" class="footer-link">Home</router-link>
                        </li>
                        <li class="mb-2">
                            <router-link to="/about" class="footer-link">About Us</router-link>
                        </li>
                        <li class="mb-2">
                            <router-link to="/privacy" class="footer-link">Privacy Policy</router-link>
                        </li>
                        <li class="mb-2">
                            <router-link to="/contact" class="footer-link">Contact</router-link>
                        </li>
                    </ul>
                </div>

                <!-- Copyright Section -->
                <div class="col-md-6">
                    <h6 class="fw-bold text-light mb-3">About</h6>
                    <p class="small">Hospital Management System — Streamline operations, improve patient care.</p>
                </div>
            </div>

            <hr class="bg-secondary">

            <!-- Copyright Footer -->
            <div class="row">
                <div class="col-12 text-center">
                    <p class="small text-light mb-0">
                        &copy; {{ year }} Hospital Management — Built by Rudransh Mathur
                    </p>
                </div>
            </div>
        </div>
    </footer>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const year = ref(new Date().getFullYear());
</script>

<style scoped>
.footer-link {
    color: #adb5bd;
    text-decoration: none;
    transition: color 0.3s ease;
}

.footer-link:hover {
    color: #ffffff;
    text-decoration: underline;
}

footer {
    margin-top: auto;
}
</style>