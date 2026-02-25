<template>
    <div>
        <!-- Hero -->
        <section class="py-5 text-white" style="background: linear-gradient(135deg,#007bff 0%,#6610f2 100%);">
            <div class="container text-center py-5">
                <!-- Welcome Section -->
                <div v-if ="!isAuthenticated">
                    <h1 class="display-4 fw-bold">Hospital Management — Simple. Secure. Fast.</h1>
                    <p class="lead mb-4">Book appointments, manage your records, and coordinate care — all from a single, easy-to-use dashboard designed for clinics and hospitals.</p>
                    <router-link to="/signup" class="btn btn-light btn-lg me-2">Sign up</router-link>
                    <router-link to="/login" class="btn btn-outline-light btn-lg">Sign in</router-link>
                </div>
                <div v-if="isAdmin">
                    <div class="mb-5">
                        <h1 class="display-6 fw-bold">Welcome Admin</h1>
                    </div>
                    <p class="lead mb-4"> Manage Doctor and patients records, Manage appointments and coordinate care quickly</p>
                    <router-link to="/" class="btn btn-outline-light btn-lg me-2">##</router-link>
                    <router-link to="/" class="btn btn-outline-light btn-lg">#####</router-link>
                    <router-link to="/" class="btn btn-outline-light btn-lg ms-2">###</router-link>
                </div>
                <div v-if="isPatient">
                    <div class="mb-5">
                        <h1 class="display-6 fw-bold">Welcome, {{ userStore.user?.fullname || 'Patient' }}!</h1>
                    </div>
                    <p class="lead mb-4">Organize appointments, manage patient diagnoses, and schedule your availability for the next week in one place.</p>
                    <router-link to="/patientappointments" class="btn btn-outline-light btn-lg me-2">View Appointments</router-link>
                    <router-link to="/patienttreatments" class="btn btn-outline-light btn-lg">View Diagnosis Reports</router-link>
                    <router-link to="/patientsearch" class="btn btn-outline-light btn-lg ms-2">Search Doctors</router-link>
                </div>
                <div v-if="isDoctor">
                    <div class="mb-5">
                        <h1 class="display-6 fw-bold">Welcome, {{ userStore.user?.fullname || 'Doctor' }}!</h1>
                    </div>
                    <p class="lead mb-4">Book appointments, view your diagnosis and treatment records, and search for doctors easily.</p>
                    <router-link to="/doctorappointments" class="btn btn-outline-light btn-lg me-2">Appointments</router-link>
                    <router-link to="/doctortreatments" class="btn btn-outline-light btn-lg">Diagnosis Reports</router-link>
                    <router-link to="/doctoravailabilities" class="btn btn-outline-light btn-lg me-2 ms-2">Add/Edit Availabilities</router-link>
                </div>
            </div>
        </section>

        <!-- Features cards -->
        <section class="py-5 bg-white">
            <div v-if="!isAuthenticated" class="container"> 
                <div class="row mb-4">
                    <div class="col text-center">
                        <h2 class="fw-bold">What you can do with HMS</h2>
                        <p class="text-muted">Useful features designed for patients, doctors and administrators.</p>
                    </div>
                </div>

                <div class="row g-4">
                    <div class="col-md-4">
                        <div class="card h-100 shadow-sm">
                            <div class="card-body">
                                <div class="mb-3 display-6 text-primary"><i class="bi bi-calendar-check"></i></div>
                                <h5 class="card-title">Online Appointments</h5>
                                <p class="card-text">Find available time slots, book appointments and get confirmations — no phone calls needed.</p>
                            </div>
                        </div>
                    </div>

                    <div class="col-md-4">
                        <div class="card h-100 shadow-sm">
                            <div class="card-body">
                                <div class="mb-3 display-6 text-primary"><i class="bi bi-file-medical"></i></div>
                                <h5 class="card-title">Electronic Health Records</h5>
                                <p class="card-text">Store and access patient histories, prescriptions and treatment notes securely in one place.</p>
                            </div>
                        </div>
                    </div>

                    <div class="col-md-4">
                        <div class="card h-100 shadow-sm">
                            <div class="card-body">
                                <div class="mb-3 display-6 text-primary"><i class="bi bi-people-fill"></i></div>
                                <h5 class="card-title">Staff & Role Management</h5>
                                <p class="card-text">Role-based access for admins, doctors and patients keeps workflows secure and compliant.</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Secondary features -->
                <div class="row mt-5">
                    <div class="col-md-6">
                        <div class="p-4 border rounded bg-light h-100">
                            <h4>Why choose our system?</h4>
                            <ul>
                                <li>Simple interface built for busy clinics</li>
                                <li>Secure authentication using Flask-Security</li>
                                <li>Small-footprint SQLite option for local deployments</li>
                            </ul>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="p-4 border rounded h-100">
                            <h4>How it works</h4>
                            <ol>
                                <li>Patients sign up and book appointments</li>
                                <li>Doctors manage availability and consult</li>
                                <li>Admins review requests and manage users</li>
                            </ol>
                        </div>
                    </div>
                </div>

                <!-- User capabilities (requested) -->
                <div class="row mt-5">
                    <div class="col-12">
                        <div class="p-4 border rounded h-100 bg-white shadow-sm">
                            <h4 class="fw-bold">What patients can do</h4>
                            <p class="text-muted">Key capabilities available to users of this Hospital Management System:</p>
                            <ul class="list-unstyled ms-3">
                                <li class="mb-2"><span class="fw-bold">1.</span> Can <strong>register, log in, and update</strong> their profile.</li>
                                <li class="mb-2"><span class="fw-bold">2.</span> Can <strong>search for doctors</strong> by specialization and availability.</li>
                                <li class="mb-2"><span class="fw-bold">3.</span> Can <strong>book, reschedule, or cancel</strong> an appointment.</li>
                                <li class="mb-2"><span class="fw-bold">4.</span> Can <strong>view their own appointment history</strong> and treatment details.</li>
                            </ul>
                            <div class="mt-3">
                                <router-link to="/signup" class="btn btn-primary me-2">Sign up</router-link>
                                <router-link to="/appointments" class="btn btn-outline-primary">Sed scheduling conflicts, and track patient history. This Hospital Management System aims to provide a centralized, secure, and user-friendly solution to reduce administrative overhead and improve patient care.</router-link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Footer CTA -->
        <section v-if="!isAuthenticated" class="py-4 bg-primary text-white">
            <div class="container d-flex justify-content-between align-items-center">
                <div>
                    <strong>Ready to manage care more efficiently?</strong>
                    <div class="text-white-50">Start with a free signup and explore the dashboard.</div>
                </div>
                <div>
                    <router-link to="/signup" class="btn btn-light">Get started</router-link>
                </div>
            </div>
        </section>
    </div>
</template>

<script>
    import useUserStore from '@/stores/user';
    export default {
        name: 'HomePage',
        data() {
            return {
                userStore: null
            };
        },
        created(){
            this.userStore = useUserStore();
        },
        computed:{
            isAuthenticated(){
                return this.userStore && this.userStore.isAuthenticated;
            },
            isAdmin(){
                return this.userStore && this.userStore.isAdmin;
            },
            isPatient(){
                return this.userStore && this.userStore.isPatient;
            },
            isDoctor(){
                return this.userStore && this.userStore.isDoctor;
            },
            displayName(){
                return this.userStore?.user?.name || 'Account';
            }
        }
    };
</script>

<style scoped>
/* Keep styling minimal; Bootstrap takes care of most layout */
.card img { object-fit: cover; height: 140px; }
</style>