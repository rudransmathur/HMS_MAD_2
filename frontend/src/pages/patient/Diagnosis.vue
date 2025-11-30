<template>
    <div class="container mt-5">
        <!-- Header -->
        <div class="mb-5">
            <h1 class="display-6 fw-bold text-primary">Your Diagnosis Reports</h1>
            <p class="text-muted">View your medical diagnosis and treatment history</p>
        </div>

        <!-- Error Alert -->
        <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
            {{ error }}
            <button type="button" class="btn-close" @click="error = ''"></button>
        </div>

        <!-- No Treatments Message -->
        <div v-if="treatments.length === 0" class="alert alert-info text-center py-5">
            <i class="bi bi-file-earmark-medical" style="font-size: 3rem; color: #0d6efd;"></i>
            <p class="mt-3 mb-0">No diagnosis reports available yet.</p>
        </div>

        <!-- Treatments List -->
        <div v-else>
            <div v-for="(treatment, index) in treatments" :key="index" class="card shadow-sm mb-4">
                <div class="card-header bg-light border-bottom">
                    <div class="row align-items-center">
                        <div class="col">
                            <h5 class="mb-0">
                                <i class="bi bi-capsule"></i> Treatment Report #{{ index + 1 }}
                            </h5>
                        </div>
                        <div class="col-auto">
                            <small class="text-muted">{{ formatDate(treatment.created_date) }}</small>
                        </div>
                    </div>
                </div>
                <div class="card-body">
                    <!-- Doctor & Appointment Info -->
                    <div class="row mb-4">
                        <div class="col-md-6">
                            <h6 class="fw-semibold text-muted mb-2">Doctor Name</h6>
                            <p>{{ treatment.doctor_name }}</p>
                        </div>
                    </div>

                    <!-- Diagnosis -->
                    <div class="mb-4">
                        <h6 class="fw-semibold text-primary mb-2">
                            <i class="bi bi-file-medical"></i> Diagnosis
                        </h6>
                        <div class="p-3 bg-light rounded">
                            <p class="mb-0">{{ treatment.diagnosis || '—' }}</p>
                        </div>
                    </div>

                    <!-- Prescription -->
                    <div class="mb-4">
                        <h6 class="fw-semibold text-primary mb-2">
                            <i class="bi bi-prescription2"></i> Prescription
                        </h6>
                        <div class="p-3 bg-light rounded">
                            <p class="mb-0">{{ treatment.prescription || '—' }}</p>
                        </div>
                    </div>

                    <!-- Notes -->
                    <div>
                        <h6 class="fw-semibold text-primary mb-2">
                            <i class="bi bi-chat-left-text"></i> Doctor's Notes
                        </h6>
                        <div class="p-3 bg-light rounded">
                            <p class="mb-0">{{ treatment.notes || '—' }}</p>
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
    name: 'DiagnosisPage',
    data() {
        return {
            error: "",
            treatments: [],
            userStore: null,
        };
    },
    created(){
        this.userStore = useUserStore();
        this.fetchTreatments();
    },
    methods: {
        async fetchTreatments() {
            try {
                if (!this.userStore.user || !this.userStore.user.id) {
                    this.error = "User not authenticated";
                    return;
                }
                
                const response = await api.get(`/treatment/patient/${this.userStore.user.id}`);
                console.log("Fetched treatments:", response);
                this.treatments = Array.isArray(response) ? response : (response ? [response] : []);
            } catch (err) {
                this.error = err.message || "Failed to fetch treatments";
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
.card {
    border: none;
    border-radius: 0.5rem;
}

.card-header {
    background-color: #f8f9fa;
    padding: 1.5rem;
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
</style>