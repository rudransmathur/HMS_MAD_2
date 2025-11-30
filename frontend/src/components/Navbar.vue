<template>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <!-- Container wrapper -->
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/">HMS</router-link>

        <!-- Toggle button -->
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false"
          aria-label="Toggle navigation">
          <i class="fas fa-bars text-light"></i>
        </button>

        <!-- Collapsible wrapper -->
        <div class="collapse navbar-collapse" id="navbarSupportedContent">

          <!-- Left links -->
          <!-- Doctor -->
          <ul v-if="isDoctor" class="navbar-nav mt-3 mt-lg-0">
            <li class="nav-item text-center mx-2 mx-lg-1">
              <router-link class="nav-link" to="/doctorappointments">
                Appointments
              </router-link>
            </li>
            <li class="nav-item text-center mx-2 mx-lg-1">
              <router-link class="nav-link" to="/doctortreatments">
                Diagnosis Reports
              </router-link>
            </li>
          </ul>

          <!-- Patient -->
          <ul v-if="isPatient" class="navbar-nav mt-3 mt-lg-0">
            <li class="nav-item text-center mx-2 mx-lg-1">
              <router-link class="nav-link" to="/patientappointments">
                Appointments
              </router-link>
            </li>
            <li class="nav-item text-center mx-2 mx-lg-1">
              <router-link class="nav-link" to="/patienttreatments">
                Diagnosis Reports
              </router-link>
            </li>
            <li class="nav-item text-center mx-2 mx-lg-1">
              <router-link class="nav-link" to="/patientsearch">
                Search Doctors
              </router-link>
            </li>
          </ul>

          <!-- Admin -->
           <ul v-if="isAdmin" class="navbar-nav mt-3 mt-lg-0">
            <li class="nav-item text-center mx-2 mx-lg-1">
              <router-link class="nav-link" to="/admindoctors">
                Doctor Requests
              </router-link>
            </li>
            <li class="nav-item text-center mx-2 mx-lg-1">
              <router-link class="nav-link" to="/adminappointments">
                Manage Appointments
              </router-link>
            </li>
            <li class="nav-item text-center mx-2 mx-lg-1">
              <router-link class="nav-link" to="/adminsearch">
                Search/Edit Users
              </router-link>
            </li>
          </ul>
          <!-- Left links -->

          <!-- Right links -->
          <ul class="navbar-nav ms-auto d-flex flex-row mt-3 mt-lg-0">
            <li v-if="!isAuthenticated" class="nav-item text-center mx-2 mx-lg-1">
              <router-link class="nav-link" to="/login">
                Login
              </router-link>
            </li>
            <li v-if="!isAuthenticated" class="nav-item text-center mx-2 mx-lg-1">
              <router-link class="nav-link" to="/signup">
                Signup
              </router-link>
            </li>
            <li v-if="isAuthenticated" class="nav-item dropdown">
              <button class="nav-link dropdown-toggle d-flex align-items-center" type="button" id="profileDropdown" data-bs-toggle="dropdown"
                aria-expanded="false" style="background: none; border: none; cursor: pointer;">
                <i class="bi bi-person"></i>
              </button>
              <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="profileDropdown">
                <li v-if="isPatient">
                  <router-link class="dropdown-item" to="/patientprofile">Profile</router-link>
                </li>
                <li v-if="isDoctor">
                  <router-link class="dropdown-item" to="/doctorprofile">Profile</router-link>
                </li>
                <li v-if="!isAdmin">
                  <hr class="dropdown-divider" />
                </li>
                <li>
                  <a class="dropdown-item" href="#" @click.prevent="handleLogout">Logout</a>
                </li>
              </ul>
            </li>
          </ul>
          <!-- Right links -->
        </div>
        <!-- Collapsible wrapper -->
      </div>
      <!-- Container wrapper -->
    </nav>
    <!-- Navbar -->
</template>

<script>
    import useUserStore from '@/stores/user';

    export default {
        name: 'Navbar',
        data() {
            return {
                userStore: null
            };
        },
        created(){
            this.userStore = useUserStore();
        },
        computed:{
            isAuthenticated(){
                return this.userStore && this.userStore.isAuthenticated;
            },
            isAdmin(){
                return this.userStore && this.userStore.isAdmin;
            },
            isPatient(){
                return this.userStore && this.userStore.isPatient;
            },
            isDoctor(){
                return this.userStore && this.userStore.isDoctor;
            },
            displayName(){
                return this.userStore?.user?.name || 'Account';
            }
        },
        methods: {
          handleLogout() {
            if (this.userStore && typeof this.userStore.logout === 'function') {
              this.userStore.logout();
            }
            if (this.$router) {
              this.$router.push('/');
            }
          }
        }
    }
    
</script>

<style>
    .btn {
    padding: .55rem 1.5rem .45rem;
    }
</style>