<template>
	<div class="container mt-5">
		<div class="row mb-4">
			<div class="col">
				<h1 class="h3">Doctor Profile</h1>
				<p class="text-muted">View and update your public and professional details.</p>
			</div>
			<div class="col-auto">
				<button class="btn btn-secondary" @click="reload">Reload</button>
			</div>
		</div>

		<div v-if="loading" class="text-center py-5">
			<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>
		</div>

		<div v-if="error" class="alert alert-danger">{{ error }}</div>
		<div v-if="successMessage" class="alert alert-success">{{ successMessage }}</div>

		<div v-if="profile" class="card shadow-sm">
			<div class="card-body">
				<form @submit.prevent="saveProfile">
					<div class="row g-3">
						<div class="col-md-6">
							<label class="form-label">Username</label>
							<input class="form-control" v-model="form.username" readonly />
						</div>
						<div class="col-md-6">
							<label class="form-label">Full Name</label>
							<input class="form-control" v-model="form.fullname" />
						</div>

						<div class="col-md-4">
							<label class="form-label">Email</label>
							<input class="form-control" v-model="form.email" type="email" />
						</div>
						<div class="col-md-4">
							<label class="form-label">Phone</label>
							<input class="form-control" v-model="form.phone" type="tel" />
						</div>
						<div class="col-md-4 d-flex align-items-center">
							<div>
								<label class="form-label">Active</label>
								<div>
									<input type="checkbox" v-model="form.active" /> <span class="ms-2">Account active</span>
								</div>
							</div>
						</div>  

						<hr class="my-3" />

						<div class="col-md-6">
							<label class="form-label">Department (id or name)</label>
							<input class="form-control" v-model="form.department_name" />
						</div>
						<div class="col-md-6">
							<label class="form-label">Qualification</label>
							<input class="form-control" v-model="form.qualification" />
						</div>

						<div class="col-md-4">
							<label class="form-label">Experience (years)</label>
							<input class="form-control" v-model.number="form.experience_years" type="number" min="0" />
						</div>
						<div class="col-md-4">
							<label class="form-label">Specialization</label>
							<input class="form-control" v-model="form.specialization" />
						</div>
						<div class="col-md-4">
							<label class="form-label">Consultation Fee</label>
							<input class="form-control" v-model.number="form.consultation_fee" type="number" step="0.01" />
						</div>

						<div class="col-12 mt-3 d-flex gap-2">
							<button class="btn btn-primary" :disabled="isSaving">Save</button>
							<button type="button" class="btn btn-outline-secondary" @click="cancel">Cancel</button>
						</div>
					</div>
				</form>
			</div>
		</div>
	</div>
</template>

<script>
import api from '@/utils/api';
import useUserStore from '@/stores/user';

export default {
	name: 'DoctorProfile',
	data() {
		return {
			profile: null,
			form: null,
			loading: false,
			isSaving: false,
			error: '',
			successMessage: '',
			userStore: null,
		};
	},
	created() {
		this.userStore = useUserStore();
		this.fetchProfile();
	},
	methods: {
		getTargetUserId() {
			// prefer route param 'userId' if provided, otherwise use logged-in user's id
			const param = this.$route && this.$route.params && (this.$route.params.userId || this.$route.params.user_id);
			return param ? Number(param) : (this.userStore?.user?.id || this.userStore?.user?.user_id);
		},
		async fetchProfile() {
			try {
				this.loading = true;
				const id = this.getTargetUserId();
				if (!id) {
					this.error = 'No user id available to fetch profile.';
					return;
				}
				const resp = await api.get(`/user/${id}`);
				// API may return marshalled user or doctor object
				this.profile = resp;
				// Normalize into form object matching example JSON
				this.form = {
					user_id: resp.user_id || resp.id || resp.user_id,
					username: resp.username || resp.name || resp.username,
					fullname: resp.fullname || resp.full_name || '',
					phone: resp.phone || '',
					email: resp.email || '',
					active: resp.active === undefined ? true : resp.active,
					doctor_id: resp.doctor_id || resp.doctor_id || resp.user_id,
					department_name: resp.department_name || '',
					qualification: resp.qualification || '',
					experience_years: resp.experience_years || 0,
					specialization: resp.specialization || '',
					consultation_fee: resp.consultation_fee || 0,
					is_active: resp.is_active === undefined ? true : resp.is_active,
				};
			} catch (err) {
				this.error = err.message || 'Failed to fetch profile.';
				console.error(err);
			} finally {
				this.loading = false;
			}
		},
		cancel() {
			// reset form to original profile values
			if (this.profile) this.fetchProfile();
		},
		async saveProfile() {
			try {
				this.isSaving = true;
				const id = this.getTargetUserId();
				if (!id) {
					this.error = 'No user id available to update profile.';
					return;
				}

				// Build payload - include both user and doctor fields
				const payload = {
					username: this.form.username,
					fullname: this.form.fullname,
					phone: this.form.phone,
					email: this.form.email,
					active: this.form.active,
					// doctor fields
					department_name: this.form.department_name,
					qualification: this.form.qualification,
					experience_years: this.form.experience_years,
					specialization: this.form.specialization,
					consultation_fee: this.form.consultation_fee,
					is_active: this.form.is_active
				};

				await api.patch(`/user/${id}`, payload);
				this.successMessage = 'Profile updated successfully.';
				// refresh
				await this.fetchProfile();
				setTimeout(() => (this.successMessage = ''), 3000);
			} catch (err) {
				this.error = err.message || 'Failed to update profile.';
				console.error(err);
			} finally {
				this.isSaving = false;
			}
		},
		reload() {
			this.fetchProfile();
		}
	}
};
</script>

<style scoped>
.form-label { font-weight: 600; }
</style>

