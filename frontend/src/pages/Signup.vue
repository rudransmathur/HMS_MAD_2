<template>
    <div class="d-flex justify-content-center align-items-start" style="min-height:auto; padding: 2rem 0;">
        <div class="card p-3 shadow" style="width:720px;">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h4 class="card-title mb-0">Create Account</h4>
                <small class="text-muted">Register as Patient or Doctor</small>
            </div>

            <div class="col-12 text-end mb-3">
                <small class="text-muted">
                    Already have an account? 
                    <router-link to="/login">Sign in</router-link>
                </small>
            </div>

            <div class="card p-3 shadow-sm">
                <ul class="nav nav-pills nav-justified mb-3">
                    <li class="nav-item">
                        <button :class="['nav-link', role==='patient' ? 'active' : '']" @click="role='patient'">Patient</button>
                    </li>
                    <li class="nav-item ms-2">
                        <button :class="['nav-link', role==='doctor' ? 'active' : '']" @click="role='doctor'">Doctor</button>
                    </li>
                </ul>

                <!-- Patient Form -->
                <form v-if="role==='patient'" @submit.prevent="onSubmitPatient" novalidate>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Username <span class="text-danger">*</span></label>
                            <input v-model="patient.username" class="form-control" required />
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Full Name <span class="text-danger">*</span></label>
                            <input v-model="patient.fullname" class="form-control" required />
                        </div>

                        <div class="col-md-6 mb-3">
                            <label class="form-label">Email <span class="text-danger">*</span></label>
                            <input v-model="patient.email" type="email" class="form-control" required />
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Phone <span class="text-danger">*</span></label>
                            <input v-model="patient.phone" type="tel" class="form-control" required />
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Date of Birth <span class="text-danger">*</span></label>
                            <input v-model="patient.dob" type="date" class="form-control" required />
                        </div>

                        <div class="col-md-6 mb-3">
                            <label class="form-label">Gender <span class="text-danger">*</span></label>
                            <select v-model="patient.gender" class="form-select" required>
                                <option value="">-- Select --</option>
                                <option>Male</option>
                                <option>Female</option>
                                <option>Other</option>
                            </select>
                        </div>

                        <div class="col-md-6 mb-3">
                            <label class="form-label">Emergency Contact <span class="text-danger">*</span></label>
                            <input v-model="patient.emergency_contact" type="tel" class="form-control" required />
                        </div>
                    </div>

                    <hr />
                    <div class="mb-3">
                        <label class="form-label">Blood Group (optional)</label>
                        <select v-model="patient.blood_group" class="form-select">
                            <option value="">-- Select --</option>
                            <option>O+</option>
                            <option>O-</option>
                            <option>A+</option>
                            <option>A-</option>
                            <option>B+</option>
                            <option>B-</option>
                            <option>AB+</option>
                            <option>AB-</option>
                        </select>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Medical History (optional)</label>
                        <textarea v-model="patient.medical_history" class="form-control" rows="3"></textarea>
                    </div>

                    <hr />
                    <div class="col-md-6 mb-3">
                        <label class="form-label">Password <span class="text-danger">*</span></label>
                        <input v-model="patient.password" type="password" class="form-control" required />
                    </div>

                    <div class="col-md-6 mb-3">
                        <label class="form-label">Confirm Password <span class="text-danger">*</span></label>
                        <input v-model="patient.confirm_password" type="password" class="form-control" required />
                    </div>

                    <div class="d-flex justify-content-end mt-2">
                        <button :disabled="loading" type="submit" class="btn btn-primary">
                            <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                            {{ loading ? 'Signing up...' : 'Sign Up as Patient' }}
                        </button>
                    </div>
                    <div v-if="error" class="alert alert-danger py-2" role="alert">{{ error }}</div>
                </form>

                <!-- doctor Form -->
                <form v-if="role==='doctor'" @submit.prevent="onSubmitDoctor" novalidate>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Username <span class="text-danger">*</span></label>
                            <input v-model="doctor.username" class="form-control" required />
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Full Name <span class="text-danger">*</span></label>
                            <input v-model="doctor.fullname" class="form-control" required />
                        </div>

                        <div class="col-md-6 mb-3">
                            <label class="form-label">Phone <span class="text-danger">*</span></label>
                            <input v-model="doctor.phone" type="tel" class="form-control" required />
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Email <span class="text-danger">*</span></label>
                            <input v-model="doctor.email" type="email" class="form-control" required />
                        </div>

                        <div class="col-md-6 mb-3">
                            <label class="form-label">Department Name <span class="text-danger">*</span></label>
                            <input v-model="doctor.department_name" class="form-control" required />
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Qualification <span class="text-danger">*</span></label>
                            <input v-model="doctor.qualification" class="form-control" required />
                        </div>

                        <div class="col-md-6 mb-3">
                            <label class="form-label">Experience (years) <span class="text-danger">*</span></label>
                            <input v-model.number="doctor.experience_years" type="number" min="0" class="form-control" required />
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Specialization <span class="text-danger">*</span></label>
                            <input v-model="doctor.specialization" class="form-control" required />
                        </div>

                        <div class="col-md-6 mb-3">
                            <label class="form-label">Consultation Fee (₹) <span class="text-danger">*</span></label>
                            <input v-model.number="doctor.consultation_fee" type="number" min="0" class="form-control" required />
                        </div>
                    </div>

                    <hr />
                    <div class="col-md-6 mb-3">
                        <label class="form-label">Password <span class="text-danger">*</span></label>
                        <input v-model="doctor.password" type="password" class="form-control" required />
                    </div>

                    <div class="col-md-6 mb-3">
                        <label class="form-label">Confirm Password <span class="text-danger">*</span></label>
                        <input v-model="doctor.confirm_password" type="password" class="form-control" required />
                    </div>

                    <div class="d-flex justify-content-end mt-3">
                        <button :disabled="loading" type="submit" class="btn btn-success">
                            <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                            {{ loading ? 'Registering...' : 'Sign Up as Doctor' }}
                        </button>
                    </div>
                    <div v-if="error" class="alert alert-danger py-2 my-2" role="alert">{{ error }}</div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import { useUserStore } from '@/stores/user';
