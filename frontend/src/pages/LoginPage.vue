<template>
    <div class="d-flex justify-content-center align-items-center" style="min-height:70vh;">
        <div class="card p-4 shadow" style="width:380px;">
            <h4 class="text-center mb-3">Sign in</h4>

            <div v-if="error" class="alert alert-danger py-2" role="alert">{{ error }}</div>

            <form @submit.prevent="onSubmit" nonvalidate>
                <div class="mb-3">
                    <label for="username" class="form-label">Username</label>
                    <input id="username" v-model="username" class="form-control" placeholder="patient1" required />
                </div>

                <div class="mb-3">
                    <label for="password" class="form-label">Password</label>
                    <input id="password" v-model="password" type="password" class="form-control" placeholder="********" required />
                </div>

                <div class="d-grid">
                    <button :disabled="loading" class="btn btn-primary">
                        <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                        {{ loading ? 'Signing in...' : 'Sign In' }}
                    </button>
                </div>
            </form>
            
            <div class="text-center mt-3">
                <small>Don't have an account? <router-link to="/signup">Sign up</router-link></small>
            </div>
        </div>
    </div>
</template>

<script>
import { useUserStore } from '@/stores/user';

export default {
    name:"Login page",
    data(){
        return {
            username: '',
            password: '',
            loading: false,
            error: "",
            userStore: null
        };
    },
    created() {
        this.userStore = useUserStore();
    },
    methods: {
        async onSubmit() {
            this.error = "";
            this.loading = true;
            try {
                await this.userStore.loginWithCredentials("/auth/login", {
                    username: this.username,
                    password: this.password
                });
                this.$router.push({ path: '/' });
            } catch (err) {
                this.error = err.message || "An error occurred during login.";
                console.error("Login error:", err);
            } finally {
                this.loading = false;
            }
        }
    }
}

</script>

<style scoped>
.card{ border-radius:10px; }
</style>