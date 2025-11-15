<template>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <!-- Container wrapper -->
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/">HMS</router-link>

        <!-- Toggle button -->
        <button class="navbar-toggler" type="button" data-mdb-collapse-init
          data-mdb-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false"
          aria-label="Toggle navigation">
          <i class="fas fa-bars text-light"></i>
        </button>

        <!-- Collapsible wrapper -->
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <!-- Left links -->
          <ul class="navbar-nav me-auto d-flex flex-row mt-3 mt-lg-0">
            <li v-if="isAdmin" class="nav-item text-center mx-2 mx-lg-1">
              <router-link class="nav-link" to="/admin">
                Doctors
              </router-link>
            </li>
            <li v-if="isPatient" class="nav-item text-center mx-2 mx-lg-1">
              <router-link class="nav-link" to="/admin">
                Doctors
              </router-link>
            </li>
            <li class="nav-item text-center mx-2 mx-lg-1">
              <router-link class="nav-link" aria-disabled="true" href="/">
                Disabled
              </router-link>
            </li>
            <li class="nav-item dropdown text-center mx-2 mx-lg-1">
              <a class="nav-link dropdown-toggle" href="/" id="navbarDropdown" role="button" data-mdb-dropdown-init
                aria-expanded="false">
                Dropdown
            </a>
              <!-- Dropdown menu -->
              <ul class="dropdown-menu dropdown-menu-dark" aria-labelledby="navbarDropdown">
                <li><a class="dropdown-item" href="#">Action</a></li>
                <li><a class="dropdown-item" href="#">Another action</a></li>
                <li>
                  <hr class="dropdown-divider" />
                </li>
                <li>
                  <a class="dropdown-item" href="#">Something else here</a>
                </li>
              </ul>
            </li>
          </ul>
          <!-- Left links -->

          <!-- Right links -->
          <ul class="navbar-nav ms-auto d-flex flex-row mt-3 mt-lg-0">
            <li v-if="!isAuthenticated" class="nav-item text-center mx-2 mx-lg-1">
              <router-link class="nav-link" href="#!">
                Login
              </router-link>
            </li>
            <li v-if="!isAuthenticated" class="nav-item text-center mx-2 mx-lg-1">
              <router-link class="nav-link" href="#!">
                Signup
              </router-link>
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
                return this.userStore?.user?.role === 'patient'
            },
            isDoctor(){
                return this.userStore?.user?.role === 'doctor'
            },
            displayName(){
                return this.userStore?.user?.name || 'Account';
            }
        }
    }
    
</script>

<style>
    .btn {
    padding: .55rem 1.5rem .45rem;
    }
</style>