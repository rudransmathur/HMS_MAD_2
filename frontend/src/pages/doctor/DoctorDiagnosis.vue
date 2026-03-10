<template>
    <div class="container mt-5 mb-5">
        <!-- Header -->
        <div class="row mb-5">
            <div class="col">
                <h1 class="display-6 fw-bold text-primary">Diagnosis & Treatment Reports</h1>
                <p class="text-muted">Manage treatment records for your patients</p>
            </div>
            <div class="col-auto">
                <button class="btn btn-primary btn-lg" @click="showModal = true">
                    <i class="bi bi-plus-circle"></i> New Treatment

                </button>
            </div>
        </div>

        <!-- Error Alert -->
        <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
            {{ error }}
            <button type="button" class="btn-close" @click="error = ''"></button>
        </div>

        <!-- Success Alert -->
        <div v-if="successMessage" class="alert alert-success alert-dismissible fade show" role="alert">
            {{ successMessage }}
            <button type="button" class="btn-close" @click="successMessage = ''"></button>
        </div>
        
        <!-- Search/Filter Section -->
        <div class="card mb-4">
            <div class="card-body">
                <div class="row g-3 align-items-end">
                    <div class="col-md-4">
                        <label class="form-label mb-1">Patient Name</label>
                        <input v-model="search.patient" type="text" class="form-control" placeholder="Search by patient name">
                    </div>
                    <div class="col-md-3">
                        <label class="form-label mb-1">Date</label>
                        <input v-model="search.date" type="date" class="form-control">
                    </div>
                    <div class="col-md-3">
                        <label class="form-label mb-1">Time</label>
                        <input v-model="search.time" type="time" class="form-control">
                    </div>
                    <div class="col-md-2">
                        <button class="btn btn-outline-secondary w-100" @click="clearSearch" type="button">Clear</button>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- No Treatments Message -->
        <div v-if="filteredTreatments.length === 0" class="alert alert-info text-center py-5">
            <i class="bi bi-file-earmark-medical" style="font-size: 3rem; color: #0d6efd;"></i>
            <p class="mt-3 mb-0">No treatment reports found for the selected criteria.</p>
        </div>

        <!-- Treatments List -->
        <div v-else>
            <div v-for="(treatment, index) in filteredTreatments" :key="treatment.t_id || index" class="card shadow-sm mb-4 border-0">
                <div class="card-header bg-light border-bottom d-flex justify-content-between align-items-center">
                    <div>
                        <h5 class="mb-1">
                            <i class="bi bi-capsule"></i> Treatment Report #{{ index + 1 }}
                        </h5>
                        <small class="text-muted">Patient: <strong>{{ treatment.patient_name }}</strong> | {{ formatDate(treatment.created_date) }}</small>
                    </div>
                    <div class="btn-group" role="group">
                        <button type="button" class="btn btn-sm btn-outline-warning me-2" @click="editTreatment(treatment)">
                            <i class="bi bi-pencil"></i> Edit
                        </button>
                        <button type="button" class="btn btn-sm btn-outline-danger" @click="confirmDelete(treatment)" title="Delete Treatment">
                            <i class="bi bi-trash"></i> Delete
                        </button>
                    </div>
                </div>
                <div class="card-body">
                    <!-- Diagnosis -->
                    <div class="mb-4">
                        <h6 class="fw-semibold text-primary mb-2">
                            <i class="bi bi-file-medical"></i> Diagnosis
                        </h6>
                        <div class="p-3 bg-light rounded">
                            <p class="mb-0 text-break">{{ treatment.diagnosis }}</p>
                        </div>
                    </div>

                    <!-- Prescription -->
                    <div class="mb-4">
                        <h6 class="fw-semibold text-primary mb-2">
                            <i class="bi bi-prescription2"></i> Prescription
                        </h6>
                        <div class="p-3 bg-light rounded">
                            <p class="mb-0 text-break">{{ treatment.prescription }}</p>
                        </div>
                    </div>

                    <!-- Notes -->
                    <div>
                        <h6 class="fw-semibold text-primary mb-2">
                            <i class="bi bi-chat-left-text"></i> Notes
                        </h6>
                        <div class="p-3 bg-light rounded">
                            <p class="mb-0 text-break">{{ treatment.notes }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Treatment Modal -->
    <div v-if="showModal" class="modal d-block" tabindex="-1" aria-labelledby="treatmentModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header bg-primary text-white">
                    <h5 class="modal-title" id="treatmentModalLabel">
                        <i class="bi bi-pencil-square"></i>
                        {{ isediting ? 'Edit Treatment' : 'Create New Treatment' }}
                    </h5>
                    <button type="button" class="btn-close btn-close-white" @click="closeModal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="saveform">
                        <!-- Patient Selection (for new treatments) -->
                        <div v-if="!isediting" class="mb-3">
                            <label for = "patient" class="form-label fw-semibold">Select Patient</label>
                            <select v-model="formData.patient_id" id = "patient" class="form-select">
                                <option value="">-- Choose a patient --</option>
                                <option v-for="patient in availablePatients" :key="patient.patient_id" :value="patient.patient_id">
                                    {{ patient.patient_name }} (Appointment {{ patient.ap_id }})
                                </option>
                            </select>
                        </div>

                        <!-- Appointment Selection -->
                        <div v-if="!isediting" class="mb-3">
                            <label for = "appointment" class="form-label fw-semibold">Associated Appointment</label>
                            <input id = "appointment" v-model="formData.appointment_id" type="number" class="form-control" placeholder="Appointment ID">
                        </div>

                        <!-- Diagnosis -->
                        <div class="mb-3">
                            <label class="form-label fw-semibold">Diagnosis</label>
                            <textarea 
                                v-model="formData.diagnosis"
                                class="form-control"
                                rows="3"
                                placeholder="Enter the patient's diagnosis..."
                                required
                            ></textarea>
                        </div>

                        <!-- Prescription -->
                        <div class="mb-3">
                            <label class="form-label fw-semibold">Prescription</label>
                            <textarea 
                                v-model="formData.prescription"
                                class="form-control"
                                rows="3"
                                placeholder="Enter prescribed medications and dosage..."
                                required
                            ></textarea>
                        </div>

                        <!-- Notes -->
                        <div class="mb-3">
                            <label class="form-label fw-semibold">Additional Notes</label>
                            <textarea 
                                v-model="formData.notes"
                                class="form-control"
                                rows="3"
                                placeholder="Any additional notes or recommendations..."
                            ></textarea>
                        </div>
                        <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
                        <button type="submit" class="btn btn-primary" :disabled="isSaving">
                            <span v-if="!isSaving">
                                {{ isediting ? 'Update' : 'Create' }}
                            </span>
                            <span v-else>
                                <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                                Saving...
                            </span>
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import api from '@/utils/api';
import useUserStore from '@/stores/user';

export default {
    name: 'DoctorDiagnosisPage',
    data() {
        return {
            error: "",
            successMessage: "",
            treatments: [],
            availablePatients: [],
            userStore: null,
            showModal: false,
            isediting: false,
            isSaving: false,
            search: {
                patient: '',
                date: '',
                time: ''
            },
            formData: {
                t_id: null,
                patient_id: '',
                appointment_id: '',
                diagnosis: '',
                prescription: '',
                notes: ''
            }
        };
    },
    computed: {
        filteredTreatments() {
            return this.treatments.filter(treatment => {
                const patientMatch = this.search.patient.trim() === '' || (treatment.patient_name && treatment.patient_name.toLowerCase().includes(this.search.patient.trim().toLowerCase()));

                // Date filter (compare only date part)
                let dateMatch = true;
                if (this.search.date) {
                    // treatment.created_date may be ISO string or similar
                    const tDate = treatment.created_date ? new Date(treatment.created_date) : null;
                    const searchDate = new Date(this.search.date);
                    if (tDate) {
                        dateMatch = tDate.getFullYear() === searchDate.getFullYear() &&
                            tDate.getMonth() === searchDate.getMonth() &&
                            tDate.getDate() === searchDate.getDate();
                    } else {
                        dateMatch = false;
                    }
                }

                // Time filter (compare hour:minute)
                let timeMatch = true;
                if (this.search.time) {
                    const tDate = treatment.created_date ? new Date(treatment.created_date) : null;
                    if (tDate) {
                        const tHours = String(tDate.getHours()).padStart(2, '0');
                        const tMinutes = String(tDate.getMinutes()).padStart(2, '0');
                        const searchParts = this.search.time.split(':');
                        timeMatch = tHours === searchParts[0] && tMinutes === searchParts[1];
                    } else {
                        timeMatch = false;
                    }
                }

                return patientMatch && dateMatch && timeMatch;
            });
        }
    },
    created(){
        this.userStore = useUserStore();
        this.fetchTreatments();
        this.fetchAvailablePatients();
    },
    methods: {
        clearSearch() {
            this.search.patient = '';
            this.search.date = '';
            this.search.time = '';
        },
        
        async fetchTreatments() {
            try {
                if (!this.userStore.user || !this.userStore.user.id) {
                    this.error = "User not authenticated";
                    return;
                }
                
                const response = await api.get(`/treatment/doctor/${this.userStore.user.id}`);
                this.treatments = Array.isArray(response) ? response : (response ? [response] : []);
            } catch (err) {
                this.error = err.message || "Failed to fetch treatments";
                console.error("Fetch treatments error:", err);
            }
        },

        async fetchAvailablePatients() {
            try {
                if (!this.userStore.user || !this.userStore.user.id) {
                    return;
                }
                
                const response = await api.get(`/appointments/doctor/${this.userStore.user.id}`);
                const appointments = Array.isArray(response) ? response : (response ? [response] : []);
                
                const patientMap = {};
                appointments.forEach(apt => {
                    if (apt.patient_id && apt.patient_name) {
                        patientMap[apt.patient_id] = {
                            patient_id: apt.patient_id,
                            patient_name: apt.patient_name,
                            ap_id: apt.ap_id
                        };
                    }
                });
                
                this.availablePatients = Object.values(patientMap);
            } catch (err) {
                console.error("Failed to fetch available patients:", err);
            }
        },

        editTreatment(treatment) {
            this.isediting = true;
            this.formData = {
                t_id: treatment.t_id,
                patient_id: treatment.patient_id || '',
                appointment_id: treatment.appointment_id || '',
                diagnosis: treatment.diagnosis || '',
                prescription: treatment.prescription || '',
                notes: treatment.notes || ''
            };
            this.error = "";
            this.showModal = true;
        },

        closeModal() {
            this.showModal = false;
            this.isediting = false;
            this.formData = {
                t_id: null,
                patient_id: '',
                appointment_id: '',
                diagnosis: '',
                prescription: '',
                notes: ''
            };
            this.error = "";
        },
        
        async saveform() {
            try {
                if (!this.formData.diagnosis || !this.formData.prescription) {
                    this.error = "Diagnosis and Prescription are required";
                    return;
                }

                if (!this.isediting && (!this.formData.patient_id || !this.formData.appointment_id)) {
                    this.error = "Patient and Appointment are required for new treatments";
                    return;
                }

                this.isSaving = true;
                const payload = {
                    appointment_id: this.formData.appointment_id,
                    patient_id: this.formData.patient_id,
                    doctor_id: this.userStore.user.id,
                    diagnosis: this.formData.diagnosis,
                    prescription: this.formData.prescription,
                    notes: this.formData.notes
                };

                if (this.isediting) {
                    await api.patch(`/treatment/${this.formData.t_id}`, payload);
                    this.successMessage = "Treatment updated successfully!";
                } else {
                    await api.post('/treatments', payload);
                    this.successMessage = "Treatment created successfully!";
                }
                this.closeModal();
                this.fetchTreatments();
            } catch (err) {
                this.error = err.message || "Failed to save treatment";
                console.error("error", err);
            } finally {
                this.isSaving = false;
            }
        },

        async confirmDelete(treatment) {
            if (!window.confirm("Are you sure you want to delete this Treatment?")) {
                return;
            }

            try {
                await api.delete(`/treatment/${treatment.t_id}`);
                await this.fetchTreatments();
            } catch (err) {
                this.error = err.message || "Failed to delete treatment";
                console.error("error:", err);
            }
        },

        formatDate(dateStr) {
            if (!dateStr) return "—";
            try {
                const date = new Date(dateStr);
                return date.toLocaleDateString('en-US', { 
                    year: 'numeric', 
                    month: 'long', 
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                });
            } catch (e) {
                return dateStr;
            }
        }
    }
}
</script>

<style scoped>
.modal.d-block {
    display: block !important;
}

.modal-dialog-centered {
    display: flex;
    align-items: center;
    min-height: calc(100% - 1rem);
}

.card {
    border: none;
    border-radius: 0.5rem;
    transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1) !important;
}

.card-header {
    background-color: #f8f9fa;
    padding: 1.5rem;
    border-radius: 0.5rem 0.5rem 0 0;
}

.card-body {
    padding: 1.5rem;
}

.bg-light {
    background-color: #f8f9fa !important;
    padding: 1rem;
    border-radius: 0.375rem;
}

h1 {
    color: #0d6efd;
}

.text-primary {
    color: #0d6efd !important;
}

.fw-semibold {
    font-weight: 600;
}

.bi {
    margin-right: 0.5rem;
}

.btn-group .btn {
    border-radius: 0.375rem;
}

.modal-header {
    background: linear-gradient(135deg, #0d6efd 0%, #0a58ca 100%);
}

.form-label {
    color: #333;
    margin-bottom: 0.5rem;
}

.text-break {
    word-wrap: break-word;
    overflow-wrap: break-word;
}

.spinner-border-sm {
    width: 1rem;
    height: 1rem;
}

.btn-group .btn:focus {
    box-shadow: none;
}
</style>