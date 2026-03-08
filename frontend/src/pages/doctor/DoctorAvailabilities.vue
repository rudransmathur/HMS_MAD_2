<template>
    <div class="container-fluid py-5">
        <!-- Header -->
        <div class="d-flex justify-content-between align-items-center mb-4">
            <div>
                <h1 class="mb-1">My Availabilities</h1>
                <p class="text-muted">Manage your availability for the next 7 days</p>
            </div>
        </div>

        <!-- Alert Messages -->
        <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
            {{ error }}
            <button type="button" class="btn-close" @click="error = ''"></button>
        </div>
        <div v-if="successMessage" class="alert alert-success alert-dismissible fade show" role="alert">
            {{ successMessage }}
            <button type="button" class="btn-close" @click="successMessage = ''"></button>
        </div>

        <!-- Weekly Availability View -->
        <div class="row g-3 mb-5">
            <div v-for="day in upcomingWeek" :key="day.date" class="col-lg-3 col-md-6 col-sm-12">
                <div class="card h-100 shadow-sm">
                    <!-- Heading -->
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">{{ formatDayName(day.date) }}</h5>
                        <small class="text-white-50">{{ formatDateShort(day.date) }}</small>
                    </div>
                    <!-- All slots -->
                    <div class="card-body">
                        <div v-if="day.availabilities.length === 0" class="text-muted text-center py-3">
                            <p class="mb-0">No availabilities set</p>
                        </div>
                        <div v-else class="list-group list-group-flush">
                            <div v-for="slot in day.availabilities" :key="slot.dav_id" class="d-flex justify-content-between align-items-center py-2 border-bottom">
                                <div>
                                    <p class="mb-0 fw-bold">{{ formatTime(slot.start_time) }}-{{ formatTime(slot.end_time) }}</p>
                                    <small class="text-muted">Available</small>
                                </div>
                                <div class="btn-group btn-group-sm" role="group">
                                    <button type="button" class="btn btn-outline-info" @click="openEditModal(slot)" title="Edit">
                                        <i class="bi bi-pencil"></i>
                                    </button>
                                    <button type="button" class="btn btn-outline-danger" @click="confirmDelete(slot)" title="Delete">
                                        <i class="bi bi-trash"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Card Footer with Add Button -->
                    <div class="card-footer bg-light">
                        <button class="btn btn-sm btn-outline-primary w-100" @click="openAddModalForDate(day.date)">
                            <i class="bi bi-plus"></i> Add Time
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Section 2: Add/Edit Modal -->
        <div class="modal fade" id="availabilityModal" tabindex="-1">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <!-- Modal Header -->
                    <div class="modal-header">
                        <h5 class="modal-title">
                            {{ editingSlot ? 'Edit Availability' : 'Add Availability' }}
                        </h5>
                        <button type="button" class="btn-close" @click="closeModal"></button>
                    </div>

                    <!-- Modal Body -->
                    <div class="modal-body">
                        <form @submit.prevent="submitForm" id="availabilityForm">
                            <!-- Date Field -->
                            <div class="mb-3">
                                <label for="availabilityDate" class="form-label fw-bold">Date</label>
                                <input
                                    type="date"
                                    class="form-control"
                                    id="availabilityDate"
                                    v-model="formData.date"
                                    :min="getTommDate()"
                                    :max="getMaxDate()"
                                    @change="validateForm"
                                    required
                                />
                            </div>

                            <!-- Start Time Field -->
                            <div class="mb-3">
                                <label for="availabilityStartTime" class="form-label fw-bold">Start Time</label>
                                <input
                                    type="time"
                                    class="form-control"
                                    id="availabilityStartTime"
                                    v-model="formData.start_time"
                                    @change="validateForm"
                                    required
                                />
                            </div>

                            <!-- End Time Field -->
                            <div class="mb-3">
                                <label for="availabilityEndTime" class="form-label fw-bold">End Time</label>
                                <input
                                    type="time"
                                    class="form-control"
                                    id="availabilityEndTime"
                                    v-model="formData.end_time"
                                    min="00:00"
                                    step="1800"
                                    @change="validateForm"
                                    required
                                />
                            </div>

                            <!-- Validation Messages -->
                            <div v-if="formErrors.length > 0" class="alert alert-warning">
                                <p class="mb-0 fw-bold">Please fix the following:</p>
                                <ul class="mb-0 mt-2">
                                    <li v-for="(error, index) in formErrors" :key="index">{{ error }}</li>
                                </ul>
                            </div>

                            <!-- Summary -->
                            <div v-if="formData.date && formData.time" class="alert alert-info">
                                <strong>Summary:</strong> Available on {{ formatDateLong(formData.date) }} at {{ formData.time }}
                            </div>
                        </form>
                    </div>

                    <!-- Modal Footer -->
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" @click="closeModal">
                            Cancel
                        </button>
                        <button 
                            type="submit"
                            form="availabilityForm"
                            class="btn btn-primary"
                            :disabled="isSubmitting || formErrors.length > 0"
                        >
                            <span v-if="isSubmitting" class="me-2"></span>
                            {{ editingSlot ? 'Update' : 'Add' }}
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Delete Confirmation Modal -->
        <div class="modal fade" id="deleteConfirmModal" tabindex="-1">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header border-danger">
                        <h5 class="modal-title text-danger">
                            <i class="bi bi-exclamation-triangle"></i> Confirm Delete
                        </h5>
                        <button type="button" class="btn-close" @click="closeDeleteModal"></button>
                    </div>
                    <div class="modal-body">
                        <p v-if="slotToDelete">
                            Are you sure you want to delete the availability on 
                            <strong>{{ formatDateLong(slotToDelete.date) }} </strong>
                            from <strong>{{ formatTime(slotToDelete.start_time) }} </strong>
                            to <strong>{{ formatTime(slotToDelete.end_time) }}?</strong>
                        </p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" @click="closeDeleteModal">
                            Cancel
                        </button>
                        <button type="button" class="btn btn-danger" @click="deleteAvailability">
                            <span v-if="isSubmitting" class="me-2"></span>
                            Delete
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import api from '@/utils/api';
    import useUserStore from '@/stores/user';
    import { Modal } from 'bootstrap';

    export default {
        data() {
            return {
                appointments: [],
                availabilities: [],
                upcomingWeek: [],
                error: '',
                successMessage: '',
                isSubmitting: false,
                isLoading: true,
                userStore: null,
                
                formData: {
                    date: '',
                    start_time: '',
                    end_time: '',
                },
                editingSlot: null,
                formErrors: [],
                
                // Delete confirmation
                slotToDelete: null,
                
                // Modal instances
                availabilityModal: null,
                deleteConfirmModal: null,
            };
        },
        
        methods: {
            async fetchDoctorAppointments(){
                try {
                    const resp = await api.get(`/appointments/doctor/${this.userStore.user.id}`);
                    this.appointments = Array.isArray(resp) ? resp : (resp ? [resp] : []);
                } catch (err) {
                    this.error = err.message;
                    console.error('error:', err);
                }
            },
            
            async fetchAvailabilities() {
                try {
                    this.isLoading = true;
                    this.error = '';
                    
                    if (!this.userStore) {
                        this.error = 'You must be logged in to view availabilities.';
                        return;
                    }

                    if (!this.userStore.user.id) {
                        this.error = 'Cannot determine user id.';
                        return;
                    }

                    const resp = await api.get(`/allavailability/${this.userStore.user.id}`);
                    this.availabilities = Array.isArray(resp) ? resp : (resp ? [resp] : []);
                } catch (err) {
                    this.successMessage = err.message;
                    console.error('error:', err);
                } finally {
                    this.isLoading = false;
                    this.organizeByWeek();
                }
            },

            organizeByWeek() {
                const week = [];
                const today = new Date();
                
                for (let i = 1; i <= 7; i++) {
                    const date = new Date(today);
                    date.setDate(date.getDate() + i);
                    const dateStr = this.formatDateForAPI(date);
                    const formattedDate = date.getFullYear() + '-' + 
                        String(date.getMonth() + 1).padStart(2, '0') + '-' +
                        String(date.getDate()).padStart(2, '0');// 0 (Sun) - 6 (Sat)

                    const dayAvailabilities = this.availabilities
                        .filter(av => av.date === formattedDate)
                        .sort((a, b) => a.start_time.localeCompare(b.start_time));

                    week.push({
                        date: dateStr,
                        availabilities: dayAvailabilities,
                    });
                }
                this.upcomingWeek = week;
            },

            validateForm() {
                this.formErrors = [];
                
    
                if (this.formData.start_time) {
                    const [st_hours, st_minutes] = this.formData.start_time.split(':').map(Number);
                    const [et_hours, et_minutes] = this.formData.end_time.split(':').map(Number);
                
                    // End time > Start time
                    if (et_hours < st_hours || (et_hours === st_hours && et_minutes <= st_minutes)) {
                        this.formErrors.push('End time must be after start time');
                    }

                    // End Time - Start time < 14 hours
                    if (et_hours - st_hours > 14 || (et_hours - st_hours === 14 && et_minutes > st_minutes)) {
                        this.formErrors.push('Time slot cannot be longer than 14 hours');
                    }
                }
                
                // Start time - End time = order of 30 minuites
                const end_minutes = new Date(`1970-01-01T${this.formData.end_time}`).getMinutes();
                const start_minutes = new Date(`1970-01-01T${this.formData.start_time}`).getMinutes();

                if ((end_minutes !== 0 && end_minutes !== 30) || (start_minutes !== 0 && start_minutes !== 30)) {
                    this.formErrors.push("Time must be in 30-minute intervals");
                }

                if (!this.editingSlot) {
                    if (this.formData.date && this.formData.time) {
                        const duplicate = this.availabilities.find(
                            av => av.date === this.formData.date && av.start_time === this.formData.start_time + ':00'
                        );
                        if (duplicate) {
                            this.formErrors.push('This time slot already exists');
                        }
                    }
                    for (const aval of this.availabilities) {
                        if (aval.date === this.formData.date && (aval.start_time === this.formData.start_time + ':00' && aval.end_time === this.formData.end_time + ':00')) {
                            this.formErrors.push('This time slot already exists');
                        }
                        else if (aval.date === this.formData.date &&( 
                            (this.formData.end_time + ':00' > aval.start_time && this.formData.end_time + ':00' < aval.end_time)
                            ||
                            (this.formData.start_time  + ':00'  > aval.start_time && this.formData.start_time + ':00' < aval.end_time))) {
                            this.formErrors.push('This time slot overlaps with an existing one');
                        }
                    }
                }
                return this.formErrors.length === 0;
            },

            async submitForm() {
                if (!this.validateForm()) {
                    return;
                }
                
                this.isSubmitting = true;
                this.error = '';
                
                try {
                    const aval_payload = {
                        doctor_id: this.userStore.user.id,
                        date: this.formData.date,
                        start_time: this.formData.start_time + ':00', // Convert to HH:MM:SS
                        end_time: this.formData.end_time + ':00', // Convert to HH:MM:SS
                    };
                    
                    if (this.editingSlot) {
                        const start_time = this.editingSlot.start_time;
                        const end_time = this.editingSlot.end_time;
                        for (const appointment of this.appointments) {
                            if (appointment.appointment_time > end_time) {
                                const apt_payload = {
                                    "status": "Cancelled"
                                }
                                await api.patch(`/appointments/${appointment.ap_id}`, apt_payload);
                            }
                        }
                        await api.put(`/doctoravailability/${this.editingSlot.dav_id}`, aval_payload);
                        this.successMessage = 'Availability updated successfully!';
                    } else {
                        // Create new availability
                        await api.post('/allavailability', aval_payload);
                        this.successMessage = 'Availability added successfully!';
                    }
                    
                    this.closeModal();
                    await this.fetchAvailabilities();
                    await this.fetchDoctorAppointments();
                    
                    // Auto-hide success message after 3 seconds
                    setTimeout(() => {
                        this.successMessage = '';
                    }, 3000);
                } catch (err) {
                    console.error('Error:', err);
                } finally {
                    this.isSubmitting = false;
                }
            },

            async deleteAvailability() {
                if (!this.slotToDelete) return;
                
                this.isSubmitting = true;
                this.error = '';
                
                try {
                    const start_time = this.slotToDelete.start_time;
                    const end_time = this.slotToDelete.end_time;
                    for (const appointment of this.appointments) {
                        if (appointment.appointment_time > end_time) {
                            const apt_payload = {
                                "status": "Cancelled"
                            }
                            await api.patch(`/appointments/${appointment.ap_id}`, apt_payload);
                        }
                    }
                    await api.delete(`/doctoravailability/${this.slotToDelete.dav_id}`);
                    this.successMessage = 'Availability deleted successfully!';
                    this.closeDeleteModal();
                    await this.fetchAvailabilities();
                    await this.fetchDoctorAppointments();
                    
                    // Auto-hide success message after 3 seconds
                    setTimeout(() => {
                        this.successMessage = '';
                    }, 3000);
                } catch (err) {
                    this.error = err.message ;
                    console.error('Error:', errror);
                } finally {
                    this.isSubmitting = false;
                }
            },

            openAddModalForDate(date) {
                this.editingSlot = null;
                this.formData = { date: date, time: '' };
                this.formErrors = [];
                this.availabilityModal.show();
            },

            openEditModal(slot) {
                this.editingSlot = slot;
                this.formData = {
                    date: slot.date,
                    start_time: slot.start_time.substring(0, 5), // Convert HH:MM:SS to HH:MM
                    end_time: slot.end_time.substring(0, 5), // Convert HH:MM:SS to HH:MM
                };
                this.formErrors = [];
                this.availabilityModal.show();
            },

            closeModal() {
                this.availabilityModal.hide();
                this.editingSlot = null;
                this.formData = { date: '', time: '' };
                this.formErrors = [];
            },

            confirmDelete(slot) {
                this.slotToDelete = slot;
                this.deleteConfirmModal.show();
            },

            closeDeleteModal() {
                this.deleteConfirmModal.hide();
                this.slotToDelete = null;
            },

            formatDateForAPI(date) {
                if (typeof date === 'string') {
                    return date;
                }
                const year = date.getFullYear();
                const month = String(date.getMonth() + 1).padStart(2, '0');
                const day = String(date.getDate()).padStart(2, '0');
                return `${year}-${month}-${day}`;
            },

            formatDayName(dateStr) {
                const date = new Date(dateStr + 'T00:00:00');
                return date.toLocaleDateString('en-US', { weekday: 'long' });
            },


            formatDateShort(dateStr) {
                const date = new Date(dateStr + 'T00:00:00');
                return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
            },

            
            formatDateLong(dateStr) {
                const date = new Date(dateStr + 'T00:00:00');
                return date.toLocaleDateString('en-US', { 
                    weekday: 'long',
                    year: 'numeric', 
                    month: 'long', 
                    day: 'numeric' 
                });
            },

            formatTime(timeStr) {
                if (!timeStr) return '';
                return timeStr.substring(0, 5); // Remove seconds
            },

            getTommDate() {
                const tomm = new Date();
                tomm.setDate(tomm.getDate() + 1);
                return this.formatDateForAPI(tomm);
            },


            getMaxDate() {
                const maxDate = new Date();
                maxDate.setDate(maxDate.getDate() + 7);
                return this.formatDateForAPI(maxDate);
            },
        },

        mounted() {
            // Initialize Bootstrap modals
            this.availabilityModal = new Modal(document.getElementById('availabilityModal'));
            this.deleteConfirmModal = new Modal(document.getElementById('deleteConfirmModal'));
            
            // Initialize user store and fetch data
            this.userStore = useUserStore();
            this.fetchAvailabilities();
            this.fetchDoctorAppointments();
        }
    };
