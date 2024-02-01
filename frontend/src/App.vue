<template>
  <nav class="navbar navbar-expand-lg navbar-custom">
    <div class="container">
      <span class="navbar-brand">Habitville</span>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ml-auto">
          <!-- Habit Tracker button -->
          <li class="nav-item">
            <router-link
              to="/"
              class="btn btn-outline-light m-2"
            >
              Habit Tracker
            </router-link>
          </li>
          <!-- Profile Page button -->
          <li class="nav-item">
            <router-link
              to="/profile"
              class="btn btn-outline-light m-2"
            >
              Profile Page
            </router-link>
          </li>
          <!-- Logout button -->
          <li class="nav-item">
            <button
              type="button"
              class="btn btn-outline-light m-2"
              @click="logout"
            >
              Logout
            </button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  
  <main class="container pt-4">
    <RouterView class="flex-shrink-0" />
  </main>
</template>


<script lang="ts">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";

export default defineComponent({
    components: { RouterView },

    methods: {
      logout() {
        window.location.href = "http://localhost:8000/logout/";
      },
    },
});
</script>

<style>
body, html {
    margin: 0;
    padding: 0;
    font-family: Arial, sans-serif;
    background-color: #65dc6f; 
    color: #333;
}

#app { 
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    background-color: #65dc6f; 
}

.navbar-custom {
    background-color: #4CAF50; 
}

.navbar-custom .navbar-brand {
    color: white;
    cursor: default; 
}

.navbar-custom .navbar-brand:hover {
    color: white; 
}

.navbar-custom .navbar-nav .nav-link {
    color: white;
}

.navbar-custom .navbar-nav .nav-link:hover {
    color: white; 
}

main {
    flex: 1; 
    background-color: inherit; 
}

.footer-custom {
    background-color: #4CAF50; 
    color: white;
}

main * {
    background-color: inherit;
}
</style>
