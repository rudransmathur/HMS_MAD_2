<template>
    <div class="container mt-4">
        <div class="mb-5">
            <h1 class="display-6 fw-bold text-primary">Welcome Admin:</h1>
        </div>
        <div class="d-flex justify-content-between align-items-center mb-3">
            <div>
                <h2 class="h4">Admin — Requests</h2>
                <p class="text-muted mb-0">Pending profile update requests from users/doctors.</p>
            </div>
        </div>

        <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>
        </div>

        <div v-if="error" class="alert alert-danger">{{ error }}</div>

        <div v-if="requests && requests.length === 0" class="alert alert-info">No requests found.</div>

        <div v-if="requests && requests.length > 0">
            <div class="mb-4">
                <h5 class="mb-2">Pending (Created)</h5>
                <div v-if="createdRequests.length === 0" class="alert alert-info">No pending requests.</div>
                <div v-else class="table-responsive">
                    <table class="table table-striped table-hover">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Type</th>
                                <th>Status</th>
                                <th>Username</th>
                                <th>Name</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="r in createdRequests" :key="r.r_id">
                                <td>{{ r.r_id }}</td>
                                <td>{{ r.type }}</td>
                                <td>{{ r.status }}</td>
                                <td>{{ r.username }}</td>
                                <td>{{ r.fullname }}</td>
                                <td class="text-end">
                                    <button class="btn btn-sm btn-outline-primary me-2" @click="pendingviewRequest(r)">View</button>
                                    <button class="btn btn-sm btn-outline-primary me-2" @click="approveRequest(r)">Approve</button>
                                    <button class="btn btn-sm btn-outline-primary me-2" @click="rejectRequest(r)">Reject</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div v-if="pendingselected" class="card mt-4">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <h5 class="card-title">Request : {{ pendingselected.r_id }} — {{ pendingselected.type }}</h5>
                            <p class="text-muted mb-1">Status: <strong>{{ pendingselected.status }}</strong></p>
                            <p class="text-muted mb-0">User ID: {{ pendingselected.user_id }}</p>
                        </div>
                        <div>
                            <button class="btn btn-sm btn-secondary" @click="pendingselected = null">Close</button>
                        </div>
                    </div>

                    <hr />

                    <div>
                        <h6>Payload</h6>
                        <pre class="small bg-light p-3" style="white-space:pre-wrap;">{{ JSON.stringify(pendingselected.data, null, 2) }}</pre>
                    </div>
                </div>
            </div>

            <div class="mb-4">
                <h5 class="mb-2">Processed (Approved / Rejected)</h5>
                <div v-if="processedRequests.length === 0" class="alert alert-info">No processed requests.</div>
                <div v-else class="table-responsive">
                    <table class="table table-striped table-hover">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Type</th>
                                <th>Status</th>
                                <th>Username</th>
                                <th>Name</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="r in processedRequests" :key="r.r_id">
                                <td>{{ r.r_id }}</td>
                                <td>{{ r.type }}</td>
                                <td>{{ r.status }}</td>
                                <td>{{ r.username }}</td>
                                <td>{{ r.fullname }}</td>
                                <td class="text-end">
                                    <button class="btn btn-sm btn-outline-primary me-2" @click="processedviewRequest(r)">View</button>
                                    <button class="btn btn-sm btn-outline-primary me-2" @click="undoRequest(r)">Undo</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <div v-if="processedselected" class="card mt-4">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-start">
                    <div>
                        <h5 class="card-title">Request : {{ processedselected.r_id }} — {{ processedselected.type }}</h5>
                        <p class="text-muted mb-1">Status: <strong>{{ processedselected.status }}</strong></p>
                        <p class="text-muted mb-0">User ID: {{ processedselected.user_id }}</p>
                    </div>
                    <div>
                        <button class="btn btn-sm btn-secondary" @click="processedselected = null">Close</button>
                    </div>
                </div>

                <hr />

                <div>
                    <h6>Payload</h6>
                    <pre class="small bg-light p-3" style="white-space:pre-wrap;">{{ JSON.stringify(processedselected.data, null, 2) }}</pre>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import api from '@/utils/api';

export default {
    name: 'AdminDashboard',
    data() {
        return {
            requests: null,
            loading: false,
            error: '',
            pendingselected: null,
            processedselected: null
        };
    },
    created() {
        this.fetchRequests();
    },
    computed: {
        createdRequests() {
            if (!this.requests) return [];
            return this.requests.filter(r => r.status === 'created');
        },
        processedRequests() {
            if (!this.requests) return [];
            return this.requests.filter(r => r.status !== 'created');
        }
    },
    methods: {
        async fetchRequests() {
            try {
                this.loading = true;
                this.error = '';
                const resp = await api.get('/requests');
                this.requests = Array.isArray(resp) ? resp : (resp.data || []);
            } catch (err) {
                console.error(err);
                this.error = err.message || 'Failed to load requests.';
            } finally {
                this.loading = false;
            }
        },
        pendingviewRequest(r) {
            try {
                if (typeof r.data === 'string') {
                    r.data = JSON.parse(r.data);
                }
            } catch (e) {
            }
            this.pendingselected = r;
            this.$nextTick(() => {
                const el = this.$el.querySelector('.card');
                if (el) el.scrollIntoView({ behavior: 'smooth' });
            });
        },
        processedviewRequest(r) {
            try {
                if (typeof r.data === 'string') {
                    r.data = JSON.parse(r.data);
                }
            } catch (e) {
            }
            this.processedselected = r;
            this.$nextTick(() => {
                const el = this.$el.querySelector('.card');
                if (el) el.scrollIntoView({ behavior: 'smooth' });
            });
        },
        async approveRequest(r){
            try {
                const payload = {
                    r_id: r.r_id,
                    data: r.data,
                    status: 'approved',
                    type: r.type,
                    user_id: r.user_id
                };
                await api.patch(`/requests/${r.r_id}`, payload);
                await this.fetchRequests();
                this.pendingselected = null;
            } catch (e) {
                this.error = e.message;
                console.error("error:", e);
            }
        },
        async rejectRequest(r){
            try {
                const payload = {
                    r_id: r.r_id,
                    data: r.data,
                    status: 'rejected',
                    type: r.type,
                    user_id: r.user_id
                };
                await api.patch(`/requests/${r.r_id}`, payload);
                await this.fetchRequests();
                this.pendingselected = null;
            } catch (e) {
                this.error = e.message;
                console.error("error:", e);
            }
        },
        async undoRequest(r){
            try {
                const payload = {
                    r_id: r.r_id,
                    data: r.data,
                    status: 'created',
                    type: r.type,
                    user_id: r.user_id
                };
                // fix: correct URL must not contain a space
                await api.patch(`/requests/${r.r_id}`, payload);
                await this.fetchRequests();
                this.processedselected = null;
            } catch (e) {
                this.error = e.message;
                console.error("error:", e);
            }
        }
    }
};
</script>

<style scoped>
pre { font-size: .9rem; }
</style>