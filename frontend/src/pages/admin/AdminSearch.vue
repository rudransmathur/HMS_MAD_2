<template>
	<div class="container mt-4">
		<div class="d-flex justify-content-between align-items-center mb-3">
			<div>
				<h2 class="h4">Admin — Search and Edit Users</h2>
				<p class="text-muted mb-0">Search users by name or role. Edit/Delete allowed only for doctors.</p>
			</div>
		</div>

		<div class="row g-2 mb-3">
			<div class="col-md-6">
				<input v-model="q" class="form-control" placeholder="Search by name or username" />
			</div>
			<div class="col-md-3">
				<select v-model="roleFilter" class="form-select">
					<option value="all">All roles</option>
					<option value="doctor">Doctor</option>
					<option value="patient">Patient</option>
					<option value="other">Other</option>
				</select>
			</div>
			<div class="col-md-3 text-end">
				<small class="text-muted">Total: {{ filteredUsers.length }}</small>
			</div>
		</div>

		<div v-if="loading" class="text-center py-5">
			<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>
		</div>

		<div v-if="error" class="alert alert-danger">{{ error }}</div>

		<div v-if="!loading && filteredUsers.length === 0" class="alert alert-info">No users found.</div>

		<div v-if="filteredUsers.length > 0" class="table-responsive">
			<table class="table table-striped table-hover">
				<thead>
					<tr>
						<th>User ID</th>
						<th>Username</th>
						<th>Full Name</th>
						<th>Phone</th>
						<th>Email</th>
						<th>Active</th>
						<th>Action</th>
					</tr>
				</thead>
				<tbody>
					<tr v-for="u in filteredUsers" :key="u.user_id || u.id">
						<td>{{ u.user_id || u.id }}</td>
						<td>{{ u.username }}</td>
						<td>{{ u.fullname }}</td>
						<td>{{ u.phone }}</td>
						<td>{{ u.email }}</td>
						<td>
							<span v-if="u.active" class="badge bg-success">Yes</span>
							<span v-else class="badge bg-secondary">No</span>
						</td>
						<td class="text-end">
							<button class="btn btn-sm btn-outline-primary me-2" @click="openEdit(u)" :disabled="!isDoctor(u)">Edit</button>
							<button class="btn btn-sm btn-outline-danger" @click="confirmDelete(u)" :disabled="!isDoctor(u)">Delete</button>
						</td>
					</tr>
				</tbody>
			</table>
		</div>

		<!-- Edit modal -->
		<div v-if="editing" class="modal-backdrop">
			<div class="modal d-block" tabindex="-1" role="dialog">
				<div class="modal-dialog modal-lg" role="document">
					<div class="modal-content">
						<div class="modal-header">
							<h5 class="modal-title">Edit Doctor — {{ editForm.username }}</h5>
							<button type="button" class="btn-close" @click="closeEdit"></button>
						</div>
						<div class="modal-body">
							<div v-if="editError" class="alert alert-danger">{{ editError }}</div>
							<div class="row g-3">
								<div class="col-md-6">
									<label class="form-label">Full name</label>
									<input class="form-control" v-model="editForm.fullname" />
								</div>
								<div class="col-md-6">
									<label class="form-label">Email</label>
									<input class="form-control" v-model="editForm.email" type="email" />
								</div>
								<div class="col-md-6">
									<label class="form-label">Phone</label>
									<input class="form-control" v-model="editForm.phone" />
								</div>
								<div class="col-md-6">
									<label class="form-label">Active</label>
									<div><input type="checkbox" v-model="editForm.active" /> <span class="ms-2">Active</span></div>
								</div>
							</div>
						</div>
						<div class="modal-footer">
							<button class="btn btn-secondary" @click="closeEdit">Cancel</button>
							<button class="btn btn-primary" @click="saveEdit" :disabled="saving">Save</button>
						</div>
					</div>
				</div>
			</div>
		</div>

	</div>
</template>

<script>
import api from '@/utils/api';

export default {
	name: 'AdminSearch',
	data() {
		return {
			users: [],
			doctors: [],
			loading: false,
			error: '',
			q: '',
			roleFilter: 'all',
			editing: false,
			editForm: null,
			saving: false,
			editError: ''
		};
	},
	computed: {
		doctorIds() {
			return new Set((this.doctors || []).map(d => d.user_id || d.userId || d.id));
		},
		usersWithRole() {
			return (this.users || []).map(u => {
				const id = u.user_id || u.id;
				const role = this.doctorIds.has(id) ? 'doctor' : 'patient';
				return { ...u, role };
			});
		},
		filteredUsers() {
			const q = (this.q || '').toLowerCase().trim();
			return this.usersWithRole.filter(u => {
				if (this.roleFilter !== 'all' && u.role !== this.roleFilter) return false;
				if (!q) return true;
				return (u.fullname || '').toLowerCase().includes(q) || (u.username || '').toLowerCase().includes(q);
			});
		}
	},
	created() {
		this.loadAll();
	},
	methods: {
		async loadAll() {
			try {
				this.loading = true;
				this.error = '';
				const [usersResp, doctorsResp] = await Promise.all([api.get('/users'), api.get('/doctors')]);
				this.users = Array.isArray(usersResp) ? usersResp : (usersResp.data || []);
				this.doctors = Array.isArray(doctorsResp) ? doctorsResp : (doctorsResp.data || []);
			} catch (e) {
				console.error(e);
				this.error = e.message || 'Failed to load users.';
			} finally {
				this.loading = false;
			}
		},
		reload() {
			this.loadAll();
		},
		isDoctor(u) {
			const id = u.user_id || u.id;
			return this.doctorIds.has(id);
		},
		openEdit(u) {
			if (!this.isDoctor(u)) return;
			this.editForm = { ...u };
			this.editing = true;
			this.editError = '';
		},
		closeEdit() {
			this.editing = false;
			this.editForm = null;
		},
		async saveEdit() {
			try {
				this.saving = true;
				this.editError = '';
				const id = this.editForm.user_id || this.editForm.id;
				const payload = {
					username: this.editForm.username,
					fullname: this.editForm.fullname,
					phone: this.editForm.phone,
					email: this.editForm.email,
					active: this.editForm.active
				};
				await api.patch(`/user/${id}`, payload);
				await this.loadAll();
				this.closeEdit();
			} catch (e) {
				console.error(e);
				this.editError = e.message || 'Failed to save.';
			} finally {
				this.saving = false;
			}
		},
		confirmDelete(u) {
			if (!this.isDoctor(u)) return;
			if (!window.confirm(`Delete doctor ${u.fullname || u.username}? This action cannot be undone.`)) return;
			this.deleteUser(u);
		},
		async deleteUser(u) {
			try {
				const id = u.user_id || u.id;
				await api.delete(`/user/${id}`);
				await this.loadAll();
			} catch (e) {
				console.error(e);
				this.error = e.message || 'Failed to delete user.';
			}
		}
	}
};
</script>

<style scoped>
.modal-backdrop { background: rgba(0,0,0,0.4); position: fixed; inset: 0; display:flex; align-items:center; justify-content:center; z-index: 1050; }
.modal { z-index: 1060; }
</style>