</script>

<style scoped>
/* Container and Layout */
.container-fluid {
    background-color: #f8f9fa;
    min-height: 100vh;
}

/* Header Section */
h1 {
    color: #2c3e50;
    font-weight: 700;
    font-size: 2.5rem;
}

.text-muted {
    color: #6c757d !important;
    font-size: 1.1rem;
}

/* Buttons */
.btn-primary {
    background-color: #007bff;
    border-color: #007bff;
    transition: all 0.3s ease;
}

.btn-primary:hover {
    background-color: #0056b3;
    border-color: #0056b3;
    box-shadow: 0 4px 12px rgba(0, 123, 255, 0.4);
}

.btn-outline-primary:hover {
    background-color: #007bff;
    color: white;
}

.btn-outline-info {
    color: #17a2b8;
    border-color: #17a2b8;
}

.btn-outline-info:hover {
    background-color: #17a2b8;
    border-color: #17a2b8;
}

.btn-outline-danger {
    color: #dc3545;
    border-color: #dc3545;
}

.btn-outline-danger:hover {
    background-color: #dc3545;
    border-color: #dc3545;
}

/* Alert Messages */
.alert {
    border-radius: 0.5rem;
    border-left: 4px solid;
    animation: slideDown 0.3s ease;
}

.alert-danger {
    border-left-color: #dc3545;
    background-color: #f8d7da;
    color: #721c24;
}

