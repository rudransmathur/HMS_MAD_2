<template>
    <div class="container mt-5 mb-5">
        <!-- Header -->
        <div class="row mb-5">
            <div class="col">
                <h1 class="display-6 fw-bold text-primary">Diagnosis & Treatment Reports</h1>
                <p class="text-muted">Manage treatment records for your patients</p>
            </div>
            <div class="col-auto">
                <button 
                    class="btn btn-primary btn-lg"
                    data-bs-toggle="modal"
                    data-bs-target="#treatmentModal"
                    @click="resetForm"
                >
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

        <!-- No Treatments Message -->
        <div v-if="treatments.length === 0" class="alert alert-info text-center py-5">
            <i class="bi bi-file-earmark-medical" style="font-size: 3rem; color: #0d6efd;"></i>
            <p class="mt-3 mb-0">No treatment reports created yet. Click "New Treatment" to create one.</p>
        </div>

        <!-- Treatments List -->
        <div v-else>
            <div v-for="(treatment, index) in treatments" :key="treatment.t_id || index" class="card shadow-sm mb-4 border-0">
                <div class="card-header bg-light border-bottom d-flex justify-content-between align-items-center">
                    <div>
                        <h5 class="mb-1">
                            <i class="bi bi-capsule"></i> Treatment Report #{{ index + 1 }}
                        </h5>
                        <small class="text-muted">Patient: <strong>{{ treatment.patient_name }}</strong> | {{ formatDate(treatment.created_date) }}</small>
                    </div>
                    <div class="btn-group" role="group">
                        <button 
                            type="button"
                            class="btn btn-sm btn-outline-warning"
                            data-bs-toggle="modal"
                            data-bs-target="#treatmentModal"
                            @click="editTreatment(treatment)"
                            title="Edit Treatment"
                        >
                            <i class="bi bi-pencil"></i> Edit
                        </button>
                        <button 
                            type="button"
                            class="btn btn-sm btn-outline-danger"
                            @click="confirmDelete(treatment)"
                            title="Delete Treatment"
                        >
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
                            <p class="mb-0 text-break">{{ treatment.diagnosis || '—' }}</p>
                        </div>
                    </div>

                    <!-- Prescription -->
                    <div class="mb-4">
                        <h6 class="fw-semibold text-primary mb-2">
                            <i class="bi bi-prescription2"></i> Prescription
                        </h6>
                        <div class="p-3 bg-light rounded">
                            <p class="mb-0 text-break">{{ treatment.prescription || '—' }}</p>
                        </div>
                    </div>

                    <!-- Notes -->
                    <div>
                        <h6 class="fw-semibold text-primary mb-2">
                            <i class="bi bi-chat-left-text"></i> Notes
                        </h6>
                        <div class="p-3 bg-light rounded">
                            <p class="mb-0 text-break">{{ treatment.notes || '—' }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Treatment Modal -->
    <div class="modal fade" id="treatmentModal" tabindex="-1" aria-labelledby="treatmentModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header bg-primary text-white">
                    <h5 class="modal-title" id="treatmentModalLabel">
                        <i class="bi" :class="isEditingTreatment ? 'bi-pencil-square' : 'bi-plus-circle'"></i>
                        {{ isEditingTreatment ? 'Edit Treatment' : 'Create New Treatment' }}
                    </h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <!-- Patient Selection (for new treatments) -->
                    <div v-if="!isEditingTreatment" class="mb-3">
                        <label class="form-label fw-semibold">Select Patient</label>
                        <select v-model="formData.patient_id" class="form-select">
                            <option value="">-- Choose a patient --</option>
                            <option v-for="patient in availablePatients" :key="patient.patient_id" :value="patient.patient_id">
                                {{ patient.patient_name }} (Appointment {{ patient.ap_id }})
                            </option>
                        </select>
                    </div>

                    <!-- Appointment Selection -->
                    <div v-if="!isEditingTreatment" class="mb-3">
                        <label class="form-label fw-semibold">Associated Appointment</label>
                        <input 
                            v-model="formData.appointment_id" 
                            type="number"
                            class="form-control"
                            placeholder="Appointment ID"
                        >
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
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button 
                        type="button" 
                        class="btn btn-primary"
                        @click="saveTreatment"
                        :disabled="isSaving"
                    >
                        <span v-if="!isSaving">
                            <i class="bi bi-check"></i> {{ isEditingTreatment ? 'Update' : 'Create' }}
                        </span>
                        <span v-else>
                            <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                            Saving...
                        </span>
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div class="modal fade" id="deleteConfirmModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-sm">
            <div class="modal-content border-danger">
                <div class="modal-header bg-danger text-white">
                    <h5 class="modal-title"><i class="bi bi-exclamation-triangle"></i> Delete Treatment</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <p>Are you sure you want to delete this treatment record? This action cannot be undone.</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button 
                        type="button" 
                        class="btn btn-danger"
                        @click="deleteTreatment"
                        :disabled="isSaving"
                    >
                        <i class="bi bi-trash"></i> Delete
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import api from '@/utils/api';
import useUserStore from '@/stores/user';
// Use global bootstrap that is imported in main.js

export default {
    name: 'DoctorDiagnosisPage',
    data() {
        return {
            error: "",
            successMessage: "",
            treatments: [],
            availablePatients: [],
            userStore: null,
            isEditingTreatment: false,
            isSaving: false,
            formData: {
                t_id: null,
                patient_id: '',
                appointment_id: '',
                diagnosis: '',
                prescription: '',
                notes: ''
            },
            treatmentToDelete: null,
            deleteModal: null,
        };
    },
    created(){
        this.userStore = useUserStore();
        this.fetchTreatments();
        this.fetchAvailablePatients();
    },
    mounted(){
        // Initialize modal references for manual control using global bootstrap
        const deleteConfirmElement = document.getElementById('deleteConfirmModal');
        if (deleteConfirmElement && window && window.bootstrap && window.bootstrap.Modal) {
            this.deleteModal = new window.bootstrap.Modal(deleteConfirmElement);
        }
    },
    methods: {
        async fetchTreatments() {
            try {
                if (!this.userStore.user || !this.userStore.user.id) {
                    this.error = "User not authenticated";
                    return;
                }
                
                const response = await api.get(`/treatment/doctor/${this.userStore.user.id}`);
                console.log("Fetched treatments:", response);
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
                
                // Extract unique patients from appointments
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
        resetForm() {
            this.isEditingTreatment = false;
            this.formData = {
                t_id: null,
                patient_id: '',
                appointment_id: '',
                diagnosis: '',
                prescription: '',
                notes: ''
            };
        },
        editTreatment(treatment) {
            this.isEditingTreatment = true;
            this.formData = {
                t_id: treatment.t_id,
                patient_id: treatment.patient_id || '',
                appointment_id: treatment.appointment_id || '',
                diagnosis: treatment.diagnosis || '',
                prescription: treatment.prescription || '',
                notes: treatment.notes || ''
            };
        },
        async saveTreatment() {
            try {
                // Validate required fields
                if (!this.formData.diagnosis || !this.formData.prescription) {
                    this.error = "Diagnosis and Prescription are required";
                    return;
                }

                if (!this.isEditingTreatment && (!this.formData.patient_id || !this.formData.appointment_id)) {
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

                if (this.isEditingTreatment) {
                    // Update existing treatment
                    await api.patch(`/treatment/${this.formData.t_id}`, payload);
                    this.successMessage = "Treatment updated successfully!";
                } else {
                    // Create new treatment
                    await api.post('/treatments', payload);
                    this.successMessage = "Treatment created successfully!";
                }

                // Close modal and refresh
                const modal = Modal.getInstance(document.getElementById('treatmentModal'));
                if (modal) modal.hide();
                
                setTimeout(() => {
                    this.fetchTreatments();
                    this.error = '';
                }, 500);
            } catch (err) {
                this.error = err.message || "Failed to save treatment";
            } finally {
                this.isSaving = false;
            }
        },
        confirmDelete(treatment) {
            this.treatmentToDelete = treatment;
            this.deleteModal.show();
        },
        async deleteTreatment() {
            try {
                if (!this.treatmentToDelete) return;
                
                this.isSaving = true;
                await api.delete(`/treatment/${this.treatmentToDelete.t_id}`);
                this.successMessage = "Treatment deleted successfully!";
                
                this.deleteModal.hide();
                setTimeout(() => {
                    this.fetchTreatments();
                    this.treatmentToDelete = null;
                }, 500);
            } catch (err) {
                this.error = err.message || "Failed to delete treatment";
            } finally {
                this.isSaving = false;
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