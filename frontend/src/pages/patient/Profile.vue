<template>
    <div class="container mt-5 mb-5">
        <!-- Header -->
        <div class="row mb-5">
            <div class="col-12">
                <h1 class="display-6 fw-bold text-primary mb-2">My Profile</h1>
                <p class="text-muted">Manage your personal and medical information</p>
            </div>
        </div>

        <!-- Error Alert -->
        <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
            {{ error }}
            <button type="button" class="btn-close" @click="error = ''"></button>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-3 text-muted">Loading your profile...</p>
        </div>

        <!-- Profile Content -->
        <div v-else-if="profile" class="row g-4">
            <!-- Personal Information Card -->
            <div class="col-md-6">
                <div class="card shadow-sm h-100">
                    <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
                        <h5 class="mb-0"><i class="bi bi-person-fill"></i> Personal Information</h5>
                        <button 
                            v-if="!isEditingPersonal"
                            class="btn btn-sm btn-light"
                            @click="isEditingPersonal = true"
                        >
                            <i class="bi bi-pencil"></i> Edit
                        </button>
                    </div>
                    <div class="card-body">
                        <div v-if="!isEditingPersonal">
                            <div class="mb-3">
                                <label class="text-muted small">Full Name</label>
                                <p class="fs-6 fw-semibold">{{ profile.fullname }}</p>
                            </div>
                            <div class="mb-3">
                                <label class="text-muted small">Username</label>
                                <p class="fs-6">{{ profile.username }}</p>
                            </div>
                            <div class="mb-3">
                                <label class="text-muted small">Email</label>
                                <p class="fs-6"><i class="bi bi-envelope"></i> {{ profile.email }}</p>
                            </div>
                            <div class="mb-3">
                                <label class="text-muted small">Phone</label>
                                <p class="fs-6"><i class="bi bi-telephone"></i> {{ profile.phone }}</p>
                            </div>
                            <div class="row">
                                <div class="col-6">
                                    <label class="text-muted small">Gender</label>
                                    <p class="fs-6">{{ profile.gender || '—' }}</p>
                                </div>
                                <div class="col-6">
                                    <label class="text-muted small">Age</label>
                                    <p class="fs-6">{{ profile.age || '—' }} years</p>
                                </div>
                            </div>
                        </div>
                        <div v-else class="form-content">
                            <div class="mb-3">
                                <label class="form-label">Full Name</label>
                                <input v-model="editData.fullname" type="text" class="form-control">
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Email</label>
                                <input v-model="editData.email" type="email" class="form-control">
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Phone</label>
                                <input v-model="editData.phone" type="tel" class="form-control">
                            </div>
                            <div class="row">
                                <div class="col-6">
                                    <div class="mb-3">
                                        <label class="form-label">Gender</label>
                                        <select v-model="editData.gender" class="form-select">
                                            <option value="">Select Gender</option>
                                            <option value="Male">Male</option>
                                            <option value="Female">Female</option>
                                            <option value="Other">Other</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="col-6">
                                    <div class="mb-3">
                                        <label class="form-label">Date of Birth</label>
                                        <input v-model="editData.dob" type="date" class="form-control">
                                    </div>
                                </div>
                            </div>
                            <div class="d-flex gap-2">
                                <button 
                                    class="btn btn-primary btn-sm"
                                    @click="savePersonalInfo"
                                    :disabled="isSaving"
                                >
                                    <i class="bi bi-check"></i> Save
                                </button>
                                <button 
                                    class="btn btn-secondary btn-sm"
                                    @click="cancelEdit('personal')"
                                    :disabled="isSaving"
                                >
                                    <i class="bi bi-x"></i> Cancel
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Medical Information Card -->
            <div class="col-md-6">
                <div class="card shadow-sm h-100">
                    <div class="card-header bg-danger text-white d-flex justify-content-between align-items-center">
                        <h5 class="mb-0"><i class="bi bi-heart-pulse"></i> Medical Information</h5>
                        <button 
                            v-if="!isEditingMedical"
                            class="btn btn-sm btn-light"
                            @click="isEditingMedical = true"
                        >
                            <i class="bi bi-pencil"></i> Edit
                        </button>
                    </div>
                    <div class="card-body">
                        <div v-if="!isEditingMedical">
                            <div class="mb-3">
                                <label class="text-muted small">Blood Group</label>
                                <p class="fs-6 fw-semibold">
                                    <span v-if="profile.blood_group" class="badge bg-danger">{{ profile.blood_group }}</span>
                                    <span v-else class="text-muted">Not specified</span>
                                </p>
                            </div>
                            <div class="mb-3">
                                <label class="text-muted small">Date of Birth</label>
                                <p class="fs-6">{{ formatDate(profile.dob) }}</p>
                            </div>
                            <div class="mb-3">
                                <label class="text-muted small">Emergency Contact</label>
                                <p class="fs-6">
                                    <i class="bi bi-telephone-plus"></i>
                                    {{ profile.emergency_contact || '—' }}
                                </p>
                            </div>
                            <div class="mb-3">
                                <label class="text-muted small">Medical History</label>
                                <p class="fs-6 text-break">{{ profile.medical_history || 'No medical history recorded' }}</p>
                            </div>
                        </div>
                        <div v-else class="form-content">
                            <div class="mb-3">
                                <label class="form-label">Blood Group</label>
                                <select v-model="editData.blood_group" class="form-select">
                                    <option value="">Select Blood Group</option>
                                    <option value="A+">A+</option>
                                    <option value="A-">A-</option>
                                    <option value="B+">B+</option>
                                    <option value="B-">B-</option>
                                    <option value="O+">O+</option>
                                    <option value="O-">O-</option>
                                    <option value="AB+">AB+</option>
                                    <option value="AB-">AB-</option>
                                </select>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Emergency Contact</label>
                                <input v-model="editData.emergency_contact" type="tel" class="form-control" placeholder="Phone number">
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Medical History</label>
                                <textarea 
                                    v-model="editData.medical_history" 
                                    class="form-control" 
                                    rows="3"
                                    placeholder="List any chronic conditions, allergies, past surgeries, etc."
                                ></textarea>
                            </div>
                            <div class="d-flex gap-2">
                                <button 
                                    class="btn btn-primary btn-sm"
                                    @click="saveMedicalInfo"
                                    :disabled="isSaving"
                                >
                                    <i class="bi bi-check"></i> Save
                                </button>
                                <button 
                                    class="btn btn-secondary btn-sm"
                                    @click="cancelEdit('medical')"
                                    :disabled="isSaving"
                                >
                                    <i class="bi bi-x"></i> Cancel
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import api from '@/utils/api';
import useUserStore from '@/stores/user';