.alert-success {
    border-left-color: #28a745;
    background-color: #d4edda;
    color: #155724;
}

.alert-warning {
    border-left-color: #ffc107;
    background-color: #fff3cd;
    color: #856404;
}

.alert-info {
    border-left-color: #17a2b8;
    background-color: #d1ecf1;
    color: #0c5460;
}

@keyframes slideDown {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}


/* Cards */
.card {
    border: none;
    border-radius: 0.75rem;
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    background-color: white;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15) !important;
}

.card-header {
    background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
    border: none;
    padding: 1.25rem;
}

.card-header h5 {
    font-weight: 600;
    font-size: 1.25rem;
    margin-bottom: 0.5rem;
}

.card-header small {
    font-size: 0.85rem;
    display: block;
}

.card-body {
    padding: 1.5rem;
    background-color: #fff;
}

.card-footer {
    border-top: 1px solid #e9ecef;
    padding: 1rem;
    background-color: #f8f9fa;
}

.card-footer .btn {
    font-weight: 500;
}

/* Time Slots List */
.list-group-flush > div {
    padding: 0.75rem 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #e9ecef;
}

.list-group-flush > div:last-child {
    border-bottom: none;
}

.list-group-flush p {
    font-size: 1.1rem;
    margin-bottom: 0;
}

