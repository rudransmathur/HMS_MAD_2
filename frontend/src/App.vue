<script>
  import { defineComponent } from 'vue';

  import Navbar from './components/Navbar.vue';
  import Footer from './components/Footer.vue';
  export default {
    data() {
      return {};
    },
    components: {
      Navbar,
      Footer,
    },
  }
</script>

<template>
  <div id="app">
    <Navbar />
    <router-view />
    <Footer />
  </div>
</template>

<style scoped></style>