export default {
    name: 'ProfilePage',
    data() {
        return {
            error: "",
            successMessage: "",
            profile: null,
            userStore: null,
            isEditingPersonal: false,
            isEditingMedical: false,
            isSaving: false,
            loading: true,
            editData: {}
        };
    },
    computed: {
        profileCompletion() {
            if (!this.profile) return 0;
            const fields = ['fullname', 'email', 'phone', 'gender', 'dob', 'blood_group', 'emergency_contact', 'medical_history'];
            const completed = fields.filter(field => this.profile[field] && this.profile[field].toString().trim() !== '').length;
            return Math.round((completed / fields.length) * 100);
        },
        completedFields() {
            if (!this.profile) return 0;
            const fields = ['fullname', 'email', 'phone', 'gender', 'dob', 'blood_group', 'emergency_contact', 'medical_history'];
            return fields.filter(field => this.profile[field] && this.profile[field].toString().trim() !== '').length;
        },
        totalFields() {
            return ['fullname', 'email', 'phone', 'gender', 'dob', 'blood_group', 'emergency_contact', 'medical_history'].length;
        },
        missingFields() {
            if (!this.profile) return [];
            const fields = {
                'fullname': 'Full Name',
                'email': 'Email',
                'phone': 'Phone',
                'gender': 'Gender',
                'dob': 'Date of Birth',
                'blood_group': 'Blood Group',
                'emergency_contact': 'Emergency Contact',
                'medical_history': 'Medical History'
            };
            return Object.keys(fields)
                .filter(field => !this.profile[field] || this.profile[field].toString().trim() === '')
                .map(field => fields[field]);
        }
    },
    created() {
        this.userStore = useUserStore();
        this.fetchProfile();
    },
    methods: {
        async fetchProfile() {
            try {
                this.loading = true;
                if (!this.userStore.user || !this.userStore.user.id) {
                    this.error = "User not logged in.";
                    this.loading = false;
                    return;
                }
                const response = await api.get(`/user/${this.userStore.user.id}`);
                console.log(response);
                
                this.profile = Array.isArray(response) ? response[0] : response;
                this.initializeEditData();
            } catch (err) {
                this.error = err.message || "An error occurred while fetching profile.";
                console.error("Profile fetch error:", err);
            } finally {
                this.loading = false;
            }
        },
        initializeEditData() {
            this.editData = {
                fullname: this.profile.fullname,
                email: this.profile.email,
                phone: this.profile.phone,
                gender: this.profile.gender || '',
                dob: this.profile.dob || '',
                blood_group: this.profile.blood_group || '',
                emergency_contact: this.profile.emergency_contact || '',
                medical_history: this.profile.medical_history || ''
            };
        },
        async savePersonalInfo() {
            try {
                this.isSaving = true;
                const payload = {
                    fullname: this.editData.fullname,
                    email: this.editData.email,
                    phone: this.editData.phone,
                    gender: this.editData.gender,
                    dob: this.editData.dob
                };
                await api.patch(`/user/${this.userStore.user.id}`, payload);
                this.profile = { ...this.profile, ...payload };
                this.isEditingPersonal = false;
                this.successMessage = "Personal information updated successfully!";
                setTimeout(() => this.successMessage = '', 3000);
            } catch (err) {
                this.error = err.message || "Failed to save personal information.";
            } finally {
                this.isSaving = false;
            }
        },
        async saveMedicalInfo() {
            try {
                this.isSaving = true;
                const payload = {
                    blood_group: this.editData.blood_group,
                    emergency_contact: this.editData.emergency_contact,
                    medical_history: this.editData.medical_history
                };
                await api.patch(`/user/${this.userStore.user.id}`, payload);
                this.profile = { ...this.profile, ...payload };
                this.isEditingMedical = false;
                this.successMessage = "Medical information updated successfully!";
                setTimeout(() => this.successMessage = '', 3000);
            } catch (err) {
                this.error = err.message || "Failed to save medical information.";
            } finally {
                this.isSaving = false;
            }
        },
        cancelEdit(section) {
            if (section === 'personal') {
                this.isEditingPersonal = false;
            } else {
                this.isEditingMedical = false;
            }
            this.initializeEditData();
        },
        formatDate(dateStr) {
            if (!dateStr) return '—';
            try {
                return new Date(dateStr).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                });
            } catch (e) {
                return dateStr;
            }
        }
    }
}
</script>

<style scoped>
.card {
    border: none;
    border-radius: 0.5rem;
    transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
}

.card-header {
    border-radius: 0.5rem 0.5rem 0 0;
    font-weight: 600;
}

.badge {
    padding: 0.5rem 0.75rem;
    font-size: 0.875rem;
}

.form-label {
    color: #333;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.text-muted.small {
    font-size: 0.813rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.bi {
    margin-right: 0.5rem;
}

h1 {
    color: #0d6efd;
}

.progress {
    background-color: #e9ecef;
}

.font-monospace {
    font-family: 'Courier New', monospace;
    font-size: 0.875rem;
}

.form-content {
    animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}
</style>