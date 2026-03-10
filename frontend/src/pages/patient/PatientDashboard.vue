<template>
    <div class="container mt-5">
        <!-- Welcome Section -->
        <div class="mb-5">
            <h1 class="display-6 fw-bold text-primary">Welcome, {{ userStore.user?.fullname || 'Patient' }}!</h1>
            <p class="text-muted">Manage your appointments and healthcare needs</p>
        </div>

        <!-- Error -->
        <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
            {{ error }}
        </div>

        <!-- Appointments -->
        <div class="card shadow-lg mb-5">
            <div class="card-header bg-primary text-white">
                <h3 class="mb-0"><i class="bi bi-calendar-check"></i> Today's Appointments</h3>
            </div>
            <div class="card-body">
                <!-- No Appointments  -->
                <div v-if="presentAppointments.length === 0" class="text-center py-5">
                    <i class="bi bi-inbox" style="font-size: 3rem; color: #ccc;"></i>
                    <p class="text-muted mt-3">You haven't booked any appointments yet.</p>
                    <p class="text-muted">Click the "Book Appointment" button below to get started.</p>
                </div>

                <!-- Appointments List -->
                <div v-else>
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead class="table-light">
                                <tr>
                                    <th><i class="bi bi-person-fill"></i> Doctor</th>
                                    <th><i class="bi bi-calendar"></i> Date</th>
                                    <th><i class="bi bi-clock"></i> Time</th>
                                    <th><i class="bi bi-info-circle"></i> Status</th>
                                    <th><i class="bi bi-chat"></i> Reason</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="appointment in presentAppointments" :key="appointment.ap_id">
                                    <td class="fw-semibold">{{ getDoctorName(appointment.doctor_id) }}</td>
                                    <td>{{ formatDate(appointment.appointment_date) }}</td>
                                    <td>{{ appointment.appointment_time }}</td>
                                    <td>
                                        <span :class="getStatusBadge(appointment.status)">
                                            {{ appointment.status }}
                                        </span>
                                    </td>
                                    <td>{{ appointment.reason || "—" }}</td>
                                    <td>
                                        <button class="btn btn-sm btn-warning me-2" @click="editAppointment(appointment)" title="Edit">
                                            <i class="bi bi-pencil"></i>
                                        </button>
                                        <button class="btn btn-sm btn-danger" @click="deleteAppointment(appointment.ap_id)" title="Delete">
                                            <i class="bi bi-trash"></i>
                                        </button>
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
                <!-- No Appointments  -->
                <div v-if="futureAppointments.length === 0" class="text-center py-5">
                    <i class="bi bi-inbox" style="font-size: 3rem; color: #ccc;"></i>
                    <p class="text-muted mt-3">You haven't booked any appointments yet.</p>
                    <p class="text-muted">Click the "Book Appointment" button below to get started.</p>
                </div>

                <!-- Appointments List -->
                <div v-else>
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead class="table-light">
                                <tr>
                                    <th><i class="bi bi-person-fill"></i> Doctor</th>
                                    <th><i class="bi bi-calendar"></i> Date</th>
                                    <th><i class="bi bi-clock"></i> Time</th>
                                    <th><i class="bi bi-info-circle"></i> Status</th>
                                    <th><i class="bi bi-chat"></i> Reason</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="appointment in futureAppointments" :key="appointment.ap_id">
                                    <td class="fw-semibold">{{ getDoctorName(appointment.doctor_id) }}</td>
                                    <td>{{ formatDate(appointment.appointment_date) }}</td>
                                    <td>{{ appointment.appointment_time }}</td>
                                    <td>
                                        <span :class="getStatusBadge(appointment.status)">
                                            {{ appointment.status }}
                                        </span>
                                    </td>
                                    <td>{{ appointment.reason || "—" }}</td>
                                    <td>
                                        <button class="btn btn-sm btn-warning me-2" @click="editAppointment(appointment)" title="Edit">
                                            <i class="bi bi-pencil"></i>
                                        </button>
                                        <button class="btn btn-sm btn-danger" @click="deleteAppointment(appointment.ap_id)" title="Delete">
                                            <i class="bi bi-trash"></i>
                                        </button>
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
                <h3 class="mb-0"><i class="bi bi-calendar-check"></i> Past Appointments</h3>
            </div>
            <div class="card-body">
                <!-- No Appointments  -->
                <div v-if="pastAppointments.length === 0" class="text-center py-5">
                    <i class="bi bi-inbox" style="font-size: 3rem; color: #ccc;"></i>
                    <p class="text-muted mt-3">You haven't booked any appointments yet.</p>
                    <p class="text-muted">Click the "Book Appointment" button below to get started.</p>
                </div>

                <!-- Appointments List -->
                <div v-else>
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead class="table-light">
                                <tr>
                                    <th><i class="bi bi-person-fill"></i> Doctor</th>
                                    <th><i class="bi bi-calendar"></i> Date</th>
                                    <th><i class="bi bi-clock"></i> Time</th>
                                    <th><i class="bi bi-info-circle"></i> Status</th>
                                    <th><i class="bi bi-chat"></i> Reason</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="appointment in pastAppointments" :key="appointment.ap_id">
                                    <td class="fw-semibold">{{ getDoctorName(appointment.doctor_id) }}</td>
                                    <td>{{ formatDate(appointment.appointment_date) }}</td>
                                    <td>{{ appointment.appointment_time }}</td>
                                    <td>
                                        <span :class="getStatusBadge(appointment.status)">
                                            {{ appointment.status }}
                                        </span>
                                    </td>
                                    <td>{{ appointment.reason || "—" }}</td>
                                    <td>
                                        <button class="btn btn-sm btn-warning me-2" @click="editAppointment(appointment)" title="Edit">
                                            <i class="bi bi-pencil"></i>
                                        </button>
                                        <button class="btn btn-sm btn-danger" @click="deleteAppointment(appointment.ap_id)" title="Delete">
                                            <i class="bi bi-trash"></i>
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <!-- Book Appointment Button -->
        <div class="text-center mb-5">
            <button class="btn btn-primary btn-lg" @click="showModal = true">
                <i class="bi bi-plus-circle"></i> Book Appointment
            </button>
        </div>

        <!-- Add/Edit Appointment Modal -->
        <div v-if="showModal" class="modal d-block" style="background-color: rgba(0,0,0,0.5);">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header bg-primary text-white">
                        <h5 class="modal-title">{{ editingAppointment ? 'Edit Appointment' : 'Book New Appointment' }}</h5>
                        <button type="button" class="btn-close btn-close-white" @click="closeModal"></button>
                    </div>
                    <div class="modal-body">
                        <form @submit.prevent="submitAppointment">
                            <!-- Doctor Selection -->
                            <div class="mb-3">
                                <label for="doctor" class="form-label fw-semibold">Select Doctor <span class="text-danger">*</span></label>
                                <select v-model="formData.doctor_id" id="doctor" class="form-select" required @change="getavailability(formData.doctor_id)">
                                    <option value="">-- Choose a Doctor --</option> 
                                    <option v-for="doctor in doctors" :key="doctor.user_id" :value="doctor.user_id">
                                        Dr. {{ doctor.fullname }} - {{ doctor.specialization }}
                                    </option>
                                </select>
                            </div>

                            <!-- Appointment Date -->
                            <div class="mb-3">
                                <label for="date" class="form-label fw-semibold">Appointment Date <span class="text-danger">*</span></label>
                                <select v-model="formData.appointment_date" id="date" class="form-select" required>
                                    <option value="">-- Select Date --</option>
                                    <option v-for="slot in allAvailabilities" :key="slot.date" :value="slot.date">
                                        {{ slot.date }}
                                    </option>
                                </select>
                            </div>

                            <!-- Appointment Time -->
                            <div class="mb-3">
                                <label for="time" class="form-label fw-semibold">Appointment Time <span class="text-danger">*</span></label>
                                <select v-model="formData.appointment_time" id="time" class="form-select" required>
                                    <option value="">-- Select Time --</option>
                                    <option v-for="time in availabilities" :key="time" :value="time">{{ time }}</option>
                                </select>
                            </div>
                            <!-- Reason -->
                            <div class="mb-3">
                                <label for="reason" class="form-label fw-semibold">Reason for Visit <span class="text-danger">*</span></label>
                                <textarea v-model="formData.reason" id="reason" class="form-control" rows="3" placeholder="Describe your symptoms or reason" required></textarea>
                            </div>
                            <div v-if="modalError" class="mt-2 alert alert-danger alert-dismissible fade show" role="alert">
                                {{ modalError }}
                            </div>

                            <!-- Form Actions -->
                            <div class="d-flex gap-2">
                                <button type="submit" class="btn btn-primary flex-grow-1" :disabled="isSubmitting">
                                    <i class="bi bi-check-circle"></i> {{ isSubmitting ? 'Saving...' : 'Save Appointment' }}
                                </button>
                                <button type="button" class="btn btn-secondary" @click="closeModal">
                                    <i class="bi bi-x-circle"></i> Cancel
                                </button>
                            </div>
                        </form>
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
            modalError: "",
            appointments: [],
            presentAppointments: [],
            pastAppointments: [],
            futureAppointments: [],
            doctor_apt: [],
            doctors: [],
            availabilities: [],
            allAvailabilities: [],
            userStore: null,
            showModal: false,
            editingAppointment: null,
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
        this.fetchDoctors();
    },
    watch: {
        'formData.appointment_date': function() {
            this.filterAvailabilitiesByDate();
        },
        'formData.doctor_id': function() {
            // When doctor changes, clear date and time, and reset availabilities
            this.formData.appointment_date = "";
            this.formData.appointment_time = "";
            this.availabilities = [];
            this.allAvailabilities = [];
        }
    },
    methods: {
        async fetchAppointments() {
            try {
                if (!this.userStore.user || !this.userStore.user.id) {
                    this.error = "User not authenticated";
                    return;
                }
                
                const response = await api.get(`/appointments/patient/${this.userStore.user.id}`);
                // Filter out null/undefined appointments
                this.appointments = (Array.isArray(response) ? response : [response]).filter(apt => apt && apt.ap_id);
            } catch (err) {
                this.error = err.message || "Failed to fetch appointments";
                console.error("error:", err);
            }
            finally{
                console.log("Appointments:", this.appointments);
                await this.sortAppointents();
            }
        },

        async sortAppointents(){
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
                const response = await api.get('/doctors');
                // Filter to only get valid, active doctors
                this.doctors = (Array.isArray(response) ? response : [response])
                    .filter(doctor => doctor && doctor.user_id && doctor.fullname && doctor.is_active !== false);
            } catch (err) {
                this.error = "Failed to fetch doctors: " + (err.message || "Unknown error");
                console.error("Failed to fetch doctors:", err);
            }
        },

        async getavailability(doctorId) {
            this.modalError = "";
            try {
                const res = await api.get(`/allavailability/${doctorId}`);
                const total_availabilities = (Array.isArray(res) ? res : [res]);
                this.allAvailabilities = total_availabilities;
            } catch (err) {
                this.modalError = err.message || "Failed to fetch availability";
                console.error("Failed to fetch availability:", err);
                this.allAvailabilities = [];
            }
            try {
                const doctor_apt_res = await api.get(`/appointments/doctor/${doctorId}`);
                this.doctor_apt = (Array.isArray(doctor_apt_res) ? doctor_apt_res : [doctor_apt_res]);
            } catch (error) {
                this.modalError = error.message || "Failed to fetch doctor's appointments";
                console.error("Failed to fetch doctor's appointments:", error);
                this.doctor_apt = [];
            }
            this.filterAvailabilitiesByDate();
        },

        filterAvailabilitiesByDate() {
            if (!this.allAvailabilities || !this.formData.appointment_date) {
                this.availabilities = [];
                return;
            }
            // Find all slots for the selected date
            const slotsForDate = this.allAvailabilities.filter(
                slot => slot.date === this.formData.appointment_date
            );
            // Get all booked times for this doctor on this date
            const bookedTimes = this.doctor_apt
                .filter(apt => apt.appointment_date === this.formData.appointment_date)
                .map(apt => apt.appointment_time);

            // For each slot, generate all possible times in the slot's range (30 min interval)
            let availableTimes = [];
            slotsForDate.forEach(slot => {
                let start = slot.start_time;
                let end = slot.end_time;
                let current = start;
                while (current < end) {
                    if (!bookedTimes.includes(current)) {
                        availableTimes.push(current);
                    }
                    // Increment by 30 minutes
                    let [h, m, s] = current.split(':').map(Number);
                    m += 30;
                    if (m >= 60) {
                        h += 1;
                        m -= 60;
                    }
                    current = `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:00`;
                    if (current > end) break;
                }
            });
            this.availabilities = availableTimes;
        },
        // ...existing code...
        getSlotTimes(slot) {
            console.log(slot);
            let times = [];
            let start = slot.start_time;
            let end = slot.end_time;
            let current = start;
            while (current < end) {
                times.push(current);
                let [h, m, s] = current.split(':').map(Number);
                m += 30;
                if (m >= 60) {
                    h += 1;
                    m -= 60;
                }
                current = `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:00`;
                if (current > end) break;
            }
            return times;
        },

        getDoctorName(doctorId) {
            const doctor = this.doctors.find(d => d.user_id === doctorId);
            return doctor ? `Dr. ${doctor.fullname}` : "Unknown Doctor";
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

        editAppointment(appointment) {
            this.editingAppointment = appointment;
            this.formData = {
                doctor_id: appointment.doctor_id,
                appointment_date: appointment.appointment_date,
                appointment_time: appointment.appointment_time,
                reason: appointment.reason,
                status: appointment.status
            };
            this.showModal = true;
        },

        closeModal() {
            this.showModal = false;
            this.editingAppointment = null;
            this.formData = {
                doctor_id: "",
                appointment_date: "",
                appointment_time: "",
                reason: "",
                status: "Pending"
            };
        },

        async submitAppointment() {
            try {
                this.isSubmitting = true;
                const payload = {
                    patient_id: this.userStore.user.id,
                    doctor_id: this.formData.doctor_id,
                    appointment_date: this.formData.appointment_date,
                    appointment_time: this.formData.appointment_time,
                    status: this.formData.status,
                    reason: this.formData.reason
                };

                if (this.editingAppointment) {
                    // Update existing appointment
                    await api.patch(`/appointments/${this.editingAppointment.ap_id}`, payload);
                } else {
                    // Create new appointment
                    await api.post('/appointments', payload);
                }

                this.closeModal();
                await this.fetchAppointments();
            } catch (err) {
                this.error = err.message || "Failed to save appointment";
                console.error("error:", err);
            } finally {
                this.isSubmitting = false;
            }
        },

        async deleteAppointment(apId) {
            if (!window.confirm("Are you sure you want to delete this appointment?")) {
                return;
            }

            try {
                await api.delete(`/appointments/${apId}`);
                await this.fetchAppointments();
            } catch (err) {
                this.error = err.message || "Failed to delete appointment";
                console.error("error:", err);
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