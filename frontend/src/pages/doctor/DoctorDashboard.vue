<template>
    <div class="container mt-5">
        <!-- Welcome Section -->
        <div class="mb-5">
            <h1 class="display-6 fw-bold text-primary">Welcome, {{ userStore.user?.fullname || 'Doctor' }}!</h1>
        </div>

        <!-- Error Alert -->
        <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
            {{ error }}
            <button type="button" class="btn-close" @click="error = ''"></button>
        </div>

        <!-- Appointments Section -->
        <div class="card shadow-lg mb-5">
            <div class="card-header bg-primary text-white">
                <h3 class="mb-0"><i class="bi bi-calendar-check"></i> Your Appointments</h3>
            </div>
            <div class="card-body">
                <!-- No Appointments Message -->
                <div v-if="appointments.length === 0" class="text-center py-5">
                    <i class="bi bi-inbox" style="font-size: 3rem; color: #ccc;"></i>
                    <p class="text-muted mt-3">You don't have any appointments yet.</p>
                </div>

                <!-- Appointments List -->
                <div v-else>
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead class="table-light">
                                <tr>
                                    <th><i class="bi bi-person-fill"></i> Patient</th>
                                    <th><i class="bi bi-calendar"></i> Date</th>
                                    <th><i class="bi bi-clock"></i> Time</th>
                                    <th><i class="bi bi-info-circle"></i> Status</th>
                                    <th><i class="bi bi-chat"></i> Reason</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="appointment in appointments" :key="appointment.ap_id">
                                    <td class="fw-semibold">{{ appointment.patient_name }}</td>
                                    <td>{{ formatDate(appointment.appointment_date) }}</td>
                                    <td>{{ appointment.appointment_time }}</td>
                                    <td>
                                        <span :class="getStatusBadge(appointment.status)">
                                            {{ appointment.status }}
                                        </span>
                                    </td>
                                    <td>{{ appointment.reason || "—" }}</td>
                                </tr>
                            </tbody>
                        </table>
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
    name: "PatientDashboard",
    data() {
        return {
            error: "",
            appointments: [],
            doctors: [],
            userStore: null,
            isSubmitting: false,
            formData: {
                doctor_id: "",
                appointment_date: "",
                appointment_time: "",
                reason: "",
                status: "Pending"
            }
        };
    },
    created() {
        this.userStore = useUserStore();
        this.fetchAppointments();
    },
    methods: {
        async fetchAppointments() {
            try {
                if (!this.userStore.user || !this.userStore.user.id) {
                    this.error = "User not authenticated";
                    return;
                }
                
                const response = await api.get(`/appointments/doctor/${this.userStore.user.id}`);
                // Filter out null/undefined appointments
                this.appointments = (Array.isArray(response) ? response : [response]).filter(apt => apt && apt.ap_id);
            } catch (err) {
                this.error = err.message || "Failed to fetch appointments";
                console.error("error:", err);
            }
        },
        async fetchDoctors() {
            try {
                const response = await api.get('/patient');
                // Filter to only get valid, active doctors
                this.doctors = (Array.isArray(response) ? response : [response])
                    .filter(doctor => doctor && doctor.user_id && doctor.fullname && doctor.is_active !== false);
            } catch (err) {
                this.error = "Failed to fetch doctors: " + (err.message || "Unknown error");
                console.error("Failed to fetch doctors:", err);
            }
        },
        formatDate(dateStr) {
            if (!dateStr) return "—";
            const date = new Date(dateStr);
            return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
        },
        getStatusBadge(status) {
            const badges = {
                'Pending': 'badge bg-warning text-dark',
                'Confirmed': 'badge bg-info',
                'Completed': 'badge bg-success',
                'Cancelled': 'badge bg-danger'
            };
            return badges[status] || 'badge bg-secondary';
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

.table-hover tbody tr:hover {
    background-color: #f5f5f5;
}

.badge {
    padding: 0.5rem 0.75rem;
    font-size: 0.875rem;
}

.btn-lg {
    padding: 0.75rem 2rem;
    font-size: 1.1rem;
}

h1 {
    color: #0d6efd;
}

.card {
    border: none;
    border-radius: 0.5rem;
}

.card-header {
    border-radius: 0.5rem 0.5rem 0 0;
    padding: 1.5rem;
}

.form-label {
    color: #333;
}

.text-danger {
    color: #dc3545;
}
</style>