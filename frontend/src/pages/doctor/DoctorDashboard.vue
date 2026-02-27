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

        <!-- Current Appointments Section -->
        <div class="card shadow-lg mb-5">
            <div class="card-header bg-primary text-white">
                <h3 class="mb-0"><i class="bi bi-calendar-check"></i> Today's Appointments</h3>
            </div>
            <div class="card-body">
                <!-- No Appointments Message -->
                <div v-if="presentAppointments.length === 0" class="text-center py-5">
                    <i class="bi bi-inbox" style="font-size: 3rem; color: #ccc;"></i>
                    <p class="text-muted mt-3">You don't have any appointment today.</p>
                </div>

                <!-- Present Appointments List -->
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
                                    <th><i class="bi bi-info-circle"> Change Status</i></th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="appointment in presentAppointments" :key="appointment.ap_id">
                                    <td class="fw-semibold">{{ appointment.patient_name }}</td>
                                    <td>{{ formatDate(appointment.appointment_date) }}</td>
                                    <td>{{ appointment.appointment_time }}</td>
                                    <td>
                                        <span :class="getStatusBadge(appointment.status)">
                                            {{ appointment.status }}
                                        </span>
                                    </td>
                                    <td>{{ appointment.reason }}</td>
                                    <td>
                                        <select class="form-select form-select-sm" v-model="appointment.status" @change="changestatus(appointment)">
                                            <option value="Pending">Pending</option>
                                            <option value="Cancelled">Cancelled</option>
                                            <option value="Completed">Completed</option>
                                        </select>
                                    </td>
                                </tr>
                            </tbody>
                        </table>

                    </div>
                </div>
            </div>
        </div>
        <div class="card shadow-lg mb-5">
            <div class="card-header bg-primary text-white">
                <h3 class="mb-0"><i class="bi bi-calendar-check"></i> Future Appointments</h3>
            </div>
            <div class="card-body">
                <!-- No Appointments Message -->
                <div v-if="futureAppointments.length === 0" class="text-center py-5">
                    <i class="bi bi-inbox" style="font-size: 3rem; color: #ccc;"></i>
                    <p class="text-muted mt-3">You don't have any appointments yet.</p>
                </div>

                <!-- Future Appointments List -->
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
                                <tr v-for="appointment in futureAppointments" :key="appointment.ap_id">
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
        <div class="card shadow-lg mb-5">
            <div class="card-header bg-primary text-white">
                <h3 class="mb-0"><i class="bi bi-calendar-check"></i> Past Appointments</h3>
            </div>
            <div class="card-body">
                <!-- No Appointments Message -->
                <div v-if="pastAppointments.length === 0" class="text-center py-5">
                    <i class="bi bi-inbox" style="font-size: 3rem; color: #ccc;"></i>
                    <p class="text-muted mt-3">No past appointments available.</p>
                </div>

                <!-- Past Appointments List -->
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
                                    <th><i class="bi bi-info-circle"> Change Status</i></th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="appointment in pastAppointments" :key="appointment.ap_id">
                                    <td class="fw-semibold">{{ appointment.patient_name }}</td>
                                    <td>{{ formatDate(appointment.appointment_date) }}</td>
                                    <td>{{ appointment.appointment_time }}</td>
                                    <td>
                                        <span :class="getStatusBadge(appointment.status)">
                                            {{ appointment.status }}
                                        </span>
                                    </td>
                                    <td>{{ appointment.reason || "—" }}</td>
                                    <td>
                                        <select class="form-select form-select-sm" v-model="appointment.status" @change="changestatus(appointment)">
                                            <option value="Cancelled">Cancelled</option>
                                            <option value="Completed">Completed</option>
                                        </select>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div v-if="showModal" class="modal d-block" tabindex="-1" aria-labelledby="treatmentModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header bg-primary text-white">
                    <h5 class="modal-title" id="treatmentModalLabel">
                        <i class="bi bi-pencil-square"></i>
                        Create New Treatment
                    </h5>
                    <button type="button" class="btn-close btn-close-white" @click="closeModal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="saveform">
                        <!-- Patient Selection (for new treatments) -->
                        <div class="mb-3">
                            Patient name: {{ this.modalPatient }}
                        </div>

                        <!-- Diagnosis -->
                        <div class="mb-3">
                            <label class="form-label fw-semibold">Diagnosis</label>
                            <textarea 
                                v-model="trformData.diagnosis"
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
                                v-model="trformData.prescription"
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
                                v-model="trformData.notes"
                                class="form-control"
                                rows="3"
                                placeholder="Any additional notes or recommendations..."
                            ></textarea>
                        </div>
                        <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
                        <button type="submit" class="btn btn-primary" :disabled="isSaving">
                            <span v-if="!isSaving">
                                Create
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
    name: "DoctorDashboard",
    data() {
        return {
            error: "",
            appointments: [],
            presentAppointments: [],
            pastAppointments: [],
            futureAppointments: [],
            doctors: [],
            userStore: null,
            showModal: false,
            modalPatient: null,
            isSaving: false,
            isSubmitting: false,
            trformData: {
                t_id: null,
                patient_id: '',
                appointment_id: null,
                diagnosis: '',
                prescription: '',
                notes: ''
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
                const resp = await api.get(`/appointments/doctor/${this.userStore.user.id}`);
                this.appointments = Array.isArray(resp) ? resp : (resp ? [resp] : []);
            } catch (err) {
                this.error = err.message || "Failed to fetch appointments";
                console.error("error:", err);
            }
            this.classifyAppointments();
        },

        async classifyAppointments(){
            const today = new Date();
            const year = today.getFullYear();
            const month = String(today.getMonth() + 1).padStart(2, '0');
            const day = String(today.getDate()).padStart(2, '0');
            const todayStr = `${year}-${month}-${day}`;
            this.presentAppointments = this.appointments.filter(apt => {
                const aptDate = new Date(apt.appointment_date);
                const aptDateStr = `${aptDate.getFullYear()}-${String(aptDate.getMonth() + 1).padStart(2, '0')}-${String(aptDate.getDate()).padStart(2, '0')}`;
                return aptDateStr === todayStr;
            });
            this.pastAppointments = this.appointments.filter(apt => {
                const aptDate = new Date(apt.appointment_date);
                const aptDateStr = `${aptDate.getFullYear()}-${String(aptDate.getMonth() + 1).padStart(2, '0')}-${String(aptDate.getDate()).padStart(2, '0')}`;
                return aptDateStr < todayStr;
            });
            this.futureAppointments = this.appointments.filter(apt => {
                const aptDate = new Date(apt.appointment_date);
                const aptDateStr = `${aptDate.getFullYear()}-${String(aptDate.getMonth() + 1).padStart(2, '0')}-${String(aptDate.getDate()).padStart(2, '0')}`;
                return aptDateStr > todayStr;
            });
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

        async changestatus(appointment) {
            try {
                if (appointment.status === "Completed") {
                    this.showModal = true;
                    this.trformData = {
                        t_id: null,
                        patient_id: appointment.patient_id,
                        appointment_id: appointment.ap_id,
                        diagnosis: '',
                        prescription: '',
                        notes: ''
                    };
                    this.modalPatient = appointment.patient_name;
                }
                else{
                    const payload = {
                        status: appointment.status
                    };
                    const res = api.patch(`/appointments/${appointment.ap_id}`, payload);
                    if (res.message) {
                        this.error = res.message;
                        console.error("Status update error:", res.message);
                    }
                    else {
                        console.log("Status updated:", appointment.status);
                    }
                }
            } catch (err) {
                this.error = "Failed to update appointment status";
                console.error("Status update failed:", err);
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
        },
        
        closeModal() {
            this.showModal = false;
            this.trformData = {
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
                if (!this.trformData.diagnosis || !this.trformData.prescription) {
                    this.error = "Diagnosis and Prescription are required";
                    return;
                }
                this.isSaving = true;
                const payload = {
                    appointment_id: this.trformData.appointment_id,
                    patient_id: this.trformData.patient_id,
                    doctor_id: this.userStore.user.id,
                    diagnosis: this.trformData.diagnosis,
                    prescription: this.trformData.prescription,
                    notes: this.trformData.notes
                };
                console.log(payload)
                await api.post('/treatments', payload);
                this.successMessage = "Treatment created successfully!";
                const ap_payload = {
                    status: "Completed"
                };

                console.log(ap_payload, this.trformData.appointment_id)
                const res = await api.patch(`/appointments/${this.trformData.appointment_id}`, ap_payload);
                if (res && res.message) {
                    this.error = res.message;
                    console.error("Status update error:", res.message);
                    this.closeModal();
                }
                else {
                    console.log("Status updated: Completed");
                    this.closeModal();
                }
            } catch (err) {
                this.error = err.message || "Failed to save treatment";
                console.error("error", err);
            } finally {
                this.isSaving = false;
            }
        },
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