.list-group-flush small {
    font-size: 0.85rem;
}

/* Button Groups */
.btn-group-sm .btn {
    padding: 0.4rem 0.6rem;
    font-size: 0.85rem;
}

/* Modal Styling */
.modal-header {
    background-color: #f8f9fa;
    border-bottom: 1px solid #dee2e6;
}

.modal-header .modal-title {
    font-weight: 600;
    color: #2c3e50;
}

.modal-body {
    padding: 1.5rem;
}

.modal-footer {
    background-color: #f8f9fa;
    border-top: 1px solid #dee2e6;
}

/* Form Elements */
.form-label {
    color: #2c3e50;
    margin-bottom: 0.5rem;
}

.form-control,
.form-select {
    border: 1px solid #dee2e6;
    border-radius: 0.375rem;
    padding: 0.75rem;
    font-size: 1rem;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.form-control:focus,
.form-select:focus {
    border-color: #007bff;
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.form-control:invalid,
.form-select:invalid {
    border-color: #dc3545;
}

.form-control:invalid:focus,
.form-select:invalid:focus {
    border-color: #dc3545;
    box-shadow: 0 0 0 0.2rem rgba(220, 53, 69, 0.25);
}

/* Delete Confirmation Modal */
.modal-header.border-danger {
    border-bottom: 2px solid #dc3545 !important;
}

.text-danger {
    color: #dc3545 !important;
}

/* Responsive Design */
@media (max-width: 768px) {
    h1 {
        font-size: 1.75rem;
    }

    .d-flex.justify-content-between {
        flex-direction: column;
        gap: 1rem;
    }

    .btn-lg {
        width: 100%;
    }

    .card-body {
        padding: 1rem;
    }

    .list-group-flush > div {
        flex-direction: column;
        align-items: flex-start;
    }

    .btn-group {
        align-self: flex-end;
        margin-top: 0.5rem;
    }
}

@media (max-width: 576px) {
    .row.g-3 {
        gap: 0.75rem !important;
    }

    .modal-dialog {
        margin: 0.5rem;
    }

    .card {
        margin-bottom: 0.5rem;
    }

    .btn {
        padding: 0.5rem 1rem;
        font-size: 0.875rem;
    }
}

/* Empty State */
.text-center.text-muted {
    padding: 2rem;
    font-size: 1rem;
}

/* Animation for modal appearance */
.modal.fade .modal-dialog {
    transition: transform 0.3s ease, opacity 0.3s ease;
}

.modal.show .modal-dialog {
    transform: none;
}
</style>