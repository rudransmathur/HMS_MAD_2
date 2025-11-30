<template>
    <div class="container mt-5">
        <!-- Header -->
        <div class="mb-5">
            <h1 class="display-5 fw-bold text-primary">Find Available Doctors</h1>
            <p class="text-muted">Search and filter doctors by specialty, availability, and time</p>
        </div>

        <!-- Error Alert -->
        <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
            {{ error }}
            <button type="button" class="btn-close" @click="error = ''"></button>
        </div>

        <!-- Search Filters -->
        <div class="card shadow-sm mb-5">
            <div class="card-header bg-light">
                <h5 class="mb-0"><i class="bi bi-funnel"></i> Search Filters</h5>
            </div>
            <div class="card-body">
                <div class="row g-3">
                    <!-- Name Search -->
                    <div class="col-md-3">
                        <label class="form-label fw-semibold">Doctor Name</label>
                        <input 
                            v-model="searchQuery" 
                            type="text" 
                            class="form-control" 
                            placeholder="Search by name..."
                        >
                    </div>

                    <!-- Department Filter -->
                    <div class="col-md-3">
                        <label class="form-label fw-semibold">Department</label>
                        <select v-model="selectedDepartment" class="form-select">
                            <option value="">-- All Departments --</option>
                            <option v-for="dept in departments" :key="dept" :value="dept">
                                {{ dept }}
                            </option>
                        </select>
                    </div>

                    <!-- Day Filter -->
                    <div class="col-md-3">
                        <label class="form-label fw-semibold">Availability Day</label>
                        <select v-model="selectedDay" class="form-select">
                            <option value="">-- All Days --</option>
                            <option value="0">Monday</option>
                            <option value="1">Tuesday</option>
                            <option value="2">Wednesday</option>
                            <option value="3">Thursday</option>
                            <option value="4">Friday</option>
                            <option value="5">Saturday</option>
                            <option value="6">Sunday</option>
                        </select>
                    </div>

                    <!-- Time Filter -->
                    <div class="col-md-3">
                        <label class="form-label fw-semibold">Available After (Time)</label>
                        <input 
                            v-model="selectedTime" 
                            type="time" 
                            class="form-control"
                        >
                    </div>
                </div>

                <!-- Results Summary -->
                <div class="mt-3 text-muted">
                    <small>Showing {{ filteredAvailabilities.length }} availability slot(s)</small>
                </div>
            </div>
        </div>

        <!-- No Results Message -->
        <div v-if="filteredAvailabilities.length === 0" class="alert alert-info text-center py-5">
            <i class="bi bi-search" style="font-size: 3rem; color: #0d6efd;"></i>
            <p class="mt-3 mb-0">No doctors found matching your criteria. Try adjusting your filters.</p>
        </div>

        <!-- Doctors Table -->
        <div v-else class="card shadow-sm">
            <div class="table-responsive">
                <table class="table table-hover mb-0">
                    <thead class="table-light">
                        <tr>
                            <th><i class="bi bi-person-fill"></i> Doctor Name</th>
                            <th><i class="bi bi-building"></i> Department</th>
                            <th><i class="bi bi-star"></i> Specialization</th>
                            <th><i class="bi bi-cash-coin"></i> Consultation Fee</th>
                            <th><i class="bi bi-calendar-event"></i> Day</th>
                            <th><i class="bi bi-clock"></i> Time</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="slot in filteredAvailabilities" :key="`${slot.doctor_id}-${slot.dav_id}`">
                            <td class="fw-semibold">Dr. {{ slot.doctor_fullname }}</td>
                            <td>{{ slot.department_name }}</td>
                            <td>{{ slot.specialization }}</td>
                            <td><span class="badge bg-success">₹{{ slot.consultation_fee }}</span></td>
                            <td>{{ getDayName(slot.day_of_week) }}</td>
                            <td>{{ formatTime(slot.start_time) }} - {{ formatTime(slot.end_time) }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
import api from '@/utils/api';
import useUserStore from '@/stores/user';

const DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

export default {
    name: "SearchPage",
    data() {
        return {
            error: "",
            doctors: [],
            availabilities: [],
            searchQuery: "",
            selectedDepartment: "",
            selectedDay: "",
            selectedTime: "",
            userStore: null
        };
    },
    computed: {
        departments() {
            return [...new Set(this.doctors.map(d => d.department_name).filter(Boolean))].sort();
        },
        filteredAvailabilities() {
            return this.availabilities
                .filter(slot => {
                    // Filter by doctor name
                    if (this.searchQuery && !slot.doctor_fullname.toLowerCase().includes(this.searchQuery.toLowerCase())) {
                        return false;
                    }
                    // Filter by department
                    if (this.selectedDepartment && slot.department_name !== this.selectedDepartment) {
                        return false;
                    }
                    // Filter by day
                    if (this.selectedDay !== "" && slot.day_of_week !== parseInt(this.selectedDay)) {
                        return false;
                    }
                    // Filter by time (available after)
                    if (this.selectedTime) {
                        if (slot.start_time < this.selectedTime) {
                            return false;
                        }
                    }
                    return true;
                })
                .sort((a, b) => {
                    // Sort by day, then by start time
                    if (a.day_of_week !== b.day_of_week) {
                        return a.day_of_week - b.day_of_week;
                    }
                    return a.start_time.localeCompare(b.start_time);
                });
        }
    },
    created() {
        this.userStore = useUserStore();
        this.fetchDoctors();
        this.fetchAvailabilities();
    },
    methods: {
        async fetchDoctors() {
            try {
                const response = await api.get('/doctors');
                console.log("Fetched doctors:", response);
                // Filter to only get valid, active doctors
                this.doctors = (Array.isArray(response) ? response : [response])
                    .filter(doctor => doctor && doctor.user_id && doctor.fullname && doctor.is_active !== false);
            } catch (err) {
                this.error = "Failed to fetch doctors: " + (err.message || "Unknown error");
                console.error("Failed to fetch doctors:", err);
            }
        },
        async fetchAvailabilities() {
            try {
                const response = await api.get('/doctoravailability');
                console.log("Fetched availabilities:", response);
                const availsList = Array.isArray(response) ? response : (response ? [response] : []);
                
                // Enrich availability data with doctor info
                this.availabilities = availsList.map(avail => {
                    const doctor = this.doctors.find(d => d.doctor_id === avail.doctor_id);
                    return {
                        ...avail,
                        doctor_fullname: doctor?.fullname || 'Unknown',
                        department_name: doctor?.department_name || 'N/A',
                        specialization: doctor?.specialization || 'N/A',
                        consultation_fee: doctor?.consultation_fee || 0
                    };
                });
            } catch (err) {
                this.error = "Failed to fetch availabilities: " + (err.message || "Unknown error");
                console.error("Failed to fetch availabilities:", err);
            }
        },
        getDayName(dayIndex) {
            return DAYS[dayIndex] || 'Unknown';
        },
        formatTime(timeStr) {
            if (!timeStr) return '—';
            try {
                const [hours, minutes] = timeStr.split(':');
                const hour = parseInt(hours);
                const meridiem = hour >= 12 ? 'PM' : 'AM';
                const displayHour = hour % 12 || 12;
                return `${displayHour}:${minutes} ${meridiem}`;
            } catch (e) {
                return timeStr;
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
    border-bottom: 1px solid #dee2e6;
}

.table-hover tbody tr:hover {
    background-color: #f8f9fa;
}

h1 {
    color: #0d6efd;
}

.badge {
    padding: 0.5rem 0.75rem;
    font-size: 0.875rem;
}

.btn-sm {
    padding: 0.375rem 0.75rem;
}

.form-label {
    color: #333;
    margin-bottom: 0.5rem;
}

.bi {
    margin-right: 0.5rem;
}
</style>