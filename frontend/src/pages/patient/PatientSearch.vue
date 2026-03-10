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
                            <option value="">All Departments</option>
                            <option v-for="dept in departments" :key="dept" :value="dept">
                                {{ dept }}
                            </option>
                        </select>
                    </div>
                </div>

                <!-- Results Summary -->
                <div class="mt-3 text-muted">
                    <small>Showing {{ filteredDoctors.length }} doctor(s)</small>
                </div>
            </div>
        </div>

        <!-- No Results Message -->
        <div v-if="filteredDoctors.length === 0" class="alert alert-info text-center py-5">
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
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="doctor in filteredDoctors" :key="doctor.doctor_id">
                            <td class="fw-semibold">Dr. {{ doctor.fullname }}</td>
                            <td>{{ doctor.department_name }}</td>
                            <td>{{ doctor.specialization }}</td>
                            <td><span class="badge bg-success">₹{{ doctor.consultation_fee }}</span></td>
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
        filteredDoctors() {
            return this.doctors
                .filter(doctor => {
                    // Filter by doctor name
                    if (this.searchQuery && !doctor.fullname.toLowerCase().includes(this.searchQuery.toLowerCase())) {
                        return false;
                    }
                    // Filter by department
                    if (this.selectedDepartment && doctor.department_name !== this.selectedDepartment) {
                        return false;
                    }
                    // Filter by day
                    if (this.selectedDay !== "" && doctor.day_of_week !== parseInt(this.selectedDay)) {
                        return false;
                    }
                    // Filter by time (available after)
                    if (this.selectedTime) {
                        if (slot.start_time < this.selectedTime) {
                            return false;
                        }
                    }
                    return true;
                });
        }
    },
    async created() {
        this.userStore = useUserStore();
        await this.fetchDoctors();
        await this.fetchAvailabilities();
    },
    methods: {
        async fetchDoctors() {
            try {
                const response = await api.get('/doctors');
                console.log("Fetched doctors:", response);
                // Filter to only get valid, active doctors (use doctor_id instead of user_id)
                this.doctors = (Array.isArray(response) ? response : [response])
                    .filter(doctor => doctor && doctor.doctor_id && doctor.fullname && doctor.is_active !== false);
            } catch (err) {
                this.error = "Failed to fetch doctors: " + (err.message || "Unknown error");
                console.error("Failed to fetch doctors:", err);
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