import api from '@/utils/api';

export default {
    name: "SignupPage",
    data() {
        return {
            role: '',
            loading: false,
            error: '',
            patient: {
                role: 'Patient',
                username: '',
                fullname: '',
                email: '',
                phone: '',
                password: '',
                confirm_password: '',
                dob: '',
                gender: '',
                emergency_contact: '',
                blood_group: '',
                medical_history: ''
            },
            doctor: {
                role: 'Doctor',
                username: '',
                fullname: '',
                phone: '',
                email: '',
                password: '',
                confirm_password: '',
                department_name: '',
                qualification: '',
                experience_years: 0,
                specialization: '',
                consultation_fee: 0
            },
            userStore: null
        };
    },
    created() {
        this.userStore = useUserStore();
    },
    methods: {
        async onSubmitPatient() {
            this.error = '';
            if (this.patient.password !== this.patient.confirm_password) {
                this.error = 'Passwords do not match.';
                return;
            }
            this.loading = true;
            try{
                const payload = { ...this.patient };

                const res = await api.post('/auth/register', payload);
                if (res && res.id){
                    this.$router.push('/login');
                }
                else{
                    console.error("Signup error: ", res.message);
                    this.error = res.message || "An error occurred during sign up.";
                }
            }catch(err){
                this.error = err.message || "An error occurred during login.";
                console.error("Signup error:", err);
            }
            finally{
                this.loading = false;
            }
        },

        async onSubmitDoctor() {
            this.error = '';
            if (this.doctor.password !== this.doctor.confirm_password) {
                this.error = 'Passwords do not match.';
                return;
            }
            this.loading = true;
            try{
                const payload = { ...this.doctor };

                const res = await api.post('/auth/register', payload);
                if (res && res.id)
                this.$router.push('/login');
                else{
                    console.error("Login error: ", res.message);
                    this.error = res.message || "An error occurred during sign up.";
                }
            }catch(err){
                this.error = err.message || "An error occurred during sign up.";
                console.error("Login error:", err);
            }
            finally{
                this.loading = false;
            }
        }
    }
}

</script>

<style scoped>
.card{ border-radius:10px; }
</style>